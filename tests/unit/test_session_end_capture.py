"""Tests pinning the capture point /session-end must keep.

WHETSTONE's uptake metric M1 counts `KB-graph:` lines in session docs, and
/session-end is where an author is asked for one. An edit that drops the ask
would silence the metric and fail nothing else.
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


def _step5() -> str:
    return re.search(r"^## Step 5: .*?(?=^## Step 6)", SESSION_END.read_text(), re.S | re.M).group(0)


def test_session_end_asks_for_the_kb_graph_line():
    """In Step 5, where the session doc is written, and as an instruction to record."""
    ask = (
        "- If a traversal informed the session's work, record it in Work Completed as a "
        f"`{_kb_graph_format()}` line, in the sub-topic it informed."
    )
    assert ask in _step5()


def test_session_doc_format_shows_the_kb_graph_line():
    assert f"`{_kb_graph_format()}`" in FORMAT.read_text()


def test_format_puts_the_kb_graph_line_inside_a_sub_topic():
    """Above the edit it led to: the M3 check reads the record's order."""
    text = FORMAT.read_text()
    line = text.index(f"`{_kb_graph_format()}`")
    assert text.index("### 1. <Sub-topic>") < line < text.index("[What was done, why, what files changed.]")
