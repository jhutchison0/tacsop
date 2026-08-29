#!/usr/bin/env python3
"""Check this machine before it writes to the lake.

Every check here answers a question that has already cost someone something.
The reference repo goes stale and its conventions drift out from under you. A
mode flag threaded through three of four processes writes production data for
five days before anyone notices. Uncontrolled local cache fills a shared host
to zero bytes free and locks a colleague out of the box.

What this script will not do is guess. It checks credential presence, never
reachability, and it says which one it checked. A preflight that predicts what
a run will do must mirror what the run actually does; a conservative gate that
blocks good work is still a wrong gate.

Usage:
    python scripts/lake_preflight.py --target dev
    python scripts/lake_preflight.py --target prod --fetch --strict
"""

import argparse
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.myproject.utils.machine import Machine, resolve_machine

REFERENCE = "lakehouse"

# Past this, the local clone has probably missed a convention change. The
# lakehouse repo has averaged a commit every few days; a season of silence
# means the clone, not the upstream.
STALE_AFTER_DAYS = 30

# Maturity tiers, not deployment environments. `prod` writes where consumers
# read. `dev` and `scratch` write where nobody reads but you.
TARGETS = ("dev", "scratch", "prod")

TARGET_FLAG = "--lake-profile"

# Two namespaces, both real. The lakehouse docs and its agent-facing reference
# use MINIO_*; several of its own operational scripts and the registry service
# read S3_*. A tool that works today can fail tomorrow on the same box because
# it reached for the other name.
MINIO_VARS = ("MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY")
S3_VARS = ("S3_ENDPOINT", "S3_ACCESS_KEY", "S3_SECRET_KEY")
CREDENTIAL_VARS = MINIO_VARS + S3_VARS

# Extensions the lakehouse's own .gitignore excludes. Data belongs in the lake;
# what stays local is a cache you can regenerate. 713 GB of one such cache once
# filled a shared host to zero bytes and locked a colleague out of the box.
DATA_SUFFIXES = (
    ".parquet", ".pq", ".feather", ".arrow", ".orc", ".avro",
    ".nc", ".nc4", ".grib", ".grib2", ".h5", ".hdf5",
    ".gpkg", ".shp", ".tif", ".tiff", ".cog",
    ".duckdb", ".sqlite", ".sqlite3", ".pkl",
)

SKIP_DIRS = {".venv", ".git", "node_modules", "__pycache__"}

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Result:
    """One check's verdict."""

    name: str
    status: str  # PASS | WARN | FAIL
    detail: str


def check_reference_repo(machine: Machine) -> Result:
    """The lakehouse SOP repo must be on disk before anything reads it."""
    path = machine.references.get(REFERENCE)
    if path is None:
        return Result(
            "reference repo",
            "FAIL",
            f"no {REFERENCE} reference for {machine.name} in config/project.yaml",
        )
    if not path.is_dir():
        return Result("reference repo", "FAIL", f"{REFERENCE} not on disk at {path}")
    return Result("reference repo", "PASS", str(path))


def check_reference_currency(machine: Machine) -> Result:
    """How old is the local clone's newest commit?

    Reads the local clone only. Without --fetch this cannot know whether origin
    has moved, and the detail line says so rather than implying it checked.
    """
    path = machine.references.get(REFERENCE)
    if path is None or not path.is_dir():
        return Result("reference currency", "FAIL", "no reference repo to date")

    committed = subprocess.run(
        ["git", "-C", str(path), "log", "-1", "--format=%ct"],
        capture_output=True,
        text=True,
    )
    if committed.returncode != 0 or not committed.stdout.strip():
        return Result("reference currency", "WARN", f"{path} is not a git clone")

    age = datetime.now(timezone.utc) - datetime.fromtimestamp(
        int(committed.stdout.strip()), tz=timezone.utc
    )
    days = age.days
    status = "WARN" if days > STALE_AFTER_DAYS else "PASS"
    return Result(
        "reference currency",
        status,
        f"newest commit is {days} days old (local clone only; --fetch to ask origin)",
    )


def check_target(target: str | None) -> Result:
    """Which tier is this run writing to?

    A bare invocation fails. launch-control made bare mean production in every
    entry point but one, and wrote to the live staging bucket for five days
    before anyone read the lake and noticed. The safer default is the one that
    refuses to guess.
    """
    if target is None:
        return Result(
            "target",
            "FAIL",
            f"refusing a bare invocation: pass --target {{{','.join(TARGETS)}}}",
        )
    if target not in TARGETS:
        return Result(
            "target", "FAIL", f"{target!r} is not a target (have: {', '.join(TARGETS)})"
        )
    if target == "prod":
        return Result("target", "PASS", "PRODUCTION: writing where consumers read")
    return Result("target", "PASS", target)


def check_leg_threading(target: str, legs: list[str]) -> Result:
    """Does every leg of the chain carry the same target?

    This is the check that exists because of one specific bug. A mode flag
    threaded through the engine and stage1 but not stage2 meant one process
    loaded production config while its siblings ran in dev. Nothing failed;
    the data just went to the wrong bucket. The same class recurred a month
    later in a different driver.

    A target declared once is not a target threaded everywhere.
    """
    if not legs:
        return Result(
            "leg threading",
            "WARN",
            "no legs declared, so nothing was checked; pass --leg per process",
        )

    expected = f"{TARGET_FLAG} {target}"
    unthreaded = [leg for leg in legs if expected not in leg]
    if unthreaded:
        names = ", ".join(leg.split()[0] for leg in unthreaded)
        return Result(
            "leg threading",
            "FAIL",
            f"{len(unthreaded)} of {len(legs)} legs miss '{expected}': {names}",
        )
    return Result("leg threading", "PASS", f"{len(legs)} legs carry {expected}")


def check_environment() -> Result:
    """Are lake credentials present in the environment?

    Presence, not reachability. This never opens a socket, so it cannot tell
    you the lake is up, only that a client would find something to try. The
    detail line says which one it checked so nobody reads more into a PASS
    than it earned.
    """
    have_minio = all(os.environ.get(v) for v in MINIO_VARS)
    have_s3 = all(os.environ.get(v) for v in S3_VARS)

    if not have_minio and not have_s3:
        return Result(
            "environment",
            "FAIL",
            f"no lake credentials in the environment (presence check; "
            f"set {MINIO_VARS[0]}... or {S3_VARS[0]}...)",
        )
    if have_minio and have_s3:
        return Result(
            "environment", "PASS", "both namespaces set (presence, not reachability)"
        )
    missing = "S3_*" if have_minio else "MINIO_*"
    return Result(
        "environment",
        "WARN",
        f"only one namespace set; {missing} unset, and some lakehouse tooling "
        f"reads it (presence, not reachability)",
    )


def check_local_data(root: Path) -> Result:
    """Is bulk data sitting on this machine that belongs in the lake?"""
    found = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in DATA_SUFFIXES:
            continue
        if SKIP_DIRS.intersection(path.parts):
            continue
        found.append(path)

    if not found:
        return Result("local data", "PASS", "no data-shaped files outside the lake")

    total = sum(f.stat().st_size for f in found)
    names = ", ".join(f.name for f in sorted(found)[:3])
    more = f" and {len(found) - 3} more" if len(found) > 3 else ""
    return Result(
        "local data",
        "WARN",
        f"{len(found)} data files, {total / 1e6:.1f} MB, on this machine: "
        f"{names}{more}",
    )


def run_checks(target: str | None, legs: list[str], *, fetch: bool) -> list[Result]:
    """Every check, in the order an operator would ask them."""
    machine = resolve_machine()
    if fetch:
        path = machine.references.get(REFERENCE)
        if path and path.is_dir():
            subprocess.run(
                ["git", "-C", str(path), "fetch", "--quiet"], capture_output=True
            )
    return [
        check_reference_repo(machine),
        check_reference_currency(machine),
        check_target(target),
        check_leg_threading(target or "", legs),
        check_environment(),
        check_local_data(REPO_ROOT),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--target",
        help=f"which tier this run writes to: {', '.join(TARGETS)}. "
        "Omitting it is an error, not a default.",
    )
    parser.add_argument(
        "--leg",
        action="append",
        default=[],
        dest="legs",
        metavar="CMD",
        help="one process in the chain, repeatable. Each is checked for the "
        "target flag, because a target declared once is not a target "
        "threaded everywhere.",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="ask origin whether the reference repo has moved. Touches the network.",
    )
    parser.add_argument(
        "--strict", action="store_true", help="treat every WARN as a failure"
    )
    args = parser.parse_args(argv)

    results = run_checks(args.target, args.legs, fetch=args.fetch)

    width = max(len(r.name) for r in results)
    for r in results:
        print(f"  {r.name.ljust(width)}  {r.status:<4}  {r.detail}")

    failed = [r for r in results if r.status == "FAIL"]
    warned = [r for r in results if r.status == "WARN"]
    print()
    if failed:
        print(f"{len(failed)} FAIL, {len(warned)} WARN. See PREFLIGHT.md.")
        return 1
    if warned and args.strict:
        print(f"0 FAIL, {len(warned)} WARN, and --strict makes a warning fatal.")
        return 1
    print(f"clean ({len(warned)} WARN)." if warned else "clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
