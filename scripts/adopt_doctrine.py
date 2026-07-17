#!/usr/bin/env python3
"""Downstream-side helper to adopt the 2026-05-19 doctrine bundle from utils.

Copies TEMPLATE-COPY artifacts verbatim, substitutes the package name inside the
shift-left audit hook, merges the PostToolUse block into .claude/settings.json,
and appends to .gitignore. For CUSTOMIZE/CONDITIONAL/SKIP artifacts, prints a
manual-attention checklist with section references back to docs/doctrine-updates.md.

Run from your downstream repo root:

    python scripts/adopt_doctrine.py [--upstream PATH] [--package NAME] [--dry-run] [--yes]

Default --upstream is ~/projects/github/utils/. Default --package auto-detects
from src/<pkg>/ if exactly one subdir exists; otherwise required.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# Force UTF-8 stdio so the Unicode arrows (→) used in status messages don't
# crash on Windows, where Python's default stdio encoding is cp1252. No-op on
# POSIX (already UTF-8) and on streams that don't support reconfigure (e.g.,
# stdout redirected to a pipe with a fixed encoding).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass


HOOK_RELATIVE = ".claude/hooks/post-tool-shift-left-audit.sh"
SETTINGS_RELATIVE = ".claude/settings.json"
HOOK_COMMAND = "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-shift-left-audit.sh"
HOOK_MATCHER = "Write|Edit"
HOOK_TIMEOUT_SECONDS = 10
GITIGNORE_LINES = [".claude/audits/", "docs/design/hold/"]

VERBATIM_COPIES: list[tuple[str, str]] = [
    # (relative path, kind) — same path on both sides
    (".claude/skills/maintaining-ubiquitous-language", "dir"),
    (".claude/skills/maintaining-project-context", "dir"),
    (".claude/skills/recording-architecture-decisions", "dir"),
    (".claude/skills/shift-left-testing", "dir"),
    (".claude/skills/configuration-management", "dir"),
    (".claude/skills/python-venv-management", "dir"),
    (".claude/skills/SKILLS_FRAMEWORK.md", "file"),
    ("docs/adr/ADR-FORMAT.md", "file"),
    ("docs/session-doc-format.md", "file"),
    (".claude/commands/session-end.md", "file"),
]


class DetectionError(RuntimeError):
    """Raised when an auto-detection step cannot return an unambiguous result."""


def _detect_package(downstream_root: Path) -> str:
    """Auto-detect the downstream package name from src/<pkg>/.

    Returns the name of the single subdirectory under src/. Raises DetectionError
    if src/ is missing, contains no subdirectories, or contains more than one.
    """
    src = downstream_root / "src"
    if not src.is_dir():
        raise DetectionError(f"no src/ directory at {src}")
    subdirs = [p for p in src.iterdir() if p.is_dir()]
    if not subdirs:
        raise DetectionError(f"no src/<pkg>/ subdirectory found under {src}")
    if len(subdirs) > 1:
        names = ", ".join(sorted(p.name for p in subdirs))
        raise DetectionError(
            f"multiple src/<pkg>/ subdirectories found ({names}); "
            "pass --package NAME explicitly"
        )
    return subdirs[0].name


def _plan_copies(upstream_root: Path) -> list[tuple[Path, str, str]]:
    """Return (source_path, dest_relative, kind) for each verbatim copy."""
    return [(upstream_root / rel, rel, kind) for rel, kind in VERBATIM_COPIES]


def _apply_copies(
    plan: list[tuple[Path, str, str]],
    downstream_root: Path,
    dry_run: bool,
) -> list[dict]:
    """Apply each (src, dst, kind) copy under downstream_root.

    Never overwrites: if the target already exists, the entry is skipped with a
    'skipped (exists)' status so the user can review and merge manually.
    Returns a list of per-entry status dicts: {'dst': str, 'status': str}.
    """
    results = []
    for src, dst_rel, kind in plan:
        dst = downstream_root / dst_rel
        entry = {"dst": dst_rel, "status": ""}

        if not src.exists():
            entry["status"] = "missing (source not found)"
            print(f"[missing] {dst_rel} — source {src} not found")
            results.append(entry)
            continue

        if dst.exists():
            entry["status"] = "skipped (exists — review manually)"
            print(f"[skip] {dst_rel} — already exists; review by hand")
            results.append(entry)
            continue

        if dry_run:
            entry["status"] = "would copy (dry-run)"
            print(f"[dry-run] would copy {kind} → {dst_rel}")
            results.append(entry)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        if kind == "dir":
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        entry["status"] = f"copied ({kind})"
        print(f"[copy] {dst_rel}")
        results.append(entry)
    return results


def _substitute_hook(
    upstream_hook: Path,
    downstream_root: Path,
    package: str,
    dry_run: bool,
) -> dict:
    """Copy the audit hook with `myproject` → `package` substitution.

    Substitution is a plain string replace on the literal token `myproject`.
    The hook's bash case statement structure is preserved verbatim — we are
    only changing the package-name token, not the surrounding syntax.
    """
    dst = downstream_root / HOOK_RELATIVE
    entry = {"dst": HOOK_RELATIVE, "status": ""}

    if dst.exists():
        entry["status"] = "skipped (exists — review manually)"
        print(f"[skip] {HOOK_RELATIVE} — already exists; review by hand")
        return entry

    if dry_run:
        entry["status"] = f"would copy + substitute myproject→{package} (dry-run)"
        print(f"[dry-run] would copy {HOOK_RELATIVE} (substitute myproject → {package})")
        return entry

    body = upstream_hook.read_text()
    new_body = body.replace("myproject", package)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(new_body)
    # Preserve executable bit if the source had it
    src_mode = upstream_hook.stat().st_mode
    dst.chmod(src_mode)

    entry["status"] = f"copied + substituted myproject → {package}"
    print(f"[copy+sub] {HOOK_RELATIVE} (myproject → {package})")
    return entry


def _our_hook_block() -> dict:
    """The PostToolUse matcher block we want present in settings.json."""
    return {
        "matcher": HOOK_MATCHER,
        "hooks": [
            {
                "type": "command",
                "command": HOOK_COMMAND,
                "timeout": HOOK_TIMEOUT_SECONDS,
            }
        ],
    }


def _matcher_already_present(matchers: list, command_suffix: str) -> bool:
    """True if any matcher already wires our hook command (by command suffix)."""
    for m in matchers:
        for h in m.get("hooks", []):
            if h.get("command", "").endswith(command_suffix):
                return True
    return False


def _merge_settings(downstream_root: Path, dry_run: bool) -> dict:
    """Idempotently merge the PostToolUse hook block into .claude/settings.json.

    Creates the file if absent. Preserves all existing top-level keys and any
    existing PostToolUse matchers — appends our matcher as an additional entry.
    Skips with a 'present' status if our matcher already wires the hook.
    """
    path = downstream_root / SETTINGS_RELATIVE
    entry = {"dst": SETTINGS_RELATIVE, "status": ""}

    if dry_run:
        action = "create with hook block" if not path.exists() else "merge hook block"
        entry["status"] = f"would {action} (dry-run)"
        print(f"[dry-run] would {action} in {SETTINGS_RELATIVE}")
        return entry

    if path.exists():
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            entry["status"] = f"skipped (existing settings.json invalid: {exc})"
            print(f"[skip] {SETTINGS_RELATIVE} — existing file is not valid JSON: {exc}")
            return entry
    else:
        data = {}

    hooks = data.setdefault("hooks", {})
    matchers = hooks.setdefault("PostToolUse", [])

    if _matcher_already_present(matchers, "post-tool-shift-left-audit.sh"):
        entry["status"] = "skipped (hook already present)"
        print(f"[skip] {SETTINGS_RELATIVE} — shift-left audit hook already wired")
        return entry

    matchers.append(_our_hook_block())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    entry["status"] = "added PostToolUse matcher"
    print(f"[merge] {SETTINGS_RELATIVE} — added Write|Edit matcher for shift-left audit hook")
    return entry


def _append_gitignore(downstream_root: Path, dry_run: bool) -> dict:
    """Append GITIGNORE_LINES to .gitignore if not already present.

    Comparison is whole-line, after .strip(); we do not match substrings.
    """
    path = downstream_root / ".gitignore"
    entry = {"dst": ".gitignore", "status": ""}

    existing_lines = []
    if path.exists():
        existing_lines = [ln.strip() for ln in path.read_text().splitlines()]
    missing = [ln for ln in GITIGNORE_LINES if ln not in existing_lines]

    if not missing:
        entry["status"] = "skipped (all lines already present)"
        print(f"[skip] .gitignore — all target lines already present")
        return entry

    if dry_run:
        entry["status"] = f"would append {len(missing)} line(s) (dry-run)"
        print(f"[dry-run] would append to .gitignore: {missing}")
        return entry

    body = path.read_text() if path.exists() else ""
    if body and not body.endswith("\n"):
        body += "\n"
    body += "\n".join(missing) + "\n"
    path.write_text(body)

    label = "added" if len(missing) == len(GITIGNORE_LINES) else "partial (some already present)"
    entry["status"] = f"{label}: {missing}"
    print(f"[append] .gitignore — added {missing}")
    return entry


MANUAL_CHECKLIST_ITEMS = [
    ("LANGUAGE.md", "§1", "Copy as starter template; rewrite content per your domains."),
    ("CONTEXT.md", "§2", "Copy as starter template; rewrite identity / mission / constraints."),
    ("docs/adr/0001-directory-form-mandatory-for-new-skills.md", "§3",
     "Copy as your own ADR-0001 (or ADR-NNNN); edit Decision-maker(s) field."),
    (".claude/agents/python-prototyper.md", "§9",
     "Copy and substitute src/myproject/ to your package layout (diff first if locally customized)."),
    ("CLAUDE.md test-first wording", "§10",
     "Merge the Shift-Left Testing Development Principle block into your CLAUDE.md."),
    ("Python 3.11 minimum bump", "§11",
     "Edit pyproject.toml + config/project.yaml + CLAUDE.md by hand; verify CI supports 3.11 first."),
    ("docs/propagation-protocol.md", "§4",
     "SKIP unless your repo is also a propagation hub (currently only utils itself)."),
    (".claude/skills/session-end.md (deletion)", "§8",
     "If present, diff against docs/session-doc-format.md, move any unique content out, then delete."),
    (".claude/settings.local.json → .claude/settings.json (rename)", "§13",
     "Back up first. Anthropic convention. Your existing settings.local.json (if any) becomes per-user-override-only, gitignored."),
    (".claude/skills/shift-left-testing.md (legacy single-file)", "§5",
     "If present, delete after verifying the new directory form works."),
    (".claude/skills/configuration-management.md (legacy single-file)", "§5",
     "If present, delete after verifying the new directory form works."),
    (".claude/skills/python-venv-management.md (legacy single-file)", "§5",
     "If present, delete after verifying the new directory form works."),
]


def _print_manual_checklist() -> None:
    """Print the list of artifacts the helper deliberately does NOT touch."""
    print()
    print("=" * 72)
    print("MANUAL ATTENTION REQUIRED — the helper deliberately skipped these:")
    print("=" * 72)
    for item, section, note in MANUAL_CHECKLIST_ITEMS:
        print(f"  • {item}")
        print(f"      ({section}) {note}")
    print()
    print("Full context for each item is in the source repo at:")
    print("    docs/doctrine-updates.md  (2026-05-19 entry)")
    print()


def adopt(
    upstream: Path,
    downstream: Path,
    package: str,
    dry_run: bool,
    yes: bool,
) -> None:
    """Orchestrate the full adoption.

    Order: print the plan + manual-checklist preview, prompt for confirmation
    (unless dry_run or yes), then apply copies, hook substitution, settings
    merge, and gitignore append. Always print the manual checklist at the end.
    """
    print(f"Adopt doctrine bundle: {upstream}  →  {downstream}")
    print(f"Package name for hook substitution: {package}")
    print()

    if not dry_run and not yes:
        answer = input("Apply changes? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Aborted by user — no changes written.")
            return

    print("--- Verbatim copies ---")
    _apply_copies(_plan_copies(upstream), downstream, dry_run=dry_run)

    print("\n--- Audit hook (with package substitution) ---")
    _substitute_hook(
        upstream / HOOK_RELATIVE, downstream, package=package, dry_run=dry_run
    )

    print("\n--- .claude/settings.json (PostToolUse merge) ---")
    _merge_settings(downstream, dry_run=dry_run)

    print("\n--- .gitignore ---")
    _append_gitignore(downstream, dry_run=dry_run)

    _print_manual_checklist()


DEFAULT_UPSTREAM = Path.home() / "projects" / "github" / "utils"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Adopt the 2026-05-19 doctrine bundle from a local utils clone.",
    )
    parser.add_argument(
        "--upstream",
        type=Path,
        default=DEFAULT_UPSTREAM,
        help=f"Path to local utils clone (default: {DEFAULT_UPSTREAM})",
    )
    parser.add_argument(
        "--package",
        help="Downstream package name (default: auto-detect from src/<pkg>/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan without writing anything",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt (use with caution)",
    )
    args = parser.parse_args(argv)

    upstream = args.upstream.expanduser().resolve()
    if not upstream.is_dir():
        print(
            f"Error: --upstream path not found: {upstream}\n"
            "Clone utils to ~/projects/github/utils/ or pass --upstream PATH.",
            file=sys.stderr,
        )
        sys.exit(2)

    downstream = Path.cwd()

    if args.package:
        package = args.package
    else:
        try:
            package = _detect_package(downstream)
        except DetectionError as exc:
            print(
                f"Error: could not auto-detect package name — {exc}\n"
                "Pass --package NAME explicitly.",
                file=sys.stderr,
            )
            sys.exit(2)

    adopt(
        upstream=upstream,
        downstream=downstream,
        package=package,
        dry_run=args.dry_run,
        yes=args.yes,
    )


if __name__ == "__main__":
    main()
