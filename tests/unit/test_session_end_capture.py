"""Tests pinning the two capture points /session-end must keep.

Two WHETSTONE instruments depend on /session-end asking for them: the
`KB-graph:` line (uptake metric M1) and Step 5.5, the upward lesson channel.
An edit that drops either ask would silence a metric and fail nothing else.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSION_END = ROOT / ".claude" / "commands" / "session-end.md"
FORMAT = ROOT / "docs" / "session-doc-format.md"
TRAVERSAL = ROOT / ".claude" / "skills" / "traversing-the-knowledge-base" / "SKILL.md"


def _kb_graph_format() -> str:
    """The line format as the traversal skill defines it, the one source."""
    return re.search(r"^KB-graph: <.+>$", TRAVERSAL.read_text(), re.M).group(0)


def test_session_end_asks_for_the_kb_graph_line():
    assert f"`{_kb_graph_format()}`" in SESSION_END.read_text()


def test_session_doc_format_shows_the_kb_graph_line():
    assert f"`{_kb_graph_format()}`" in FORMAT.read_text()


def test_session_end_carries_the_upward_lesson_step():
    text = SESSION_END.read_text()
    assert "LESSON (OBSERVED): " in text
    assert "scope: fleet" in text
    assert "`.claude/upstream-lesson.md`" in text
    steps = [text.index(f"## Step {n}: ") for n in ("5", "5.5", "6")]
    assert steps == sorted(steps), "Step 5.5 sits between Step 5 and Step 6"
