# Review: Home-Storage Source Material for the lake-conventions Update

**Author**: code-reviewer
**Date**: 2026-08-30
**Type**: Code review (pre-update review of source material and constraints)

The source note (`docs/design/hold/STORAGE.md`, gitignored) is sound operational doctrine with one Critical trap: its code example embeds real network addresses as environment-variable defaults, so the first repo that copies the taught pattern puts an address in git and violates the governing rule. Fix the taught pattern, settle four structural questions (vehicle, routing, authority, boundary), and the update can proceed.

This review will be committed. Every address from the source note appears here in placeholder form only.

**The governing rule, as set by the user**: personal projects get access to home storage; none of the actual addresses go into git; the skill advises agents where to look; environments and configurations carry the real paths.

## Critical

### C1. The source note's code example teaches an address-into-git pattern

The "Configuration in code" section defines data roots as:

```python
ROOT = Path(os.environ.get("<VAR>", r"\\<nas-host>\<share>"))
```

Two defects, either one disqualifying:

1. **It contradicts the governing rule on contact.** The fallback default is a real UNC path. A skill exists to be copied; the moment this pattern lands in committed code, the address is in git. The gitignore protecting the source note protects nothing downstream.
2. **It contradicts the skill's own doctrine.** SKILL.md, "Dev and production": "A bare invocation with no target is an error, not production" and "Never fall back to a base config." A missing environment variable silently resolving to a live NAS is exactly the guess that section forbids. The skill would teach one refusal-to-guess rule for the lake and the opposite reflex for home storage.

**The taught pattern must be: required variable, loud failure.**

```python
import os
from pathlib import Path

def storage_root(var: str) -> Path:
    value = os.environ.get(var)
    if value is None:
        raise RuntimeError(
            f"{var} is not set. Home-storage roots live in .env on each "
            "machine, never in code or committed config."
        )
    return Path(value)
```

No default, no address, portable to every repo. The real path lives in `.env` (uncommitted) per machine, which is also what makes the source note's own portability claim work: on the NAS itself the same variable points at the server-side path and the code does not change.

## High

### H1. The example's variable names embed the NAS hostname

The environment variable names in the source note are derived from the NAS's name. Values stay in `.env`, but **names get committed**: in code that reads them, and in `.env.example`, which this repo commits and which CLAUDE.md points newcomers at. A committed variable name containing the hostname is half an address in git.

**Fix**: name variables by role, not by host: `HOME_MEDIA_ROOT`, `HOME_CORPUS_ROOT`, `HOME_STORES_ROOT`. Add them to `.env.example` with placeholder values (`\\<nas-host>\<share>`). The skill teaches the names; only `.env` knows the values.

### H2. lake-conventions may be the wrong vehicle, and the selection rule must be falsifiable

The skill ships to roughly 19 repos, most work-scoped. Its frontmatter description, "When to use" triggers, and ADOPTION.md opening ("For a repo that reads from or writes to the lake") are all lake-shaped. Two failure modes:

- **Leakage in**: a work repo carries home-storage text. An agent grepping for storage guidance finds it and asks a work machine's operator to set `HOME_*` variables, or worse, routes work data there (see H3).
- **Leakage out**: a personal repo that uses home storage but never touches the lake has no reason to adopt lake-conventions at all, so guidance buried there never reaches the repos it exists for. The description's triggers would not fire even if adopted.

**Preferred fix (structural gate)**: a sibling skill, `home-storage-conventions` or similar, adopted only by personal-scoped repos. Work repos never carry the text, so the selection rule is falsifiable by `ls .claude/skills/`. This also honors Simplicity First: the lake skill keeps one point.

**If the lead proceeds with one skill (behavioral gate)**, the home section must open with a machine-checkable condition, for example: "This section applies only when `resolve_machine().scope` includes `personal` and the repo declares personal scope in `config/project.yaml`. On any other machine or repo, stop here." Note that `project.yaml` today has no repo-level scope field; one would need adding, with a default. Either way, the frontmatter description, "When to use" list, ADOPTION.md's first line, and the ADOPTION.md step-2 CLAUDE.md blurb all need updating, and the version bumps (scope expansion: at least 1.1.0).

### H3. Missing routing doctrine: scope decides the storage system, and crossing is never a default

The lake doctrine says work data goes to the lake. The source note says new bulk data goes to the NAS. Both are correct in their own scope, and the roster already contains one machine scoped `[work, personal]`, where an agent faces both rules at once. The hazard is asymmetric and serious in both directions: work data on a personal NAS is a data-governance violation shaped like exfiltration; personal data in the work lake pollutes governed storage.

**Fix**: pin one sentence in the update: "The project's scope selects the storage system. Work-scoped data goes to the lake; personal-scoped data goes to home storage. Crossing that line is a human decision made explicitly, never a fallback or a convenience."

### H4. Home storage has no authoritative source, and the skill cannot cite the source note

The lake skill's authority chain is explicit: the upstream repo is the authority, the skill is the portable mapping, upstream wins on disagreement. The home-storage equivalent does not exist. The source note is gitignored and hub-local; a committed skill citing it hands 18 repos a dangling pointer.

**Fix**: either name a real reference (a personal runbook repo, pointed at via the roster's `references:` block on personal machines, same mechanism as the lakehouse reference), or state honestly: "Home storage has no authoritative reference repo yet. This section is the only written doctrine; the addresses live only in each machine's environment." Do not imply an authority that is not on any disk.

## Concern

### N1. Boundary ruling: what the committed roster may carry

The roster precedent (`machines.<host>.references.lakehouse: ~/projects/...`) is a tilde-relative path to a **git checkout of documentation**, meaningful only on the named machine. A home-NAS UNC path is different in kind: it names a network endpoint any LAN machine can resolve. Proposed line, falsifiable and worth stating in the update:

> Committed config may point at code and docs (tilde-relative, no usernames). Only the environment points at data. Anything that resolves over a network (UNC path, hostname, IP, mount endpoint) never goes in git, in either role.

Under this line a home runbook reference in the roster is acceptable (it is a docs pointer); a home data root in the roster is a violation even though the roster "already has paths."

### N2. The `unknown` roster entry defaults to `scope: [personal]`

Any unrostered hostname resolves as personal-scoped (`config/project.yaml` line 33, `machine.py`). If the H2 gate keys on machine scope, an unrostered work box passes it. The absent `HOME_*` variables are a backstop (nothing resolves), but the gate would then invite an agent to prompt for them. The skill's own rule is refusing to guess: the gate should require an explicit roster entry, or the update should say "an unknown machine is not a personal machine; add the box to the roster first."

### N3. Preflight: say plainly that home storage has no coverage

All six checks in `scripts/lake_preflight.py` are lake-shaped: lakehouse reference, S3/MinIO credential namespaces, tier targets, leg threading. None asks anything about home storage. Do not extend the preflight now. PREFLIGHT.md's own doctrine settles this: a check's acceptance logic must mirror a run's, and no home-storage run is defined yet to mirror; "a conservative gate is still a wrong gate." What the update owes instead is one honest sentence: "`lake_preflight.py` checks nothing about home storage. A green preflight says nothing about it." Without that sentence, a passing preflight invites exactly the unearned confidence PREFLIGHT.md warns about.

### N4. Data-safety doctrine worth pinning (all statable without addresses)

The source note contains hard-won rules that belong in the portable skill, genericized:

1. **Never run an embedded database against a network share.** SQLite, DuckDB, Kuzu, on-disk FAISS: file locking over SMB corrupts. Live stores stay with the compute; the NAS holds closed replicas. Close the database first or copy from a snapshot.
2. **A mirror with deletions is availability, not backup.** A mirroring sync faithfully replicates a mistake, deletions included. Snapshots and the offsite copy are the undo.
3. **Redundancy survives hardware, not operators.** RAIDZ1 survives one drive failure; it does not survive a mirrored deletion. Same lesson as 2, from the disk side.
4. **Address by name, never by IP.** A DHCP reservation makes the IP stable; a name survives re-addressing.
5. **Regular credentials for data access, never admin.**
6. **Server paths never appear in client code.** If a script contains a server-side mount path and does not run on the server, it is wrong. The three-addresses concept (server path, client UNC path, admin UI) is portable; the source note's example column is not.

### N5. Machine-local operational detail that must stay out of the portable skill

These serve the operator of one box, go stale fast, and several carry real addresses:

- The share-creation click path in the NAS UI, with its real dataset path.
- The mirror-job invocation with real source, destination, and log paths.
- The Windows credential-caching UI steps.
- The admin UI URL and the "verify the hostname in the UI" caveat.
- The transient "share pending, downloads land locally and sync later" state, stale the day the share exists.
- The camera-card media pipeline. Household data flow, not project conventions; no repo runs it.
- The named internal dataset layout. Teach the roles (corpus of record, store replicas, kept artifacts); the actual share and directory names are addresses and live with the environment.

### N6. Pick one home for the variables

The source note offers "`.env` or the shell profile." Two blessed locations produce machines with both, disagreeing. The skill should pick one: `.env` per repo (matches CLAUDE.md and the existing key-handling doctrine), shell profile only for machine-wide tooling outside any repo, if at all.

## Verdict: GO-WITH-FIXES

The doctrine in the source material is good and the governing rule is implementable. Do not start writing until these are settled, in order:

1. **(C1)** Replace the env-default pattern with required-variable-loud-failure in whatever the skill teaches. The source note's example must not be copied as written into any committed artifact.
2. **(H1)** Role-based variable names (`HOME_*`); add to `.env.example` with placeholders.
3. **(H2)** Decide the vehicle. Preferred: separate personal-scoped skill. If combined: falsifiable gate condition plus frontmatter, triggers, ADOPTION.md, and version updates.
4. **(H3)** Pin the routing sentence: scope selects the storage system, crossing is a human decision.
5. **(H4)** Name a real authoritative reference for home storage or state that none exists. Never cite the gitignored note from committed text.
6. **(N3)** One sentence declaring home storage outside preflight coverage. No new checks now.
7. **(N4, N5)** Carry the six pinned safety rules in; keep the seven machine-local items out.
8. **(N1, N2, N6)** State the roster boundary line, close the `unknown`-scope gap in the gate wording, and bless `.env` as the single variable home.
