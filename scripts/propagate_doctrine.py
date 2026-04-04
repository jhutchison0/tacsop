#!/usr/bin/env python3
"""Propagate doctrine updates to sibling repos.

Reads the latest entry from docs/doctrine-updates.md and drops a notification
file (.claude/upstream-update.md) into each sibling repo that has a
.claude/commands/ directory.

Usage:
    python scripts/propagate_doctrine.py [--dry-run]
"""

import argparse
import re
import sys
from pathlib import Path

UTILS_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = UTILS_ROOT.parent.parent  # ~/projects
DOCTRINE_FILE = UTILS_ROOT / "docs" / "doctrine-updates.md"
NOTIFICATION_FILENAME = ".claude/upstream-update.md"


def find_downstream_repos() -> list[Path]:
    """Find repos with .claude/commands/ recursively across all project directories.

    A repo is any directory containing .claude/commands/. Skips utils itself
    and filters out nested repos (e.g. git submodules inside another repo's
    subtree like lib/PageIndex).
    """
    repos = []
    for commands_dir in sorted(PROJECTS_DIR.rglob(".claude/commands")):
        if not commands_dir.is_dir():
            continue
        repo = commands_dir.parent.parent  # .claude/commands -> .claude -> repo
        if repo == UTILS_ROOT:
            continue
        repos.append(repo)

    # Remove nested repos — if repo A is inside repo B, keep only B
    filtered = []
    for repo in repos:
        if not any(repo != other and repo.is_relative_to(other) for other in repos):
            filtered.append(repo)
    return filtered


def extract_latest_entry(doctrine_path: Path) -> str | None:
    """Extract the most recent entry from the doctrine updates file."""
    if not doctrine_path.exists():
        return None

    content = doctrine_path.read_text()

    # Split on horizontal rules (---) to separate header from entries
    parts = re.split(r"\n---\n", content, maxsplit=1)
    if len(parts) < 2:
        return None

    entries_text = parts[1].strip()

    # Split on ## headings to get individual entries
    entries = re.split(r"\n(?=## \d{4}-\d{2}-\d{2}:)", entries_text)
    if not entries:
        return None

    return entries[0].strip()


def build_notification(latest_entry: str) -> str:
    """Build the notification file content."""
    return f"""# Upstream Doctrine Update

**Source**: [utils]({UTILS_ROOT}) — shared workflow template
**Action**: Review changes below and selectively merge into your project's command files.
**Cleanup**: Delete this file after reviewing.

---

{latest_entry}
"""


def propagate(dry_run: bool = False) -> None:
    """Main propagation logic."""
    latest = extract_latest_entry(DOCTRINE_FILE)
    if not latest:
        print("No doctrine updates found.")
        return

    repos = find_downstream_repos()
    if not repos:
        print("No downstream repos with .claude/commands/ found.")
        return

    notification = build_notification(latest)

    for repo in repos:
        target = repo / NOTIFICATION_FILENAME
        if dry_run:
            existing = " (append)" if target.exists() else " (new)"
            print(f"[dry-run] Would write: {target}{existing}")
        else:
            rel = repo.relative_to(PROJECTS_DIR)
            if target.exists():
                existing = target.read_text()
                target.write_text(existing.rstrip() + "\n\n---\n\n" + latest)
                print(f"Appended: {rel}")
            else:
                target.write_text(notification)
                print(f"Notified: {rel}")

    if dry_run:
        print(f"\nNotification content:\n{'=' * 40}\n{notification}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    args = parser.parse_args()
    propagate(dry_run=args.dry_run)
