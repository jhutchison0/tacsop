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
from hypothesis import settings

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


def test_disarmed_tripwire_lets_deletion_through(sandbox, monkeypatch):
    # Between tests the tripwire is disarmed, so pytest's own session cleanup runs.
    _, outside = sandbox
    target = outside / "f.txt"
    target.write_text("x")
    monkeypatch.setattr(isolation, "_armed", False)

    target.unlink()

    assert not target.exists()


def test_default_roots_are_temp_hypothesis_and_configured_extras(tmp_path):
    extra = tmp_path / "repo-cache"

    roots = isolation._allow_roots([extra])

    assert Path(os.path.realpath(tempfile.gettempdir())) in roots
    assert Path(os.path.realpath(settings().database.path)) in roots
    assert Path(os.path.realpath(extra)) in roots
    assert not isolation._inside("/data/grib/latest.grib2", roots)
    assert not isolation._inside(Path.home() / "real.txt", roots)
