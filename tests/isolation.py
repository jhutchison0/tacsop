"""Test-isolation tripwire: while a test runs, it may not touch the real world.

A pytest plugin, registered from tests/conftest.py. Three tripwires:

- Deletion outside the allowlist raises: `os.remove`, `os.rmdir`, `shutil.rmtree`,
  and a subprocess `rm`, `rmdir`, `unlink`, or `shred`.
- Network to anything but loopback raises: `socket.connect`, `socket.getaddrinfo`.
- `load_dotenv` loads nothing unless given a stream or a path inside the allowlist,
  so the repo's real `.env` never refills a variable a test removed.

The first two are one Python audit hook, armed only while a test runs (setup,
call, and teardown). An audit hook sees the call however the caller imported
it, which a monkeypatched function does not. Each catch appends one line to
`.claude/audits/isolation-tripwire.log`. What the tripwire cannot see is listed
in .claude/skills/shift-left-testing/ISOLATION.md.
"""

import ipaddress
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytest


class IsolationError(RuntimeError):
    """A test tried to reach outside its sandbox."""


_DELETERS = frozenset({"rm", "rmdir", "unlink", "shred"})

_armed = False
_default_allow: tuple[Path, ...] = ()
_allow: tuple[Path, ...] = ()
_log_path: Path | None = None
_current_test = ""


def _inside(path, roots) -> bool:
    absolute = os.path.abspath(os.fsdecode(path))
    # Resolve symlinks in the parent only: deleting a link removes the link.
    parent, name = os.path.split(absolute)
    target = Path(os.path.realpath(parent)) / name
    return any(target == root or root in target.parents for root in roots)


def _is_local(host) -> bool:
    if isinstance(host, bytes):
        host = host.decode(errors="replace")
    if host in (None, "", "localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _trip(event: str, target) -> None:
    shown = target if isinstance(target, tuple) else os.fsdecode(target)
    if _log_path is not None:
        _log_path.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().astimezone().isoformat(timespec="seconds")
        with open(_log_path, "a") as log:
            log.write(f"[{stamp}] TRIPWIRE event={event} target={shown} test={_current_test}\n")
    raise IsolationError(
        f"isolation tripwire: {event} {shown!r} is outside the test sandbox; "
        "see .claude/skills/shift-left-testing/ISOLATION.md"
    )


def _audit(event: str, args: tuple) -> None:
    if not _armed:
        return
    if event == "shutil.rmtree":
        if not _inside(args[0], _allow):
            _trip(event, args[0])
    elif event in ("os.remove", "os.rmdir"):
        path, dir_fd = args
        if dir_fd is not None and dir_fd >= 0:
            return  # relative to an open directory; shutil.rmtree checked the top
        if not _inside(path, _allow):
            _trip(event, path)
    elif event == "subprocess.Popen":
        _executable, argv, cwd, _env = args
        if argv and os.path.basename(os.fsdecode(argv[0])) in _DELETERS:
            base = os.fsdecode(cwd) if cwd is not None else os.getcwd()
            for arg in map(os.fsdecode, argv[1:]):
                if not arg.startswith("-") and not _inside(os.path.join(base, arg), _allow):
                    _trip(event, arg)
    elif event == "socket.connect":
        address = args[1]
        if isinstance(address, tuple) and not _is_local(address[0]):
            _trip(event, address)
    elif event == "socket.getaddrinfo":
        if not _is_local(args[0]):
            _trip(event, args[0])


sys.addaudithook(_audit)


def _guard_dotenv() -> None:
    """Make load_dotenv load nothing unless given a stream or a path inside the allowlist.

    Runs when pytest imports this plugin, before any test module (or the code it
    tests) runs `from dotenv import load_dotenv`, so the bound name is this one.
    """
    try:
        import dotenv
        import dotenv.main
    except ImportError:
        return
    real = dotenv.main.load_dotenv

    def load_dotenv(dotenv_path=None, stream=None, *args, **kwargs):
        if stream is not None or (dotenv_path is not None and _inside(dotenv_path, _allow)):
            return real(dotenv_path, stream, *args, **kwargs)
        return False

    dotenv.load_dotenv = dotenv.main.load_dotenv = load_dotenv


_guard_dotenv()


def _allow_roots(extra) -> tuple[Path, ...]:
    """The system temp dir, Hypothesis's example database, and configured extras."""
    roots = [tempfile.gettempdir(), *extra]
    try:
        from hypothesis import settings

        roots.append(settings().database.path)  # Hypothesis deletes stale examples
    except (ImportError, AttributeError):
        pass  # no Hypothesis, or a database with no directory
    return tuple(Path(os.path.realpath(root)) for root in roots)


def pytest_addoption(parser):
    parser.addini(
        "isolation_allow",
        type="paths",
        default=[],
        help="Extra directories tests may delete in (see ISOLATION.md).",
    )


def pytest_configure(config):
    global _default_allow, _allow, _log_path
    _default_allow = _allow = _allow_roots(config.getini("isolation_allow"))
    _log_path = config.rootpath / ".claude" / "audits" / "isolation-tripwire.log"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    global _armed, _allow, _current_test
    _allow = _default_allow
    _current_test = item.nodeid
    _armed = True
    try:
        yield
    finally:
        _armed = False
