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

import functools
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

# Each launch event's args, as (program, argv, cwd).
_LAUNCHES = {
    "subprocess.Popen": lambda a: (a[0], a[1], a[2]),  # executable, args, cwd, env
    "os.posix_spawn": lambda a: (a[0], a[1], None),  # path, argv, env
    "os.spawn": lambda a: (a[1], a[2], None),  # mode, path, args, env
    "os.exec": lambda a: (a[0], a[1], None),  # path, args, env
}


def _program_name(program) -> str:
    name = os.path.basename(os.fsdecode(program)).lower()
    return name[:-4] if name.endswith(".exe") else name


def _deleter_paths(program, argv) -> list[str]:
    """The path arguments of a launch that runs rm, rmdir, unlink, or shred; else none."""
    argv = list(argv or [])
    names = [p for p in (program, *argv[:1]) if p is not None]
    if not any(_program_name(name) in _DELETERS for name in names):
        return []
    return [arg for arg in map(os.fsdecode, argv[1:]) if not arg.startswith("-")]

_armed = False
_default_allow: tuple[Path, ...] = ()
_allow: tuple[Path, ...] = ()
_log_path: Path | None = None
_current_test = ""


def _inside(path, roots) -> bool:
    """Where the kernel would act on `path`, inside one of `roots`?

    Never os.path.abspath: it folds ".." before symlinks resolve, and the kernel
    resolves them first. Deleting a link removes the link, so the last component
    stays unresolved, except where the kernel follows it (a trailing slash, "..").
    """
    raw = os.fsdecode(path)
    if not os.path.isabs(raw):
        raw = os.path.join(os.getcwd(), raw)
    parent, name = os.path.split(raw.rstrip(os.sep) or os.sep)
    if raw.endswith(os.sep) or name in ("", ".", ".."):
        target = Path(os.path.realpath(raw))
    else:
        target = Path(os.path.realpath(parent)) / name
    return any(target == root or root in target.parents for root in roots)


def _is_local(host) -> bool:
    if isinstance(host, bytes):
        host = host.decode(errors="replace")
    if host is None or host.lower() in ("", "localhost"):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return address.is_loopback or address.is_unspecified  # 0.0.0.0 reaches this host


def _trip(event: str, target) -> None:
    shown = target if isinstance(target, tuple) else os.fsdecode(target)
    if _log_path is not None:
        stamp = datetime.now().astimezone().isoformat(timespec="seconds")
        try:
            _log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(_log_path, "a") as log:
                log.write(f"[{stamp}] TRIPWIRE event={event} target={shown} test={_current_test}\n")
        except OSError:
            pass  # the catch matters more than its log line
    raise IsolationError(
        f"isolation tripwire: {event} {shown!r} is outside the test sandbox; "
        "see .claude/skills/shift-left-testing/ISOLATION.md"
    )


def _audit(event: str, args: tuple) -> None:
    if not _armed:
        return
    if event == "shutil.rmtree":
        path, dir_fd = args[0], args[1] if len(args) > 1 else None
        if dir_fd is not None and not os.path.isabs(os.fsdecode(path)):
            _trip(event, path)  # relative to a descriptor: unresolvable, so refuse
        elif not _inside(path, _allow):
            _trip(event, path)
    elif event in ("os.remove", "os.rmdir"):
        path, dir_fd = args
        if dir_fd is not None and dir_fd >= 0:
            return  # relative to an open directory; shutil.rmtree checked the top
        if not _inside(path, _allow):
            _trip(event, path)
    elif event in _LAUNCHES:
        program, argv, cwd = _LAUNCHES[event](args)
        base = os.fsdecode(cwd) if cwd is not None else os.getcwd()
        for arg in _deleter_paths(program, argv):
            if not _inside(os.path.join(base, arg), _allow):
                _trip(event, arg)
    elif event in ("socket.connect", "socket.sendto", "socket.sendmsg"):
        address = args[1]  # (self, address); None for sendmsg on a connected socket
        if isinstance(address, tuple) and not _is_local(address[0]):
            _trip(event, address)
    elif event in ("socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr"):
        if not _is_local(args[0]):
            _trip(event, args[0])
    elif event == "socket.getnameinfo":
        if not _is_local(args[0][0]):  # (sockaddr,)
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

    @functools.wraps(real)
    def load_dotenv(dotenv_path=None, stream=None, *args, **kwargs):
        # A path, when given, decides: python-dotenv reads it before the stream.
        allowed = _inside(dotenv_path, _allow) if dotenv_path is not None else stream is not None
        return real(dotenv_path, stream, *args, **kwargs) if allowed else False

    dotenv.load_dotenv = dotenv.main.load_dotenv = load_dotenv


_guard_dotenv()


def _hypothesis_database_dir():
    """Hypothesis's example directory, which it prunes; None if there is none (as under CI)."""
    try:
        from hypothesis import settings
    except ImportError:
        return None
    return getattr(settings().database, "path", None)


def _allow_roots(extra) -> tuple[Path, ...]:
    """The system temp dir, configured extras, and Hypothesis's example directory."""
    roots = [tempfile.gettempdir(), *extra]
    database = _hypothesis_database_dir()
    if database is not None:
        roots.append(database)
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
    extra = list(config.getini("isolation_allow"))
    if getattr(config.option, "basetemp", None):  # pytest clears it; tmp_path lives in it
        extra.append(config.invocation_params.dir / config.option.basetemp)
    _default_allow = _allow = _allow_roots(extra)
    _log_path = config.rootpath / ".claude" / "audits" / "isolation-tripwire.log"
    cache = getattr(config, "cache", None)
    if cache is not None:
        # On a fresh checkout pytest builds .pytest_cache through a temp dir it
        # then deletes. Build it now, while the tripwire is still disarmed.
        cache.mkdir("isolation")


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
