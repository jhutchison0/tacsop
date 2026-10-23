"""Every Level 0 skill's frontmatter parses as YAML and carries its version.

Since 2026-10-22 the frontmatter `version:` field is the only place a skill's
number lives (the bodies lost their version histories), so a frontmatter that
strict YAML rejects would lose the number to any reader stricter than Claude
Code's own parser. Two skills failed this on the day the test was written: an
unquoted description with a `: ` inside it.
"""

from pathlib import Path

import pytest
import yaml

SKILLS = sorted((Path(__file__).resolve().parents[2] / ".claude" / "skills").glob("*/SKILL.md"))


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no frontmatter"
    block = text.split("\n---\n", 1)[0][4:]
    return yaml.safe_load(block)


@pytest.mark.parametrize("skill", SKILLS, ids=[p.parent.name for p in SKILLS])
def test_frontmatter_parses_and_carries_name_description_version(skill):
    data = _frontmatter(skill)
    assert data["name"] == skill.parent.name
    assert isinstance(data["description"], str) and data["description"].strip()
    assert isinstance(data["version"], str) and data["version"].count(".") == 2


def test_at_least_one_skill_is_checked():
    assert len(SKILLS) >= 1
