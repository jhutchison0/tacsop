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


def _run_hook(repo: Path, edited: Path) -> str:
    payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(edited)}})
    result = subprocess.run(["bash", str(HOOK)], input=payload, text=True, capture_output=True)
    assert result.returncode == 0, "the hook must exit 0 on every path"
    log = repo / ".claude" / "audits" / "shift-left-violations.log"
    return log.read_text() if log.exists() else ""


@pytest.mark.parametrize(
    "line",
    [
        "from myproject.widgets import thing\n",
        "import myproject.widgets\n",
        "from myproject import widgets\n",
        "from myproject import thing, widgets\n",
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
