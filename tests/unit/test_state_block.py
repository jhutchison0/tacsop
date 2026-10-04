"""Slice 2 of the common operating picture: no maintained surface states the repo's state.

config/project.yaml holds identity. The campaign focus is intent and lives at the head
of docs/tasks.md; known unknowns live in docs/gaps.md; the last session is the newest
file in docs/sessions/. A number that drifts is measured by command when it is needed,
never kept in an orientation surface, because a kept number reads as current after it
stops being true (README.md said "189 tests" when the suite ran 491).
"""

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]

# The surfaces that wrote, read, or pointed readers at the state block.
SURFACES = [
    ".claude/commands/session-end.md",
    ".claude/commands/session-start.md",
    ".claude/commands/sitrep.md",
    ".claude/README.md",
    "CONTEXT.md",
    ".claude/skills/maintaining-project-context/SKILL.md",
]

# The files an agent reads first (the /pcc check 5 set, less the task list).
ORIENTATION = ["CLAUDE.md", "CONTEXT.md", "README.md", "LANGUAGE.md", ".claude/README.md"]

# A count of something that drifts. "Level 0 agents" names a tier, not a count.
DRIFTING_COUNT = re.compile(r"(?<!Level )\b\d+ (tests?|repos?|consumers?|agents?)\b")

TAG = re.compile(r"\[(measured|identity|record|intent|register): [^\]]+\]")


def test_the_config_has_no_state_block():
    config = yaml.safe_load((REPO / "config" / "project.yaml").read_text())
    assert "state" not in config


@pytest.mark.parametrize("surface", SURFACES)
def test_no_surface_names_a_state_block_key(surface):
    text = (REPO / surface).read_text()
    assert [key for key in ("active_work", "last_session") if key in text] == []


def test_the_focus_lives_at_the_head_of_the_task_list():
    text = (REPO / "docs" / "tasks.md").read_text()
    focus = re.search(r"^## Focus\n(.*?)^## Active", text, re.S | re.M)
    assert focus, "docs/tasks.md has no ## Focus section before ## Active"
    assert focus.group(1).strip()
    assert "## Focus" in (REPO / ".claude" / "commands" / "session-end.md").read_text()


def test_every_session_start_summary_line_says_where_it_came_from():
    text = (REPO / ".claude" / "commands" / "session-start.md").read_text()
    step5 = re.search(r"^## Step 5: .*?(?=^---)", text, re.S | re.M).group(0)
    items = re.findall(r"^\d+\. \*\*.*$", step5, re.M)
    assert items
    assert [item for item in items if not TAG.search(item)] == []


@pytest.mark.parametrize("surface", ORIENTATION)
def test_no_orientation_surface_keeps_a_drifting_count(surface):
    assert DRIFTING_COUNT.findall((REPO / surface).read_text()) == []
