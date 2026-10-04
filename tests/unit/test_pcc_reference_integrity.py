"""Tests for /pcc check 5's file pass, run as shipped.

The bash block is extracted from .claude/commands/pcc.md and run in a scratch tree,
so a test measures the text a reader copies, not a paraphrase of it.
"""

import re
import subprocess
from pathlib import Path

PCC = Path(__file__).resolve().parents[2] / ".claude" / "commands" / "pcc.md"


def _file_pass() -> str:
    text = PCC.read_text(encoding="utf-8")
    section = re.search(r"^### 5\. Reference Integrity.*?(?=^### |^## )", text, re.S | re.M)
    return re.findall(r"^```bash\n(.*?)^```$", section.group(0), re.S | re.M)[0]


def _run(tmp_path: Path, tasks: str) -> str:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "tasks.md").write_text(tasks)
    result = subprocess.run(
        ["bash", "-c", _file_pass()], cwd=tmp_path, capture_output=True, text=True
    )
    return result.stdout


def test_a_missing_path_in_the_focus_section_is_reported(tmp_path):
    # The Focus section sits above Active and is the first thing an agent reads.
    tasks = "# Task Tracker\n\n## Focus\n\n1. Read `docs/absent.md` first.\n\n## Active\n\n## Completed\n"
    assert _run(tmp_path, tasks) == "MISSING: docs/absent.md\n"


def test_a_missing_path_in_the_active_section_is_reported(tmp_path):
    tasks = "# Task Tracker\n\n## Active\n\n- [ ] Fix `docs/absent.md`.\n\n## Completed\n"
    assert _run(tmp_path, tasks) == "MISSING: docs/absent.md\n"


def test_the_completed_section_is_not_scanned(tmp_path):
    # Completed lines are records; a file they name may be gone by design.
    tasks = "# Task Tracker\n\n## Active\n\n## Completed\n\n- [x] Removed `docs/gone.md`.\n"
    assert _run(tmp_path, tasks) == ""
