"""Characterization tests for .claude/hooks/post-tool-shift-left-audit.sh.

The hook is bash, so these tests drive it the way the harness does: a JSON
payload on stdin, then read the audit log it appends to. Each test builds a
throwaway git repo because the hook resolves the project root with
`git rev-parse`.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "post-tool-shift-left-audit.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("jq") is None or shutil.which("git") is None,
    reason="the hook needs jq and git on PATH",
)


def _repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "src" / "myproject").mkdir(parents=True)
    (tmp_path / "src" / "myproject" / "widgets.py").write_text("def thing():\n    return 1\n")
    (tmp_path / "tests" / "unit").mkdir(parents=True)
    return tmp_path


def _run_hook_result(edited: Path) -> subprocess.CompletedProcess:
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(edited)}})
    return subprocess.run(["bash", str(HOOK)], input=payload, text=True, capture_output=True)


def _run_hook(repo: Path, edited: Path) -> str:
    result = _run_hook_result(edited)
    assert result.returncode == 0, "the hook must exit 0 on every path"
    log = repo / ".claude" / "audits" / "shift-left-violations.log"
    return log.read_text() if log.exists() else ""


# The warning's channel. Claude never sees stderr from a hook that exits 0, and a
# PostToolUse hook cannot undo a write, so the warning travels as one JSON object
# on stdout: `hookSpecificOutput.additionalContext` for the agent, `systemMessage`
# for the user (hooks reference, "Exit code 0" and "PostToolUse decision control",
# read 2026-10-22). Until then the hook wrote to stderr, which reached nobody.


def test_missing_partner_sends_the_warning_as_additional_context(tmp_path):
    repo = _repo(tmp_path)
    result = _run_hook_result(repo / "src" / "myproject" / "widgets.py")
    assert result.returncode == 0
    out = json.loads(result.stdout)  # one JSON object and nothing else on stdout
    specific = out["hookSpecificOutput"]
    assert specific["hookEventName"] == "PostToolUse"
    assert "No test partner" in specific["additionalContext"]
    assert "tests/**/test_widgets.py" in specific["additionalContext"]


def test_missing_partner_tells_the_user_too(tmp_path):
    repo = _repo(tmp_path)
    result = _run_hook_result(repo / "src" / "myproject" / "widgets.py")
    out = json.loads(result.stdout)
    assert "widgets.py" in out["systemMessage"]


def test_missing_partner_writes_nothing_to_stderr(tmp_path):
    repo = _repo(tmp_path)
    result = _run_hook_result(repo / "src" / "myproject" / "widgets.py")
    assert result.stderr == ""


def test_found_partner_prints_nothing(tmp_path):
    repo = _repo(tmp_path)
    (repo / "tests" / "unit" / "test_widgets.py").write_text("import pytest\n")
    result = _run_hook_result(repo / "src" / "myproject" / "widgets.py")
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


@pytest.mark.parametrize(
    "line",
    [
        "from myproject.widgets import thing\n",
        "import myproject.widgets\n",
        "from myproject import widgets\n",
        "from myproject import thing, widgets\n",
        # Tests in a repo laid out like the template import with the src. prefix
        # (agent-eval, 2026-10-06: 53 such imports, 0 bare, so the fallback never fired).
        "from src.myproject.widgets import thing\n",
        "import src.myproject.widgets\n",
        "from src.myproject import widgets\n",
    ],
)
def test_feature_named_test_that_imports_the_module_counts_as_partner(tmp_path, line):
    repo = _repo(tmp_path)
    (repo / "tests" / "unit" / "test_feature.py").write_text(line)
    log = _run_hook(repo, repo / "src" / "myproject" / "widgets.py")
    assert "OK_TEST_EXISTS" in log
    assert "test_feature.py" in log
    assert "MISSING_TEST" not in log


@pytest.mark.parametrize(
    "line",
    [
        "from myproject.other import thing\n",
        "from myproject import widgetsx\n",
        "import myproject.widgets_extra\n",
        "import myprojectXwidgets\n",
    ],
)
def test_module_nobody_imports_still_logs_missing(tmp_path, line):
    repo = _repo(tmp_path)
    (repo / "tests" / "unit" / "test_feature.py").write_text(line)
    log = _run_hook(repo, repo / "src" / "myproject" / "widgets.py")
    assert "MISSING_TEST" in log
    assert "OK_TEST_EXISTS" not in log


def test_name_matched_partner_still_wins(tmp_path):
    repo = _repo(tmp_path)
    (repo / "tests" / "unit" / "test_widgets.py").write_text("import pytest\n")
    log = _run_hook(repo, repo / "src" / "myproject" / "widgets.py")
    assert "OK_TEST_EXISTS" in log
    assert "test_widgets.py" in log
