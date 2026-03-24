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
    """Find repos with .claude/commands/ across all project directories."""
    repos = []
    for project_group in sorted(PROJECTS_DIR.iterdir()):
        if not project_group.is_dir():
            continue
        for repo in sorted(project_group.iterdir()):
            if repo == UTILS_ROOT:
                continue
            if repo.is_dir() and (repo / ".claude" / "commands").is_dir():
                repos.append(repo)
    return repos


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
            print(f"[dry-run] Would write: {target}")
        else:
            target.write_text(notification)
            print(f"Notified: {repo.parent.name}/{repo.name}")

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
