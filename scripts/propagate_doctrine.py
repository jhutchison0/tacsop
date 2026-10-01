#!/usr/bin/env python3
"""Propagate doctrine updates to sibling repos.

Sends each sibling repo that has a .claude/commands/ directory every entry in
docs/doctrine-updates.md it has not been sent: appended to its notification
file (.claude/upstream-update.md), oldest first. A delivery mark
(.claude/doctrine-delivered) records the newest entry date the hub has offered
that repo, so the next run sends only what is newer.

Usage:
    python scripts/propagate_doctrine.py [--dry-run] [--since YYYY-MM-DD]

--since applies to repos with no mark yet: it sends every entry from that date.
Without it, an unmarked repo gets the newest entry only, which is right for a
repo bootstrapped from the template (it already holds everything older).
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

TACSOP_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = TACSOP_ROOT.parent.parent  # ~/projects
DOCTRINE_FILE = TACSOP_ROOT / "docs" / "doctrine-updates.md"
NOTIFICATION_FILENAME = ".claude/upstream-update.md"
MARK_FILENAME = ".claude/doctrine-delivered"


def find_downstream_repos() -> list[Path]:
    """Find repos with .claude/commands/ recursively across all project directories.

    A repo is any directory containing .claude/commands/. Skips tacsop itself
    and filters out nested repos (e.g. git submodules inside another repo's
    subtree like lib/PageIndex).
    """
    repos = []
    for commands_dir in sorted(PROJECTS_DIR.rglob(".claude/commands")):
        if not commands_dir.is_dir():
            continue
        repo = commands_dir.parent.parent  # .claude/commands -> .claude -> repo
        if repo == TACSOP_ROOT:
            continue
        repos.append(repo)

    # Remove nested repos — if repo A is inside repo B, keep only B
    filtered = []
    for repo in repos:
        if not any(repo != other and repo.is_relative_to(other) for other in repos):
            filtered.append(repo)
    return filtered


ENTRY_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}):", re.MULTILINE)


def extract_entries(doctrine_path: Path) -> list[tuple[str, str]]:
    """Every dated entry in the doctrine file as (date, text), newest first."""
    if not doctrine_path.exists():
        return []
    # The header ends at the first horizontal rule; entries follow, newest first.
    parts = re.split(r"\n---\n", doctrine_path.read_text(), maxsplit=1)
    if len(parts) < 2:
        return []
    entries = []
    for chunk in re.split(r"\n(?=## \d{4}-\d{2}-\d{2}:)", parts[1].strip()):
        heading = ENTRY_HEADING.match(chunk.strip())
        if heading:
            text = re.sub(r"\n+---\s*$", "", chunk.strip())
            entries.append((heading.group(1), text))
    return entries


def entries_to_deliver(entries, mark, since, existing) -> list[tuple[str, str]]:
    """The entries one consumer still needs, oldest first.

    A delivery mark (the newest date this consumer was sent) wins: everything
    newer goes. With no mark, everything from `since` goes, or, with no `since`,
    the newest entry alone. An entry whose heading already sits in the consumer's
    unread notification is never sent twice.
    """
    if mark:
        wanted = [e for e in entries if e[0] > mark]
    elif since:
        wanted = [e for e in entries if e[0] >= since]
    else:
        wanted = entries[:1]
    unread = set(existing.splitlines())
    return [e for e in reversed(wanted) if e[1].splitlines()[0] not in unread]


def build_notification(latest_entry: str) -> str:
    """Build the notification file content."""
    return f"""# Upstream Doctrine Update

**Source**: [tacsop]({TACSOP_ROOT}) — shared workflow template
**Action**: Review changes below and selectively merge into your project's command files.
**Cleanup**: Delete this file after reviewing.

---

{latest_entry}
"""


def propagate(dry_run: bool = False, since: str | None = None) -> None:
    """Send each consumer every entry it has not been sent, then mark it.

    The mark (`.claude/doctrine-delivered`) holds the newest entry date the hub
    has offered that consumer. It is the hub's newest date, not the newest one
    sent, so an entry skipped because it already sat unread is not re-sent
    after the consumer reviews and deletes the notification.
    """
    entries = extract_entries(DOCTRINE_FILE)
    if not entries:
        print("No doctrine updates found.")
        return

    repos = find_downstream_repos()
    if not repos:
        print("No downstream repos with .claude/commands/ found.")
        return

    for repo in repos:
        rel = repo.relative_to(PROJECTS_DIR)
        target = repo / NOTIFICATION_FILENAME
        mark_file = repo / MARK_FILENAME
        mark = mark_file.read_text().strip() if mark_file.exists() else None
        existing = target.read_text() if target.exists() else ""
        due = entries_to_deliver(entries, mark, since, existing)
        dates = ", ".join(date for date, _ in due)
        if dry_run:
            if due:
                mode = "append" if existing else "new"
                print(f"[dry-run] Would write: {target} ({mode}): {len(due)} entries ({dates})")
            else:
                print(f"[dry-run] Up to date: {rel}")
            continue
        body = "\n\n---\n\n".join(text for _, text in due)
        if not due:
            print(f"Up to date: {rel}")
        elif existing:
            target.write_text(existing.rstrip() + "\n\n---\n\n" + body + "\n")
            print(f"Appended {len(due)} ({dates}): {rel}")
        else:
            target.write_text(build_notification(body))
            print(f"Notified {len(due)} ({dates}): {rel}")
        mark_file.write_text(entries[0][0] + "\n")


def _entry_date(value: str) -> str:
    """argparse type: a real YYYY-MM-DD date, returned as given."""
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {value!r}") from None
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what each repo would be sent, without writing files",
    )
    parser.add_argument(
        "--since",
        type=_entry_date,
        help="For repos with no delivery mark: send every entry from this date",
    )
    args = parser.parse_args(argv)
    propagate(dry_run=args.dry_run, since=args.since)
    return 0


if __name__ == "__main__":
    sys.exit(main())
