"""Tests pinning the verifying-claims skill to its markable Standards.

The skill is prose, so these tests check shape, not judgment: the size caps,
the kernel's rule count, one probe per claim type, and one example per
incident shape (CONOP OVERWATCH, Wave 2). Whether a rule is well worded is a
reviewer's call and stays out of this file.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / ".claude" / "skills" / "verifying-claims"
SKILL = SKILL_DIR / "SKILL.md"


def _frontmatter(text: str) -> dict[str, str]:
    block = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
    return dict(line.split(": ", 1) for line in block.splitlines())


def test_skill_is_directory_form_with_frontmatter():
    meta = _frontmatter(SKILL.read_text())
    assert meta["name"] == SKILL_DIR.name
    assert meta["description"]
    assert meta["version"]


def test_skill_md_is_under_110_lines():
    assert len(SKILL.read_text().splitlines()) < 110


def _section(text: str, heading: str) -> str:
    """The body under a `## heading`, up to the next `## ` or the end."""
    match = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    assert match, f"no '## {heading}' section"
    return match.group(1)


def _numbered_rules(section: str) -> list[str]:
    return re.findall(r"^\d+\. (.+)$", section, re.M)


def test_kernel_has_at_most_six_rules():
    rules = _numbered_rules(_section(SKILL.read_text(), "The Kernel"))
    assert 1 <= len(rules) <= 6


def test_kernel_carries_the_decided_terms():
    """D2: four states, the Evidence line, UNVERIFIED. D10: clean tree, read-only probes."""
    kernel = "\n".join(_numbered_rules(_section(SKILL.read_text(), "The Kernel")))
    for term in (
        "written, tested, deployed, or observed",
        "this turn",
        "`Evidence:`",
        "`UNVERIFIED: <blocker>`",
        "`git status --porcelain`",
        "never write",
        "an absence is a claim",
    ):
        assert term in kernel, f"kernel lost {term!r}"


def _table_rows(section: str) -> list[list[str]]:
    """Body rows of the first markdown table in a section, as stripped cells."""
    lines = [line for line in section.splitlines() if line.startswith("|")]
    return [[cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:]]


CLAIM_TYPES = ("run landed", "pushed", "mirror synced", "tests pass", "venv exists", "merged", "deployed")


def test_probe_table_has_one_probe_per_claim_type():
    rows = _table_rows(_section(SKILL.read_text(), "Probes"))
    claims = [row[0].lower() for row in rows]
    for claim_type in CLAIM_TYPES:
        assert sum(claim_type in claim for claim in claims) == 1, f"want one row for {claim_type!r}"
    assert len(rows) == len(CLAIM_TYPES)
    for row in rows:
        assert "`" in row[2], f"row {row[0]!r} names no command"


EXAMPLES = SKILL_DIR / "EXAMPLES.md"


def _pairs() -> list[str]:
    """The bodies of the numbered `## N. title` sections of EXAMPLES.md."""
    return re.findall(r"^## \d+\. [^\n]*\n(.*?)(?=^## |\Z)", EXAMPLES.read_text(), re.S | re.M)


def test_examples_hold_seven_pairs():
    """Six incident shapes plus the plan's own line-count slip."""
    assert len(_pairs()) == 7


def test_each_example_shows_a_before_and_an_evidenced_after():
    for number, pair in enumerate(_pairs(), start=1):
        before, _, after = pair.partition("**After**")
        assert "**Before**" in before, f"pair {number} has no Before"
        assert after, f"pair {number} has no After"
        assert "Evidence:" in after or "UNVERIFIED:" in after, f"pair {number}'s After shows no evidence"
        assert "Evidence:" not in before and "UNVERIFIED:" not in before


def test_examples_show_a_clean_report():
    """The counterweight: a report that needs no added line, so the pairs do not teach over-flagging."""
    clean = _section(EXAMPLES.read_text(), "A clean report")
    assert "**Before**" not in clean
    assert "Evidence:" not in clean.split("\n\n")[0] and "UNVERIFIED:" not in clean.split("\n\n")[0]


CLAUDE_MD = ROOT / "CLAUDE.md"


def test_claude_md_carries_the_kernel_verbatim():
    """The ambient copy and the skill's kernel are one text in two places."""
    ambient = _numbered_rules(_section(CLAUDE_MD.read_text(), "Claim Style"))
    assert ambient == _numbered_rules(_section(SKILL.read_text(), "The Kernel"))


@pytest.mark.parametrize(
    ("path", "needle"),
    [
        (".claude/skills/SKILLS_FRAMEWORK.md", "### verifying-claims (directory form)"),
        (".claude/skills/SKILLS_FRAMEWORK.md", "├── verifying-claims/"),
        (".claude/README.md", "verifying-claims/SKILL.md + 1 sidecar"),
        (".claude/agents/code-reviewer.md", "`.claude/skills/verifying-claims/SKILL.md`"),
    ],
)
def test_skill_is_registered(path, needle):
    assert needle in (ROOT / path).read_text()
