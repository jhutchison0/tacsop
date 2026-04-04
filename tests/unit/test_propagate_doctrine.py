"""Tests for scripts/propagate_doctrine.py."""

import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the module directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import propagate_doctrine


# --- Fixtures ---


DOCTRINE_TWO_ENTRIES = """\
# Doctrine Updates

Header text here.

---

## 2026-03-26: Second Update

Second entry content.

### Details

More details here.

---

## 2026-03-24: First Update

First entry content.
"""

DOCTRINE_ONE_ENTRY = """\
# Doctrine Updates

Header text.

---

## 2026-03-26: Only Update

The only entry.
"""

DOCTRINE_NO_SEPARATOR = """\
# Doctrine Updates

Just a header with no --- separator.
"""

DOCTRINE_SEPARATOR_NO_HEADING = """\
# Doctrine Updates

---

Some content without a ## date heading.
"""


@pytest.fixture
def projects_dir(tmp_path):
    """Create a fake ~/projects directory structure."""
    return tmp_path / "projects"


def _make_repo(projects_dir, repo_name, with_commands=True, with_update=None):
    """Helper to create a fake repo directory."""
    repo = projects_dir / repo_name
    if with_commands:
        (repo / ".claude" / "commands").mkdir(parents=True)
    else:
        repo.mkdir(parents=True)
    if with_update is not None:
        (repo / ".claude" / "upstream-update.md").write_text(with_update)
    return repo


# --- extract_latest_entry ---


class TestExtractLatestEntry:
    def test_two_entries_returns_first(self, tmp_path):
        f = tmp_path / "doctrine.md"
        f.write_text(DOCTRINE_TWO_ENTRIES)
        result = propagate_doctrine.extract_latest_entry(f)
        assert result.startswith("## 2026-03-26: Second Update")
        assert "Second entry content." in result
        assert "First Update" not in result

    def test_one_entry_returns_it(self, tmp_path):
        f = tmp_path / "doctrine.md"
        f.write_text(DOCTRINE_ONE_ENTRY)
        result = propagate_doctrine.extract_latest_entry(f)
        assert "## 2026-03-26: Only Update" in result
        assert "The only entry." in result

    def test_missing_file_returns_none(self, tmp_path):
        f = tmp_path / "nonexistent.md"
        assert propagate_doctrine.extract_latest_entry(f) is None

    def test_no_separator_returns_none(self, tmp_path):
        f = tmp_path / "doctrine.md"
        f.write_text(DOCTRINE_NO_SEPARATOR)
        assert propagate_doctrine.extract_latest_entry(f) is None

    def test_separator_no_heading_returns_content(self, tmp_path):
        f = tmp_path / "doctrine.md"
        f.write_text(DOCTRINE_SEPARATOR_NO_HEADING)
        result = propagate_doctrine.extract_latest_entry(f)
        assert result == "Some content without a ## date heading."


# --- build_notification ---


class TestBuildNotification:
    def test_contains_header_and_entry(self):
        result = propagate_doctrine.build_notification("## 2026-03-26: Test\n\nBody.")
        assert "# Upstream Doctrine Update" in result
        assert "**Source**:" in result
        assert "**Action**:" in result
        assert "**Cleanup**:" in result
        assert "---" in result
        assert "## 2026-03-26: Test" in result
        assert "Body." in result


# --- find_downstream_repos ---


class TestFindDownstreamRepos:
    def test_finds_repos_with_claude_commands(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        repo_a = _make_repo(projects_dir, "gitlab/repo_a")
        repo_b = _make_repo(projects_dir, "gitlab/repo_b")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert repo_a in result
        assert repo_b in result
        assert utils not in result

    def test_skips_utils_itself(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert utils not in result

    def test_filters_nested_repos(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        parent = _make_repo(projects_dir, "gitlab/parent_repo")
        _make_repo(projects_dir, "gitlab/parent_repo/lib/nested_repo")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert parent in result
        assert len(result) == 1  # nested repo filtered out

    def test_no_repos_returns_empty(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert result == []


# --- propagate ---


class TestPropagate:
    @pytest.fixture
    def setup(self, projects_dir, monkeypatch):
        """Wire up a fake project tree with doctrine file and two repos."""
        utils = _make_repo(projects_dir, "github/utils")
        repo_a = _make_repo(projects_dir, "gitlab/repo_a")
        repo_b = _make_repo(projects_dir, "gitlab/repo_b")

        doctrine = utils / "docs" / "doctrine-updates.md"
        doctrine.parent.mkdir(parents=True)
        doctrine.write_text(DOCTRINE_ONE_ENTRY)

        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)
        monkeypatch.setattr(propagate_doctrine, "DOCTRINE_FILE", doctrine)

        return {"repos": [repo_a, repo_b], "doctrine": doctrine}

    def test_creates_new_notification(self, setup):
        propagate_doctrine.propagate(dry_run=False)

        for repo in setup["repos"]:
            target = repo / ".claude" / "upstream-update.md"
            assert target.exists()
            content = target.read_text()
            assert "# Upstream Doctrine Update" in content
            assert "## 2026-03-26: Only Update" in content

    def test_appends_to_existing(self, setup):
        existing_content = "# Upstream Doctrine Update\n\n---\n\n## 2026-03-24: Old\n\nOld content."
        repo = setup["repos"][0]
        (repo / ".claude" / "upstream-update.md").write_text(existing_content)

        propagate_doctrine.propagate(dry_run=False)

        content = (repo / ".claude" / "upstream-update.md").read_text()
        assert "## 2026-03-24: Old" in content
        assert "Old content." in content
        assert "## 2026-03-26: Only Update" in content
        # Verify separator between entries
        assert "\n\n---\n\n## 2026-03-26:" in content

    def test_dry_run_writes_nothing(self, setup, capsys):
        propagate_doctrine.propagate(dry_run=True)

        for repo in setup["repos"]:
            target = repo / ".claude" / "upstream-update.md"
            assert not target.exists()

        captured = capsys.readouterr()
        assert "[dry-run]" in captured.out
        assert "(new)" in captured.out

    def test_no_doctrine_file(self, projects_dir, monkeypatch, capsys):
        utils = _make_repo(projects_dir, "github/utils")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "UTILS_ROOT", utils)
        monkeypatch.setattr(
            propagate_doctrine, "DOCTRINE_FILE", projects_dir / "missing.md"
        )

        propagate_doctrine.propagate(dry_run=False)

        captured = capsys.readouterr()
        assert "No doctrine updates found." in captured.out
