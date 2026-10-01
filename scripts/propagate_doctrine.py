#!/usr/bin/env python3
"""Propagate doctrine updates to sibling repos.

Sends each sibling repo that has a .claude/commands/ directory every entry in
docs/doctrine-updates.md it has not been offered, appended to its notification
file (.claude/upstream-update.md), oldest first. A delivery mark
(.claude/doctrine-delivered) lists, one per line, the entry headings the hub
has offered that repo; each run adds the hub's headings and never removes one.

Usage:
    python scripts/propagate_doctrine.py [--dry-run] [--since YYYY-MM-DD]

--since applies to repos with no mark yet: it sends every entry from that date.
Without it, an unmarked repo gets the newest entry only. A repo that already
holds entries the run would send needs its mark seeded first; see "Seeding a
mark by hand" in docs/propagation-protocol.md.
Exit 1 if any repo failed or the run was refused; 0 otherwise.
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


def _with_fences(text: str):
    """Yield (line, inside_a_code_fence) for each line; fence markers count as inside.

    A fence closes only on the character that opened it, at least as long
    (CommonMark), so a ~~~ line inside a ``` block stays inside. A fence still
    open at the end raises ValueError: it would swallow everything after it.
    """
    opener = ""
    for number, line in enumerate(text.splitlines(), 1):
        run = re.match(r"\s*(`{3,}|~{3,})", line)
        if run and not opener:
            opener, opened_at = run.group(1), number
            yield line, True
        elif run and run.group(1)[0] == opener[0] and len(run.group(1)) >= len(opener):
            opener = ""
            yield line, True
        else:
            yield line, bool(opener)
    if opener:
        raise ValueError(f"unclosed code fence opened at line {opened_at}")


def extract_entries(doctrine_path: Path) -> list[tuple[str, str]]:
    """Every dated entry in the doctrine file as (date, text), in file order.

    A `## ` heading starts an entry only outside a code fence. One that is not
    dated (`## YYYY-MM-DD: Subject`) raises ValueError naming it: an entry with
    a typo in its heading would otherwise never ship.
    """
    if not doctrine_path.exists():
        return []
    # The header ends at the first horizontal rule; entries follow, newest first.
    parts = re.split(r"\n---\n", doctrine_path.read_text(encoding="utf-8"), maxsplit=1)
    if len(parts) < 2:
        return []
    entries: list[list] = []
    seen: set[str] = set()
    for line, fenced in _with_fences(parts[1]):
        if line.startswith("## ") and not fenced:
            line = line.rstrip()
            heading = ENTRY_HEADING.match(line)
            if not heading:
                raise ValueError(f"doctrine heading is not dated (## YYYY-MM-DD: Subject): {line!r}")
            if line in seen:
                # A heading is an entry's identity; a repeat would never ship.
                raise ValueError(f"doctrine heading appears twice: {line!r}")
            seen.add(line)
            entries.append([heading.group(1), [line]])
        elif entries:
            entries[-1][1].append(line)
    return [(day, re.sub(r"\n+---\s*$", "", "\n".join(lines).strip())) for day, lines in entries]


def _heading(entry: tuple[str, str]) -> str:
    return entry[1].splitlines()[0]


def _headings(text: str) -> set[str]:
    """The dated entry headings in a notification, outside code fences."""
    return {line.rstrip() for line, fenced in _with_fences(text) if not fenced and ENTRY_HEADING.match(line)}


def read_mark(mark_file: Path) -> set[str] | None:
    """The entry headings a repo has been offered; None if it has no mark.

    Raises ValueError for a mark that is not all dated headings (garbage, a
    BOM, git conflict markers, an empty file), so it is reported, not trusted.
    """
    if not mark_file.exists():
        return None
    lines = [line.rstrip() for line in mark_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    bad = [line for line in lines if not ENTRY_HEADING.match(line)]
    if bad or not lines:
        raise ValueError(f"malformed delivery mark: {bad[0] if bad else 'empty'!r}")
    return set(lines)


def entries_to_deliver(
    entries: list[tuple[str, str]], held: set[str] | None, since: str | None, existing: str
) -> list[tuple[str, str]]:
    """The entries one repo still needs, oldest first.

    A mark wins: every entry whose heading it does not hold goes, whatever its
    date. With no mark, everything from `since` goes, or, with no `since`, the
    newest entry alone. An entry already unread in the repo's notification is
    never sent twice.
    """
    if held is not None:
        wanted = [e for e in entries if _heading(e) not in held]
    elif since:
        wanted = [e for e in entries if e[0] >= since]
    else:
        wanted = entries[:1]
    unread = _headings(existing)
    return [e for e in reversed(wanted) if _heading(e) not in unread]


def build_notification(latest_entry: str) -> str:
    """Build the notification file content."""
    return f"""# Upstream Doctrine Update

**Source**: [tacsop]({TACSOP_ROOT}) — shared workflow template
**Action**: Review changes below and selectively merge into your project's command files.
**Cleanup**: Delete this file after reviewing.

---

{latest_entry}
"""


def propagate(dry_run: bool = False, since: str | None = None) -> int:
    """Send each repo every entry it has not been offered; return the failure count.

    The mark (`.claude/doctrine-delivered`) is the set of entry headings the
    hub has offered that repo, one per line. Each run adds the hub's current
    headings and never removes one, so an entry skipped because it was
    already unread, or a run from an older hub checkout, never causes a
    re-send. One repo's failure is reported and the run moves on.
    """
    entries = extract_entries(DOCTRINE_FILE)
    if not entries:
        print("No doctrine updates found.")
        return 0
    newest = max(day for day, _ in entries)
    if since and since > newest:
        # A typo here would otherwise mark every repo delivered and send nothing.
        raise ValueError(f"--since {since} is after the newest entry ({newest}); it would send nothing")

    repos = find_downstream_repos()
    if not repos:
        print("No downstream repos with .claude/commands/ found.")
        return 0

    offered = {_heading(e) for e in entries}
    failures = 0
    for repo in repos:
        rel = repo.relative_to(PROJECTS_DIR)
        target = repo / NOTIFICATION_FILENAME
        mark_file = repo / MARK_FILENAME
        try:
            held = read_mark(mark_file)
            existing = target.read_text(encoding="utf-8") if target.exists() else ""
            due = entries_to_deliver(entries, held, since, existing)
            new_mark = (held or set()) | offered
            dates = ", ".join(day for day, _ in due)
            noun = "entry" if len(due) == 1 else "entries"
            if dry_run:
                mode = "append" if existing else "new"
                change = f"mark {len(held) if held is not None else 'none'} -> {len(new_mark)} headings"
                sent = f"{len(due)} {noun} ({dates}) ({mode})" if due else "nothing"
                print(f"[dry-run] {rel}: would send {sent}; {change}")
                continue
            body = "\n\n---\n\n".join(text for _, text in due)
            if not due:
                print(f"Up to date: {rel}")
            elif existing:
                target.write_text(existing.rstrip() + "\n\n---\n\n" + body + "\n", encoding="utf-8")
                print(f"Appended {len(due)} {noun} ({dates}): {rel}")
            else:
                target.write_text(build_notification(body), encoding="utf-8")
                print(f"Notified {len(due)} {noun} ({dates}): {rel}")
            if new_mark != held:
                mark_file.write_text("\n".join(sorted(new_mark, reverse=True)) + "\n", encoding="utf-8")
        except (OSError, UnicodeDecodeError, ValueError) as err:
            failures += 1
            print(f"FAILED {rel}: {err}")
    return failures


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
    try:
        return 1 if propagate(dry_run=args.dry_run, since=args.since) else 0
    except ValueError as err:
        print(f"Refused, nothing written: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
