"""Tests for scripts/propagate_doctrine.py."""

import os
import re
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

    def _exclude(self, setup, *paths):
        config = setup["doctrine"].parents[1] / "config" / "project.yaml"
        config.parent.mkdir(parents=True)
        config.write_text("propagation:\n  exclude:\n" + "".join(f"    - {p}\n" for p in paths))

    def test_an_excluded_repo_gets_no_notification_and_no_mark(self, setup, capsys):
        # A mirror the hub must never write into is still discovered; the run
        # names it as skipped, so the exclusion is visible, and writes nothing.
        self._exclude(setup, "gitlab/repo_b")
        repo_a, repo_b = setup["repos"]

        propagate_doctrine.propagate(dry_run=False)

        assert (repo_a / ".claude" / "upstream-update.md").exists()
        assert not (repo_b / ".claude" / "upstream-update.md").exists()
        assert not (repo_b / ".claude" / "doctrine-delivered").exists()
        out = capsys.readouterr().out
        assert "[skip] gitlab/repo_b: excluded by config/project.yaml propagation.exclude" in out

    def test_a_dry_run_names_an_excluded_repo_as_skipped(self, setup, capsys):
        self._exclude(setup, "gitlab/repo_b")

        propagate_doctrine.propagate(dry_run=True)

        out = capsys.readouterr().out
        assert "[skip] gitlab/repo_b: excluded by config/project.yaml propagation.exclude" in out
        assert "[dry-run] gitlab/repo_b" not in out
        assert "[dry-run] gitlab/repo_a" in out

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
    def test_with_a_mark_delivers_every_entry_not_held_oldest_first(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held={"## 2026-08-21: A"}, since=None, existing="")
        assert _dates(got) == ["2026-08-30", "2026-09-18"]

    def test_with_no_mark_and_a_since_date_delivers_from_that_date(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held=None, since="2026-08-30", existing="")
        assert _dates(got) == ["2026-08-30", "2026-09-18"]

    def test_with_no_mark_and_no_since_delivers_the_newest_only(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held=None, since=None, existing="")
        assert _dates(got) == ["2026-09-18"]

    def test_a_mark_wins_over_since(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held={"## 2026-08-30: B", "## 2026-08-21: A"}, since="2026-08-21", existing="")
        assert _dates(got) == ["2026-09-18"]

    def test_skips_entries_already_in_the_unread_notification(self):
        existing = "# Upstream Doctrine Update\n\n---\n\n## 2026-08-30: B\n\nb"
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held=None, since="2026-08-21", existing=existing)
        assert _dates(got) == ["2026-08-21", "2026-09-18"]

    def test_a_consumer_at_the_newest_mark_gets_nothing(self):
        got = propagate_doctrine.entries_to_deliver(ENTRIES, held={h for h in ("## 2026-09-18: C", "## 2026-08-30: B", "## 2026-08-21: A")}, since=None, existing="")
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
        assert _mark(consumer) == {"## 2026-03-26: Second Update", "## 2026-03-24: First Update"}

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
        (consumer / ".claude" / "doctrine-delivered").write_text("## 2026-03-24: First Update\n")

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


def _mark(repo):
    mark = repo / ".claude" / "doctrine-delivered"
    return {line for line in mark.read_text().splitlines() if line} if mark.exists() else None


def _note(repo):
    note = repo / ".claude" / "upstream-update.md"
    return note.read_text() if note.exists() else ""


def _doc(*entries):
    """A doctrine file with (date, subject) entries, newest first as given."""
    body = "\n\n---\n\n".join(f"## {d}: {subject}\n\n{subject} body." for d, subject in entries)
    return f"# Doctrine Updates\n\nHeader.\n\n---\n\n{body}\n"


class TestHeadingMark:
    """The mark is the set of entry headings a repo has been offered; it never shrinks."""

    @pytest.fixture
    def world(self, projects_dir, monkeypatch):
        hub = _make_repo(projects_dir, "github/hub")
        repo = _make_repo(projects_dir, "github/consumer")
        doctrine = hub / "docs" / "doctrine-updates.md"
        doctrine.parent.mkdir(parents=True)
        monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
        monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", hub)
        monkeypatch.setattr(propagate_doctrine, "DOCTRINE_FILE", doctrine)
        return doctrine, repo

    def test_a_second_entry_written_the_same_day_still_ships(self, world):
        doctrine, repo = world
        doctrine.write_text(_doc(("2026-10-01", "X")))
        propagate_doctrine.propagate()
        (repo / ".claude" / "upstream-update.md").unlink()  # reviewed
        doctrine.write_text(_doc(("2026-10-01", "Y"), ("2026-10-01", "X")))

        propagate_doctrine.propagate()

        assert "## 2026-10-01: Y" in _note(repo)
        assert "## 2026-10-01: X" not in _note(repo)

    def test_an_entry_inserted_below_the_top_still_ships(self, world):
        doctrine, repo = world
        doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-08-21", "A")))
        propagate_doctrine.propagate(since="2026-08-21")
        (repo / ".claude" / "upstream-update.md").unlink()
        doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-09-10", "Late"), ("2026-08-21", "A")))

        propagate_doctrine.propagate()

        assert _note(repo).count("## 20") == 1
        assert "## 2026-09-10: Late" in _note(repo)

    def test_a_run_from_an_older_checkout_never_shrinks_the_mark(self, world):
        doctrine, repo = world
        doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-08-30", "B")))
        propagate_doctrine.propagate(since="2026-08-30")
        (repo / ".claude" / "upstream-update.md").unlink()
        doctrine.write_text(_doc(("2026-08-30", "B")))  # an older hub checkout
        propagate_doctrine.propagate()
        doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-08-30", "B")))  # back on main

        propagate_doctrine.propagate()

        assert _note(repo) == ""
        assert _mark(repo) == {"## 2026-09-18: C", "## 2026-08-30: B"}

    def test_the_newest_entry_skipped_as_unread_is_not_resent_after_review(self, world):
        doctrine, repo = world
        doctrine.write_text(_doc(("2026-03-26", "Second"), ("2026-03-24", "First")))
        (repo / ".claude" / "upstream-update.md").write_text("# U\n\n---\n\n## 2026-03-26: Second\n\nSecond body.\n")
        propagate_doctrine.propagate(since="2026-03-24")
        (repo / ".claude" / "upstream-update.md").unlink()

        propagate_doctrine.propagate()

        assert _note(repo) == ""

    @pytest.mark.parametrize("bad", ["garbage\n", "2026-08-21\n", "\ufeff## 2026-08-21: A\n", "<<<<<<< HEAD\n## 2026-08-21: A\n", "\n"])
    def test_a_malformed_mark_is_refused_and_left_untouched(self, world, bad, capsys):
        doctrine, repo = world
        doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-08-21", "A")))
        mark = repo / ".claude" / "doctrine-delivered"
        mark.write_text(bad)

        failures = propagate_doctrine.propagate()

        assert failures == 1
        assert mark.read_text() == bad
        assert _note(repo) == ""
        assert "FAILED github/consumer" in capsys.readouterr().out


FENCED_EXAMPLE = """\
# Doctrine Updates

Header.

---

## 2026-10-01: X about reverts

Mark a reverted entry like this:

```markdown
## 2026-10-05: REVERT, Old subject
```

End of X.

---

## 2026-09-18: C

c body.
"""


class TestParsing:
    def test_a_dated_heading_inside_a_code_fence_does_not_split_the_entry(self, tmp_path):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(FENCED_EXAMPLE)

        entries = propagate_doctrine.extract_entries(doctrine)

        assert [date for date, _ in entries] == ["2026-10-01", "2026-09-18"]
        assert entries[0][1].endswith("End of X.")

    @pytest.mark.parametrize("typo", ["## 2026-10-01 - Dash not colon", "## 2026-10-1: Short day", "## Untitled"])
    def test_an_undated_top_level_heading_stops_the_run_and_names_the_line(self, tmp_path, typo):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(FENCED_EXAMPLE.replace("## 2026-10-01: X about reverts", typo))

        with pytest.raises(ValueError, match=re.escape(typo)):
            propagate_doctrine.extract_entries(doctrine)

    def test_a_fenced_heading_in_an_unread_notification_is_not_unread(self):
        existing = "# U\n\n---\n\n## 2026-08-21: A\n\n```\n## 2026-09-18: C\n```\n"

        got = propagate_doctrine.entries_to_deliver(ENTRIES, held=None, since="2026-08-21", existing=existing)

        assert _dates(got) == ["2026-08-30", "2026-09-18"]

    def test_the_hubs_own_doctrine_file_parses(self):
        # Read-only: a malformed heading in the real file fails here, before any run.
        entries = propagate_doctrine.extract_entries(propagate_doctrine.DOCTRINE_FILE)

        assert entries
        assert [d for d, _ in entries] == sorted((d for d, _ in entries), reverse=True)

    def test_main_reports_a_refused_doctrine_file_and_exits_1(self, tmp_path, monkeypatch, capsys):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(FENCED_EXAMPLE.replace("## 2026-09-18: C", "## Untitled"))
        monkeypatch.setattr(propagate_doctrine, "DOCTRINE_FILE", doctrine)

        assert propagate_doctrine.main(["--dry-run"]) == 1
        assert "## Untitled" in capsys.readouterr().out


def test_a_fenced_copy_of_a_real_heading_does_not_split_the_entry(tmp_path):
    # An entry quoting another entry's exact heading inside a fence.
    doctrine = tmp_path / "doctrine-updates.md"
    doctrine.write_text(FENCED_EXAMPLE.replace("## 2026-10-05: REVERT, Old subject", "## 2026-09-18: C"))

    entries = propagate_doctrine.extract_entries(doctrine)

    assert [date for date, _ in entries] == ["2026-10-01", "2026-09-18"]
    assert entries[0][1].endswith("End of X.")


@pytest.fixture
def fleet(projects_dir, monkeypatch):
    """A hub with two entries and three consumer repos."""
    hub = _make_repo(projects_dir, "github/hub")
    repos = [_make_repo(projects_dir, f"github/c{i}") for i in (1, 2, 3)]
    doctrine = hub / "docs" / "doctrine-updates.md"
    doctrine.parent.mkdir(parents=True)
    doctrine.write_text(_doc(("2026-09-18", "C"), ("2026-08-21", "A")))
    monkeypatch.setattr(propagate_doctrine, "PROJECTS_DIR", projects_dir)
    monkeypatch.setattr(propagate_doctrine, "TACSOP_ROOT", hub)
    monkeypatch.setattr(propagate_doctrine, "DOCTRINE_FILE", doctrine)
    return repos


needs_unix_permissions = pytest.mark.skipif(
    os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0),
    reason="needs file permissions a non-root POSIX user cannot bypass",
)


def test_a_since_after_the_newest_entry_refuses_the_whole_run(fleet, capsys):
    # A typo (10-18 for 08-18) would otherwise mark every repo delivered and send nothing.
    assert propagate_doctrine.main(["--since", "2026-10-18"]) == 1

    assert "after the newest entry" in capsys.readouterr().out
    assert all(_mark(repo) is None and _note(repo) == "" for repo in fleet)


@needs_unix_permissions
def test_a_failed_notification_write_leaves_no_mark(fleet):
    note = fleet[0] / ".claude" / "upstream-update.md"
    note.write_text("# U\n\n---\n\n## 2026-03-01: Old\n\nold\n")
    note.chmod(0o444)
    try:
        propagate_doctrine.propagate()
    finally:
        note.chmod(0o644)

    assert _mark(fleet[0]) is None


@needs_unix_permissions
def test_one_failing_repo_does_not_stop_the_rest(fleet, capsys):
    note = fleet[1] / ".claude" / "upstream-update.md"
    note.write_text("# U\n\n---\n\n## 2026-03-01: Old\n\nold\n")
    note.chmod(0o444)
    try:
        code = propagate_doctrine.main(["--since", "2026-08-21"])
    finally:
        note.chmod(0o644)

    assert code == 1
    assert "FAILED github/c2" in capsys.readouterr().out
    for repo in (fleet[0], fleet[2]):
        assert "## 2026-08-21: A" in _note(repo)
        assert _mark(repo) == {"## 2026-09-18: C", "## 2026-08-21: A"}


class TestRound2:
    def test_a_repeated_heading_stops_the_run_and_names_it(self, tmp_path):
        # A heading is an entry's identity; a second "Errata" would never ship.
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(_doc(("2026-10-01", "Errata"), ("2026-10-01", "Errata")))

        with pytest.raises(ValueError, match="## 2026-10-01: Errata"):
            propagate_doctrine.extract_entries(doctrine)

    def test_an_unclosed_fence_stops_the_run(self, tmp_path):
        # Unclosed, it would swallow every older entry into this one.
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(FENCED_EXAMPLE.replace("## 2026-10-05: REVERT, Old subject\n```\n", "no close\n"))

        with pytest.raises(ValueError, match="unclosed code fence"):
            propagate_doctrine.extract_entries(doctrine)

    def test_a_tilde_line_inside_a_backtick_fence_does_not_close_it(self, tmp_path):
        doctrine = tmp_path / "doctrine-updates.md"
        doctrine.write_text(FENCED_EXAMPLE.replace("```markdown\n", "```markdown\n~~~\n"))

        entries = propagate_doctrine.extract_entries(doctrine)

        assert [d for d, _ in entries] == ["2026-10-01", "2026-09-18"]

    def test_trailing_whitespace_on_a_heading_does_not_resend_it(self, fleet):
        mark = fleet[0] / ".claude" / "doctrine-delivered"
        mark.write_text("## 2026-09-18: C  \n## 2026-08-21: A\t\n")

        propagate_doctrine.propagate()

        assert _note(fleet[0]) == ""

    def test_the_mark_is_written_even_when_everything_due_is_already_unread(self, fleet):
        # Pins the gate's surviving mutant N7: no mark here re-sends C after review.
        note = fleet[0] / ".claude" / "upstream-update.md"
        note.write_text("# U\n\n---\n\n## 2026-09-18: C\n\nC body.\n")
        propagate_doctrine.propagate()
        note.unlink()

        propagate_doctrine.propagate()

        assert _note(fleet[0]) == ""


def test_an_unclosed_fence_error_names_the_file_line(tmp_path):
    doctrine = tmp_path / "doctrine-updates.md"
    text = FENCED_EXAMPLE.replace("## 2026-10-05: REVERT, Old subject\n```\n", "no close\n")
    doctrine.write_text(text)
    fence_line = text.splitlines().index("```markdown") + 1

    with pytest.raises(ValueError, match=f"line {fence_line}$"):
        propagate_doctrine.extract_entries(doctrine)


def test_an_indented_fence_still_hides_its_headings(tmp_path):
    # Pins the gate's surviving mutant N9 (indented fence markers ignored).
    doctrine = tmp_path / "doctrine-updates.md"
    doctrine.write_text(FENCED_EXAMPLE.replace("```markdown\n## 2026-10-05: REVERT, Old subject\n```", "  ```markdown\n## 2026-10-05: REVERT, Old subject\n  ```"))

    assert [d for d, _ in propagate_doctrine.extract_entries(doctrine)] == ["2026-10-01", "2026-09-18"]


# --- the hub's own exclusions ---


def test_the_hub_never_writes_into_the_assay_mirror():
    # ~/projects/github/assay mirrors a work repository; the user's rule
    # (2026-10-02) is that this hub never writes into it.
    import yaml

    config = Path(__file__).resolve().parents[2] / "config" / "project.yaml"
    exclude = yaml.safe_load(config.read_text(encoding="utf-8"))["propagation"]["exclude"]
    assert "github/assay" in exclude
