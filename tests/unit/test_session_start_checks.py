"""Tests for the tool checks in /session-start Step 4.

The checks are a bash block inside .claude/commands/session-start.md. These
tests extract that block verbatim and run it the way a session does, in a
throwaway directory with its own gitconfig and stub `gh` and `glab` binaries,
so no result depends on this machine's identity or auth. The block must exit 0
in every case: a nonzero exit reads as an error in Claude Code even when the
block printed nothing.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

COMMAND = Path(__file__).resolve().parents[2] / ".claude" / "commands" / "session-start.md"

pytestmark = pytest.mark.skipif(
    shutil.which("bash") is None or shutil.which("git") is None,
    reason="the checks need bash and git on PATH",
)


def _tool_check_block() -> str:
    step4 = re.search(r"^## Step 4.*?(?=^## Step 5)", COMMAND.read_text(), re.S | re.M).group(0)
    blocks = re.findall(r"^```bash\n(.*?)^```$", step4, re.S | re.M)
    assert len(blocks) == 2, "Step 4 should hold the health commands, then the tool checks"
    return blocks[1]


@pytest.fixture
def session(tmp_path):
    """A project dir with its own .venv, a stub bin dir, and a git identity."""
    project = tmp_path / "project"
    (project / ".venv").mkdir(parents=True)
    stubs = tmp_path / "bin"
    stubs.mkdir()
    for cli in ("gh", "glab"):
        stub = stubs / cli
        stub.write_text(f'#!/bin/sh\nexit "${{{cli.upper()}_STUB_EXIT:-0}}"\n')
        stub.chmod(0o755)
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text("[user]\n\tname = Test\n\temail = test@example.invalid\n")
    script = tmp_path / "checks.sh"
    script.write_text(_tool_check_block())
    env = {
        "PATH": f"{stubs}{os.pathsep}{os.environ['PATH']}",
        "HOME": str(tmp_path),
        "GIT_CONFIG_GLOBAL": str(gitconfig),
        "GIT_CONFIG_SYSTEM": os.devnull,
    }
    return {"project": project, "tmp": tmp_path, "script": script, "env": env}


def _run(session, **extra_env):
    env = {**session["env"], **extra_env}
    result = subprocess.run(
        ["bash", str(session["script"])],
        cwd=session["project"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"the block must exit 0; stderr: {result.stderr}"
    return result.stdout.strip()


def test_all_fine_prints_nothing(session):
    assert _run(session) == ""


@pytest.mark.parametrize("own", ["absolute", "relative"])
def test_the_projects_own_venv_is_not_stray(session, own):
    venv = session["project"] / ".venv" if own == "absolute" else ".venv"
    assert _run(session, VIRTUAL_ENV=str(venv)) == ""


def test_another_repos_venv_is_stray(session):
    other = session["tmp"] / "other-repo" / ".venv"
    other.mkdir(parents=True)

    out = _run(session, VIRTUAL_ENV=str(other))

    assert out.startswith(f"STRAY VIRTUAL_ENV={other}:")


def test_a_venv_that_does_not_exist_is_not_flagged(session):
    # uv falls back to the project's .venv when VIRTUAL_ENV names nothing.
    assert _run(session, VIRTUAL_ENV=str(session["tmp"] / "gone")) == ""


def test_cdpath_does_not_make_the_own_venv_look_stray(session):
    decoy = session["tmp"] / "decoy"
    (decoy / ".venv").mkdir(parents=True)

    out = _run(session, VIRTUAL_ENV=str(session["project"] / ".venv"), CDPATH=str(decoy))

    assert out == ""


def test_a_missing_git_identity_names_the_commit_step(session):
    out = _run(session, GIT_CONFIG_GLOBAL=os.devnull)

    assert out == "NO GIT IDENTITY: commits fail (/session-end Step 3)"


@pytest.mark.parametrize("cli", ["gh", "glab"])
def test_a_failed_auth_check_marks_results_unverified(session, cli):
    out = _run(session, **{f"{cli.upper()}_STUB_EXIT": "1"})

    assert out.startswith(f"{cli} AUTH CHECK FAILED")
    assert "UNVERIFIED (/session-end Step 6)" in out
