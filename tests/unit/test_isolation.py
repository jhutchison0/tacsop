"""Tests for the test-isolation tripwire (tests/isolation.py).

Each test narrows the allowlist to a directory inside tmp_path, puts a sentinel
outside that directory but still inside tmp_path, and asserts two things: the
tripwire raises its own exception class, and the sentinel still exists. A test
that only asserted "something raised" would pass on a box with no tripwire,
because deleting a path that does not exist raises too.
"""

import importlib
import io
import os
import shutil
import socket
import subprocess
import tempfile
from pathlib import Path
from shutil import rmtree as rmtree_bound_at_import

import pytest
from dotenv import load_dotenv

from tests import isolation


@pytest.fixture(autouse=True)
def private_log(tmp_path, monkeypatch):
    """Keep this module's deliberate catches out of the real tripwire log."""
    monkeypatch.setattr(isolation, "_log_path", tmp_path / "tripwire.log")


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Narrow the allowlist to tmp_path/allowed; return (allowed, sentinel_dir)."""
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    monkeypatch.setattr(isolation, "_allow", (allowed,))
    return allowed, outside


def test_unlink_outside_allowlist_raises_and_file_survives(sandbox):
    _, outside = sandbox
    sentinel = outside / "keep.txt"
    sentinel.write_text("real data")

    with pytest.raises(isolation.IsolationError):
        sentinel.unlink()

    assert sentinel.exists()


def test_delete_inside_allowlist_still_works(sandbox):
    allowed, _ = sandbox
    scratch = allowed / "scratch"
    scratch.mkdir()
    (scratch / "f.txt").write_text("x")

    (scratch / "f.txt").unlink()
    rmtree_bound_at_import(scratch)

    assert not scratch.exists()


def test_rmtree_bound_at_import_outside_allowlist_raises(sandbox):
    # The 138 GB incident shape: a guard that patches shutil.rmtree misses a
    # module that ran `from shutil import rmtree` before the patch.
    _, outside = sandbox
    victim = outside / "cache"
    victim.mkdir()
    (victim / "grib.bin").write_text("real data")

    with pytest.raises(isolation.IsolationError):
        rmtree_bound_at_import(victim)

    assert (victim / "grib.bin").exists()


def test_rmdir_outside_allowlist_raises_and_directory_survives(sandbox):
    _, outside = sandbox
    empty = outside / "empty"
    empty.mkdir()

    with pytest.raises(isolation.IsolationError):
        empty.rmdir()

    assert empty.is_dir()


@pytest.mark.parametrize("rm", ["rm", shutil.which("rm") or "/bin/rm"])
def test_subprocess_rm_outside_allowlist_raises_and_tree_survives(sandbox, rm):
    _, outside = sandbox
    victim = outside / "cache"
    victim.mkdir()
    (victim / "grib.bin").write_text("real data")

    with pytest.raises(isolation.IsolationError):
        subprocess.run([rm, "-rf", str(victim)], check=False)

    assert (victim / "grib.bin").exists()


def test_subprocess_rm_inside_allowlist_still_works(sandbox):
    allowed, _ = sandbox
    scratch = allowed / "scratch"
    scratch.mkdir()

    subprocess.run(["rm", "-rf", "scratch"], cwd=allowed, check=True)

    assert not scratch.exists()


def test_connect_to_a_remote_address_raises():
    with socket.socket() as s:
        s.settimeout(0.5)  # without the tripwire this fails as a timeout, not a pass
        with pytest.raises(isolation.IsolationError):
            s.connect(("192.0.2.1", 80))  # TEST-NET-1, reserved for documentation


def test_dns_lookup_of_a_remote_name_raises():
    with pytest.raises(isolation.IsolationError):
        socket.getaddrinfo("example.invalid", 443)


def test_connect_to_loopback_still_works():
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen()
        with socket.create_connection(server.getsockname(), timeout=1):
            pass


def test_a_catch_appends_one_line_to_the_log(sandbox, tmp_path, request):
    _, outside = sandbox
    sentinel = outside / "keep.txt"
    sentinel.write_text("real data")

    with pytest.raises(isolation.IsolationError):
        sentinel.unlink()

    lines = (tmp_path / "tripwire.log").read_text().splitlines()
    assert len(lines) == 1
    assert " TRIPWIRE event=os.remove " in lines[0]
    assert f"target={sentinel}" in lines[0]
    assert f"test={request.node.nodeid}" in lines[0]


def test_load_dotenv_with_no_path_loads_nothing(tmp_path, monkeypatch):
    # python-dotenv searches upward from the calling file, so a caller beside a
    # .env file is the shape of a production entry point in a repo with a real .env.
    (tmp_path / ".env").write_text("OVERWATCH_PROBE=from_real_env\n")
    (tmp_path / "entry_point_probe.py").write_text(
        "from dotenv import load_dotenv\nloaded = load_dotenv()\n"
    )
    monkeypatch.syspath_prepend(tmp_path)
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)

    entry_point = importlib.import_module("entry_point_probe")

    assert entry_point.loaded is False
    assert "OVERWATCH_PROBE" not in os.environ


def test_load_dotenv_outside_allowlist_loads_nothing(sandbox, monkeypatch):
    _, outside = sandbox
    (outside / ".env").write_text("OVERWATCH_PROBE=from_real_env\n")
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)

    assert load_dotenv(outside / ".env") is False
    assert "OVERWATCH_PROBE" not in os.environ


def test_load_dotenv_inside_allowlist_still_loads(sandbox, monkeypatch):
    allowed, _ = sandbox
    (allowed / ".env").write_text("OVERWATCH_PROBE=from_fixture\n")
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)

    assert load_dotenv(allowed / ".env") is True
    assert os.environ["OVERWATCH_PROBE"] == "from_fixture"


def test_load_dotenv_from_a_stream_still_loads(monkeypatch):
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)

    assert load_dotenv(stream=io.StringIO("OVERWATCH_PROBE=from_stream\n")) is True
    assert os.environ["OVERWATCH_PROBE"] == "from_stream"


def test_the_hook_returns_early_when_disarmed(sandbox, monkeypatch):
    # Pins the early return only; that pytest disarms between tests is pinned by
    # test_fixture_setup_and_teardown_deletes_are_caught's neighbours, not here.
    _, outside = sandbox
    target = outside / "f.txt"
    target.write_text("x")
    monkeypatch.setattr(isolation, "_armed", False)

    target.unlink()

    assert not target.exists()


def test_default_roots_are_temp_and_configured_extras(tmp_path, monkeypatch):
    # Under CI=true, Hypothesis runs with no example database (database is None).
    monkeypatch.setattr(isolation, "_hypothesis_database_dir", lambda: None)
    extra = tmp_path / "repo-cache"

    roots = isolation._allow_roots([extra])

    assert roots == (Path(os.path.realpath(tempfile.gettempdir())), Path(os.path.realpath(extra)))
    assert not isolation._inside("/data/grib/latest.grib2", roots)


def test_default_roots_include_hypothesis_database_dir(tmp_path, monkeypatch):
    database = tmp_path / "hypothesis-examples"
    monkeypatch.setattr(isolation, "_hypothesis_database_dir", lambda: database)

    assert Path(os.path.realpath(database)) in isolation._allow_roots([])


needs_symlinks = pytest.mark.skipif(os.name == "nt", reason="symlinks need privileges on Windows")


@needs_symlinks
def test_rmtree_with_trailing_slash_through_an_allowed_symlink_raises(sandbox):
    # With a trailing slash the kernel follows the link, so the real directory empties.
    allowed, outside = sandbox
    real = outside / "cache"
    real.mkdir()
    (real / "data.bin").write_text("real data")
    (allowed / "link").symlink_to(real, target_is_directory=True)

    with pytest.raises(isolation.IsolationError):
        rmtree_bound_at_import(str(allowed / "link") + os.sep)

    assert (real / "data.bin").exists()


@needs_symlinks
def test_unlink_dotdot_after_an_allowed_symlink_raises(sandbox):
    # The kernel resolves the link before "..", so link/../data.bin lands in outside/.
    allowed, outside = sandbox
    (outside / "sub").mkdir()
    victim = outside / "data.bin"
    victim.write_text("real data")
    (allowed / "link").symlink_to(outside / "sub", target_is_directory=True)

    with pytest.raises(isolation.IsolationError):
        os.unlink(f"{allowed / 'link'}/../data.bin")

    assert victim.exists()


@needs_symlinks
def test_unlinking_an_allowed_symlink_removes_only_the_link(sandbox):
    allowed, outside = sandbox
    real = outside / "keep.txt"
    real.write_text("real data")
    link = allowed / "link.txt"
    link.symlink_to(real)

    link.unlink()

    assert not link.is_symlink()
    assert real.exists()


def test_load_dotenv_with_a_stream_and_a_real_path_loads_nothing(sandbox, monkeypatch):
    # python-dotenv reads dotenv_path first when it names a file, so a stream
    # argument must not open the gate for a path outside the allowlist.
    _, outside = sandbox
    (outside / ".env").write_text("OVERWATCH_PROBE=from_real_env\n")
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)

    assert load_dotenv(outside / ".env", stream=io.StringIO("")) is False
    assert "OVERWATCH_PROBE" not in os.environ


RM = shutil.which("rm") or "/bin/rm"


def test_subprocess_with_rm_as_executable_raises(sandbox):
    _, outside = sandbox
    victim = outside / "data.bin"
    victim.write_text("real data")

    with pytest.raises(isolation.IsolationError):
        subprocess.run(["cleanup", "-f", str(victim)], executable=RM, check=False)

    assert victim.exists()


@pytest.mark.skipif(not hasattr(os, "posix_spawn"), reason="POSIX only")
def test_posix_spawn_rm_outside_allowlist_raises(sandbox):
    _, outside = sandbox
    victim = outside / "data.bin"
    victim.write_text("real data")

    with pytest.raises(isolation.IsolationError):
        os.waitpid(os.posix_spawn(RM, ["rm", "-f", str(victim)], os.environ), 0)

    assert victim.exists()


@pytest.mark.skipif(os.name == "nt", reason="rmtree dir_fd needs POSIX fd functions")
def test_rmtree_relative_to_a_directory_descriptor_raises(sandbox, monkeypatch):
    # The tripwire cannot resolve a name against a descriptor, so it refuses
    # rather than guess from the working directory (here, an allowed one).
    allowed, outside = sandbox
    victim = outside / "cache"
    victim.mkdir()
    (victim / "data.bin").write_text("real data")
    monkeypatch.chdir(allowed)
    fd = os.open(outside, os.O_RDONLY)
    try:
        with pytest.raises(isolation.IsolationError):
            rmtree_bound_at_import("cache", dir_fd=fd)
    finally:
        os.close(fd)

    assert (victim / "data.bin").exists()


@pytest.mark.parametrize(
    "lookup",
    [
        lambda: socket.gethostbyname("example.invalid"),
        lambda: socket.gethostbyaddr("192.0.2.1"),
        lambda: socket.getnameinfo(("192.0.2.1", 80), 0),
    ],
    ids=["gethostbyname", "gethostbyaddr", "getnameinfo"],
)
def test_dns_lookups_of_remote_hosts_raise(lookup):
    with pytest.raises(isolation.IsolationError):
        lookup()


def test_udp_sendto_a_remote_address_raises():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        with pytest.raises(isolation.IsolationError):
            s.sendto(b"x", ("192.0.2.1", 9))


@pytest.mark.skipif(not hasattr(socket.socket, "sendmsg"), reason="no sendmsg on this platform")
def test_udp_sendmsg_to_a_remote_address_raises():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        with pytest.raises(isolation.IsolationError):
            s.sendmsg([b"x"], [], 0, ("192.0.2.1", 9))


def test_connect_to_a_server_bound_to_all_interfaces_still_works():
    # A server bound to "" reports 0.0.0.0, and tests connect to what it reports.
    with socket.socket() as server:
        server.bind(("", 0))
        server.listen()
        with socket.create_connection(server.getsockname(), timeout=1):
            pass


def test_localhost_in_capitals_is_local():
    assert isolation._is_local("LOCALHOST")


def test_a_catch_still_raises_isolation_error_when_the_log_cannot_be_written(
    sandbox, tmp_path, monkeypatch
):
    # An OSError from the log would be swallowed by code that wraps its delete
    # in `except OSError`, so the catch must surface as IsolationError regardless.
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("")
    monkeypatch.setattr(isolation, "_log_path", blocker / "tripwire.log")
    _, outside = sandbox
    sentinel = outside / "keep.txt"
    sentinel.write_text("real data")

    with pytest.raises(isolation.IsolationError):
        sentinel.unlink()

    assert sentinel.exists()


HUB = Path(__file__).resolve().parents[2]


@pytest.fixture
def project(pytester, monkeypatch):
    """A fresh project run in its own pytest process; returns a directory of real data.

    The process's temp dir is narrowed to <project>/tmp, so real/ and pytester's
    --basetemp both sit outside the default allowlist.
    """
    narrowed = pytester.path / "tmp"
    narrowed.mkdir()
    real = pytester.path / "real"
    real.mkdir()
    monkeypatch.setenv("TMPDIR", str(narrowed))
    monkeypatch.setenv("PYTHONPATH", str(HUB))
    monkeypatch.delenv("OVERWATCH_PROBE", raising=False)
    return real


def _register(pytester, conftest=""):
    """Register the plugin the way ISOLATION.md tells a downstream repo to.

    Through addopts, never conftest.py: pytest runs a whole conftest before it
    reads pytest_plugins, so production imports there would beat the plugin.
    """
    pytester.makepyprojecttoml('[tool.pytest.ini_options]\naddopts = ["-p", "tests.isolation"]\n')
    pytester.makeconftest(conftest)


def test_fixture_setup_and_teardown_deletes_are_caught(pytester, project):
    # The incident was a fixture, so both ends of a fixture must be armed.
    at_setup, at_teardown = project / "setup.bin", project / "teardown.bin"
    at_setup.write_text("real data")
    at_teardown.write_text("real data")
    _register(pytester)
    pytester.makepyfile(
        f"""
        import os

        import pytest

        @pytest.fixture
        def deletes_at_setup():
            os.remove({str(at_setup)!r})

        @pytest.fixture
        def deletes_at_teardown():
            yield
            os.remove({str(at_teardown)!r})

        def test_setup(deletes_at_setup):
            pass

        def test_teardown(deletes_at_teardown):
            pass
        """
    )

    pytester.runpytest_subprocess().assert_outcomes(passed=1, errors=2)

    assert at_setup.exists()
    assert at_teardown.exists()


def test_registration_holds_against_a_conftest_that_imports_production_code(pytester, project):
    # A conftest runs whole before pytest reads its pytest_plugins, and a later
    # pytest_plugins assignment replaces an earlier one.
    (pytester.path / ".env").write_text("OVERWATCH_PROBE=from_real_env\n")
    pytester.makepyfile(prodpkg="from dotenv import load_dotenv\n\nLOADED = load_dotenv()\n")
    _register(pytester, conftest="import prodpkg\n\npytest_plugins = []\n")
    pytester.makepyfile(
        test_probe="""
        import os

        import prodpkg

        def test_guarded(pytestconfig):
            assert pytestconfig.pluginmanager.has_plugin("tests.isolation")
            assert prodpkg.LOADED is False
            assert "OVERWATCH_PROBE" not in os.environ
        """
    )

    pytester.runpytest_subprocess().assert_outcomes(passed=1)


def test_a_test_that_writes_the_pytest_cache_passes_on_a_fresh_checkout(pytester, project):
    _register(pytester)
    pytester.makepyfile(
        """
        def test_cache(request):
            request.config.cache.set("probe/value", 1)
        """
    )

    pytester.runpytest_subprocess().assert_outcomes(passed=1)


def test_tmp_path_works_when_basetemp_is_outside_the_temp_dir(pytester, project):
    _register(pytester)
    pytester.makepyfile(
        """
        def test_scratch(tmp_path):
            scratch = tmp_path / "f.txt"
            scratch.write_text("x")
            scratch.unlink()
        """
    )

    pytester.runpytest_subprocess().assert_outcomes(passed=1)
