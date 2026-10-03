"""Tests for /pcc check 7, the Private-Term Check, and the output-destination rule.

Check 7 is a bash block in .claude/commands/pcc.md. These tests extract it
verbatim and run it in a scratch git repository with its own term list, so no
result depends on this machine's list or on the hub's history. The block exits
0 in every case; a line printed is the finding. The output never contains a
term: the check exists because a probe's own output republished what it was
checking for (2026-10-01, redacted 2026-10-02).
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PCC = REPO_ROOT / ".claude" / "commands" / "pcc.md"
TERM = "zq-private-host-7731"  # a string no real file holds

pytestmark = pytest.mark.skipif(
    shutil.which("bash") is None or shutil.which("git") is None,
    reason="the check needs bash and git on PATH",
)


def _check_7_block() -> str:
    text = PCC.read_text(encoding="utf-8")
    section = re.search(r"^### 7\. Private-Term Check.*?(?=^### |^## )", text, re.S | re.M)
    assert section, "pcc.md has no '### 7. Private-Term Check' section"
    blocks = re.findall(r"^```bash\n(.*?)^```$", section.group(0), re.S | re.M)
    assert len(blocks) == 1, "check 7 should hold exactly one bash block"
    return blocks[0]


@pytest.fixture
def repo(tmp_path):
    """A scratch git repo with one clean committed file, and a term list outside it."""
    root = tmp_path / "repo"
    root.mkdir()
    (tmp_path / "home").mkdir()
    env = {
        "PATH": os.environ["PATH"],
        "HOME": str(tmp_path / "home"),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.invalid",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.invalid",
    }

    def git(*args):
        subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True)

    git("init", "-q")
    (root / "clean.md").write_text("nothing private here\n")
    git("add", "clean.md")
    git("commit", "-q", "-m", "clean")
    terms = tmp_path / "terms"
    terms.write_text(f"{TERM}\n\n")
    script = tmp_path / "check7.sh"
    script.write_text(_check_7_block())
    return {"root": root, "env": env, "terms": terms, "script": script, "git": git}


def _run(repo, **extra_env):
    env = {**repo["env"], **extra_env}
    return subprocess.run(
        ["bash", str(repo["script"])], cwd=repo["root"], env=env, capture_output=True, text=True
    )


class TestCheck7:
    def test_clean_index_prints_nothing_and_exits_0(self, repo):
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"]))
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "")

    def test_committed_term_fails_naming_the_file_and_never_the_term(self, repo):
        (repo["root"] / "leak.md").write_text(f"the host is {TERM.upper()}\n")  # case differs
        repo["git"]("add", "leak.md")
        repo["git"]("commit", "-q", "-m", "leak")
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"]))
        assert r.returncode == 0
        assert "FAIL" in r.stdout and "leak.md" in r.stdout
        assert TERM.lower() not in (r.stdout + r.stderr).lower()

    def test_staged_term_is_caught_before_it_is_committed(self, repo):
        (repo["root"] / "staged.md").write_text(f"{TERM}\n")
        repo["git"]("add", "staged.md")
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"]))
        assert "FAIL" in r.stdout and "staged.md" in r.stdout

    def test_untracked_file_is_outside_the_index_and_not_scanned(self, repo):
        (repo["root"] / "wip.md").write_text(f"{TERM}\n")
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"]))
        assert r.stdout == ""

    def test_missing_list_warns_once_and_exits_0(self, repo):
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"].with_name("absent")))
        assert r.returncode == 0
        assert r.stdout.startswith("WARN") and r.stdout.count("\n") == 1

    def test_blank_only_list_warns_rather_than_matching_everything(self, repo):
        repo["terms"].write_text("\n  \n")
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"]))
        assert r.stdout.startswith("WARN")

    def test_default_list_lives_under_home_not_in_any_repo(self):
        block = _check_7_block()
        assert "$HOME/.config/tacsop/private-terms" in block
        assert "TACSOP_PRIVATE_TERMS" in block

    def test_quick_reference_names_the_check_as_blocking(self):
        assert re.search(r"^\| Private terms \|.*\| Block push \|$", PCC.read_text(encoding="utf-8"), re.M)


class TestDestinationRule:
    PHRASE = "the repository that owns the sensitivity"

    @pytest.mark.parametrize(
        "path",
        [
            ".claude/README.md",
            ".claude/agents/code-reviewer.md",
            ".claude/agents/proposer.md",
            ".claude/agents/decision-scientist.md",
        ],
    )
    def test_surface_carries_the_rule(self, path):
        assert self.PHRASE in (REPO_ROOT / path).read_text(encoding="utf-8")
