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
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert repo_a in result
        assert repo_b in result
        assert utils not in result

    def test_skips_utils_itself(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert utils not in result

    def test_filters_nested_repos(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        parent = _make_repo(projects_dir, "gitlab/parent_repo")
        _make_repo(projects_dir, "gitlab/parent_repo/lib/nested_repo")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)

        result = propagate_doctrine.find_downstream_repos()
        assert parent in result
        assert len(result) == 1  # nested repo filtered out

    def test_no_repos_returns_empty(self, projects_dir, monkeypatch):
        utils = _make_repo(projects_dir, "github/utils")
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)

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
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)
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
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", utils)
        monkeypatch.setattr(
            propagate_doctrine, "DOCTRINE_FILE", projects_dir / "missing.md"
        )

        propagate_doctrine.propagate(dry_run=False)

        captured = capsys.readouterr()
        assert "No doctrine updates found." in captured.out


class TestExtractEntries:
    def test_returns_every_entry_newest_first_with_its_date(self, tmp_path):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(DOCTRINE_TWO_ENTRIES)

        entries = propagate_doctrine.extract_entries(doctrine)

        assert [date for date, _ in entries] == ["2026-03-26", "2026-03-24"]
        assert entries[0][1].startswith("## 2026-03-26: Second Update")
        assert entries[0][1].endswith("More details here.")  # no trailing separator
        assert entries[1][1].startswith("## 2026-03-24: First Update")

    def test_missing_file_has_no_entries(self, tmp_path):
        assert propagate_doctrine.extract_entries(tmp_path / "missing.md") == []

    def test_one_entry(self, tmp_path):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(DOCTRINE_ONE_ENTRY)

        assert propagate_doctrine.extract_entries(doctrine) == [
            ("2026-03-26", "## 2026-03-26: Only Update\n\nThe only entry.")
        ]

    def test_no_separator_has_no_entries(self, tmp_path):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(DOCTRINE_NO_SEPARATOR)

        assert propagate_doctrine.extract_entries(doctrine) == []

    def test_undated_text_is_not_an_entry(self, tmp_path):
        # A delivery mark compares dates, so text with no dated heading cannot be one.
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(DOCTRINE_SEPARATOR_NO_HEADING)

        assert propagate_doctrine.extract_entries(doctrine) == []


ENTRIES = [  # newest first, as extract_entries returns them
    ("2026-09-18", "## 2026-09-18: C\n\nc"),
    ("2026-08-30", "## 2026-08-30: B\n\nb"),
    ("2026-08-21", "## 2026-08-21: A\n\na"),
]


def _dates(entries):
    return [date for date, _ in entries]


class TestEntriesToDeliver:
    def test_with_a_mark_delivers_everything_newer_oldest_first(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark="2026-08-21", since=None, existing="")
        assert _dates(got) == ["2026-08-30", "2026-09-18"]

    def test_with_no_mark_and_a_since_date_delivers_from_that_date(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark=None, since="2026-08-30", existing="")
        assert _dates(got) == ["2026-08-30", "2026-09-18"]

    def test_with_no_mark_and_no_since_delivers_the_newest_only(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark=None, since=None, existing="")
        assert _dates(got) == ["2026-09-18"]

    def test_a_mark_wins_over_since(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark="2026-08-30", since="2026-08-21", existing="")
        assert _dates(got) == ["2026-09-18"]

    def test_skips_entries_already_in_the_unread_notification(self):
        existing = "# Upstream Doctrine Update\n\n---\n\n## 2026-08-30: B\n\nb"
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark=None, since="2026-08-21", existing=existing)
        assert _dates(got) == ["2026-08-21", "2026-09-18"]

    def test_a_consumer_at_the_newest_mark_gets_nothing(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, mark="2026-09-18", since=None, existing="")
        assert got == []


class TestPropagateBacklog:
    @pytest.fixture
    def consumer(self, projects_dir, monkeypatch):
        hub = _make_repo(projects_dir, "github/hub")
        repo = _make_repo(projects_dir, "github/consumer")
        doctrine = hub / "docs" / "doctrine-updates.md"
        doctrine.parent.mkdir(parents=True)
        doctrine.write_text(DOCTRINE_TWO_ENTRIES)
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", hub)
        monkeypatch.setattr(propagate_doctrine, "DOCTRINE_FILE", doctrine)
        return repo

    def test_since_delivers_the_backlog_oldest_first_and_writes_the_mark(self, consumer):
        propagate_doctrine.propagate(dry_run=False, since="2026-03-24")

        text = (consumer / ".claude" / "upstream-update.md").read_text()
        assert text.index("## 2026-03-24: First Update") < text.index("## 2026-03-26: Second Update")
        assert (consumer / ".claude" / "doctrine-delivered").read_text().strip() == "2026-03-26"

    def test_a_second_run_delivers_nothing_new(self, consumer, capsys):
        propagate_doctrine.propagate(dry_run=False, since="2026-03-24")
        first = (consumer / ".claude" / "upstream-update.md").read_text()
        capsys.readouterr()

        propagate_doctrine.propagate(dry_run=False)

        assert (consumer / ".claude" / "upstream-update.md").read_text() == first
        assert "Up to date" in capsys.readouterr().out

    def test_a_reviewed_and_deleted_notification_is_not_resent(self, consumer):
        # The consumer reads the backlog and deletes the file; the mark remembers.
        propagate_doctrine.propagate(dry_run=False, since="2026-03-24")
        (consumer / ".claude" / "upstream-update.md").unlink()

        propagate_doctrine.propagate(dry_run=False, since="2026-03-24")

        assert not (consumer / ".claude" / "upstream-update.md").exists()

    def test_a_marked_consumer_gets_only_newer_entries(self, consumer):
        (consumer / ".claude" / "doctrine-delivered").write_text("2026-03-24\n")

        propagate_doctrine.propagate(dry_run=False, since="2026-03-01")

        text = (consumer / ".claude" / "upstream-update.md").read_text()
        assert "## 2026-03-26: Second Update" in text
        assert "## 2026-03-24: First Update" not in text

    def test_dry_run_names_what_each_consumer_would_get_and_writes_nothing(self, consumer, capsys):
        propagate_doctrine.propagate(dry_run=True, since="2026-03-24")

        assert not (consumer / ".claude" / "doctrine-delivered").exists()
        assert not (consumer / ".claude" / "upstream-update.md").exists()
        out = capsys.readouterr().out
        assert "2026-03-24" in out
        assert "2026-03-26" in out


class TestMain:
    def test_since_and_dry_run_reach_propagate(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            propagate_doctrine, "propagate", lambda dry_run, since: calls.append((dry_run, since))
        )

        assert propagate_doctrine.main(["--dry-run", "--since", "2026-08-21"]) == 0
        assert calls == [(True, "2026-08-21")]

    @pytest.mark.parametrize("bad", ["2026-8-21", "21-08-2026", "2026-13-01", "yesterday"])
    def test_a_malformed_since_date_is_refused(self, bad, monkeypatch, capsys):
        monkeypatch.setattr(propagate_doctrine, "propagate", lambda **_: pytest.fail("ran"))

        with pytest.raises(SystemExit) as exc:
            propagate_doctrine.main(["--since", bad])

        assert exc.value.code == 2
