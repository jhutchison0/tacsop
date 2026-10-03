"""Tests for /pcc check 7, the Private-Term Check, and the output-destination rule.

Check 7 is a bash block in .claude/commands/pcc.md. These tests extract it
verbatim and run it in scratch git repositories with their own term lists, so
no result depends on this machine's list or on the hub's history. The block
exits 0 in every case; a line printed is the finding. The output never carries
a term, in a path or otherwise: the check exists because a probe's own output
republished what it was checking for (2026-10-01, redacted 2026-10-02).
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

    def git(*args, cwd=root):
        return subprocess.run(
            ["git", *args], cwd=cwd, env=env, check=True, capture_output=True, text=True
        ).stdout

    git("init", "-q")
    (root / "clean.md").write_text("nothing private here\n")
    git("add", "clean.md")
    git("commit", "-q", "-m", "clean")
    terms = tmp_path / "terms"
    terms.write_text(f"{TERM}\n\n")
    script = tmp_path / "check7.sh"
    script.write_text(_check_7_block())
    return {"root": root, "tmp": tmp_path, "env": env, "terms": terms, "script": script, "git": git}


def _run(repo, cwd=None, **extra_env):
    env = {**repo["env"], "TACSOP_PRIVATE_TERMS": str(repo["terms"]), **extra_env}
    return subprocess.run(
        ["bash", str(repo["script"])], cwd=cwd or repo["root"], env=env, capture_output=True, text=True
    )


def _commit(repo, name, content, message="c"):
    path = repo["root"] / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content)
    repo["git"]("add", "-A")
    repo["git"]("commit", "-q", "-m", message)


def _with_upstream(repo):
    """Push the clean commit to a bare remote so `@{upstream}..HEAD` means 'unpushed'."""
    remote = repo["tmp"] / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], env=repo["env"], check=True)
    repo["git"]("remote", "add", "origin", str(remote))
    repo["git"]("push", "-q", "-u", "origin", "HEAD")


def _no_term_in(result):
    assert TERM.lower() not in (result.stdout + result.stderr).lower()


class TestCheck7Content:
    def test_clean_index_prints_nothing_and_exits_0(self, repo):
        r = _run(repo)
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "")

    def test_committed_term_fails_naming_the_file_and_never_the_term(self, repo):
        _commit(repo, "leak.md", f"the host is {TERM.upper()}\n")  # case differs
        r = _run(repo)
        assert r.returncode == 0
        assert "FAIL" in r.stdout and "leak.md" in r.stdout
        _no_term_in(r)

    def test_staged_term_is_caught_before_it_is_committed(self, repo):
        (repo["root"] / "staged.md").write_text(f"{TERM}\n")
        repo["git"]("add", "staged.md")
        r = _run(repo)
        assert "FAIL" in r.stdout and "staged.md" in r.stdout

    def test_untracked_file_is_outside_the_index_and_not_scanned(self, repo):
        (repo["root"] / "wip.md").write_text(f"{TERM}\n")
        assert _run(repo).stdout == ""

    def test_unstaged_edit_to_a_tracked_file_is_not_pushed_and_not_scanned(self, repo):
        (repo["root"] / "clean.md").write_text(f"{TERM}\n")  # worktree only
        assert _run(repo).stdout == ""

    def test_binary_file_holding_a_term_is_a_fail(self, repo):
        _commit(repo, "blob.bin", b"\x00\x01" + TERM.encode() + b"\x00\x02")
        r = _run(repo)
        assert "FAIL" in r.stdout and "blob.bin" in r.stdout

    def test_terms_match_as_fixed_strings_not_regexes(self, repo):
        repo["terms"].write_text("a.b[1]\n")
        _commit(repo, "near.md", "aXb[1]\n")
        assert _run(repo).stdout == ""
        _commit(repo, "exact.md", "a.b[1]\n")
        r = _run(repo)
        assert "FAIL" in r.stdout and "exact.md" in r.stdout and "near.md" not in r.stdout

    def test_run_from_a_subdirectory_scans_the_whole_tree(self, repo):
        _commit(repo, "leak.md", f"{TERM}\n")
        _commit(repo, "sub/inner.md", "clean\n")
        r = _run(repo, cwd=repo["root"] / "sub")
        assert "FAIL" in r.stdout and "leak.md" in r.stdout


class TestCheck7PathsAndHistory:
    def test_term_in_a_directory_name_is_counted_and_the_path_is_withheld(self, repo):
        _commit(repo, f"{TERM}/readme.md", f"x: {TERM}\n")
        r = _run(repo)
        assert "FAIL" in r.stdout and "path name" in r.stdout
        _no_term_in(r)

    def test_term_only_in_a_file_name_is_a_fail(self, repo):
        _commit(repo, f"{TERM}.md", "nothing private in the content\n")
        r = _run(repo)
        assert "FAIL" in r.stdout and "name" in r.stdout
        _no_term_in(r)

    def test_term_in_an_unpushed_intermediate_commit_is_a_fail(self, repo):
        _with_upstream(repo)
        _commit(repo, "mid.md", f"{TERM}\n", "add")
        repo["git"]("rm", "-q", "mid.md")
        repo["git"]("commit", "-q", "-m", "remove")
        r = _run(repo)  # index and HEAD are clean; the push would carry the term
        assert "FAIL" in r.stdout and "mid.md" in r.stdout
        repo["git"]("push", "-q", "origin", "HEAD")
        assert _run(repo).stdout == ""  # nothing left unpushed

    def test_term_in_an_unpushed_commit_message_is_a_fail(self, repo):
        _with_upstream(repo)
        repo["git"]("commit", "-q", "--allow-empty", "-m", f"touches {TERM}")
        r = _run(repo)
        assert "FAIL" in r.stdout and "commit message" in r.stdout
        _no_term_in(r)


class TestCheck7List:
    def test_missing_list_warns_once_and_exits_0(self, repo):
        r = _run(repo, TACSOP_PRIVATE_TERMS=str(repo["terms"].with_name("absent")))
        assert r.returncode == 0
        assert r.stdout.startswith("WARN") and r.stdout.count("\n") == 1

    def test_blank_only_list_warns_rather_than_passing_silently(self, repo):
        repo["terms"].write_text("\n  \n")
        assert _run(repo).stdout.startswith("WARN")

    def test_list_lines_are_trimmed_of_spaces_and_carriage_returns(self, repo):
        _commit(repo, "leak.md", f"{TERM}\n")
        repo["terms"].write_text(f"  {TERM}  \r\n")
        r = _run(repo)
        assert "FAIL" in r.stdout and "leak.md" in r.stdout

    def test_outside_a_git_repository_warns_once_and_exits_0(self, repo):
        nogit = repo["tmp"] / "nogit"
        nogit.mkdir()
        r = _run(repo, cwd=nogit)
        assert r.returncode == 0
        assert r.stdout.startswith("WARN") and r.stdout.count("\n") == 1

    def test_default_list_lives_under_home_not_in_any_repo(self):
        block = _check_7_block()
        assert "$HOME/.config/tacsop/private-terms" in block
        assert "TACSOP_PRIVATE_TERMS" in block

    def test_quick_reference_names_the_check_as_blocking(self):
        assert re.search(r"^\| Private terms \|.*\| Block push \|$", PCC.read_text(encoding="utf-8"), re.M)


RULE_SURFACES = [
    ".claude/README.md",
    ".claude/agents/code-reviewer.md",
    ".claude/agents/proposer.md",
    ".claude/agents/decision-scientist.md",
]


class TestDestinationRule:
    @pytest.mark.parametrize("path", RULE_SURFACES)
    def test_surface_carries_the_rule_its_default_and_its_test(self, path):
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        assert "the repository that owns the sensitivity" in text
        assert "never into this repo's `docs/`" in text
        assert "git ls-files --error-unmatch" in text  # the test an agent can run
        assert "write to the scratchpad and name the owning repository" in text  # the default when unsure

    @pytest.mark.parametrize(
        "path",
        [".claude/README.md", ".claude/teams/feature-development.md", ".claude/teams/decision-science.md"],
    )
    def test_no_surface_sends_output_to_docs_unconditionally(self, path):
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        for line in text.splitlines():
            if re.search(r"write[s]? (?:a )?(?:proposal|findings|report)[^|]*to `docs/", line):
                assert "owning repository" in line or "Scope Matrix" in line, line
