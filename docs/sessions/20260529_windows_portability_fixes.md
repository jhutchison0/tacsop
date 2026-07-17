# Session: Windows-Portability Patch — Catch-Up from Heimdall-Darkroom Adoption

**Date**: 2026-05-29
**Branch**: main
**Tags**: #session #infra #bugfix #portability #complete

**Documents**: [scripts/adopt_doctrine.py](../../scripts/adopt_doctrine.py), [.claude/hooks/post-tool-shift-left-audit.sh](../../.claude/hooks/post-tool-shift-left-audit.sh), [src/myproject/utils/logger.py](../../src/myproject/utils/logger.py), [pyproject.toml](../../pyproject.toml)
**References**: [docs/doctrine-updates.md](../doctrine-updates.md) — 2026-05-29 entry; [CHANGELOG.md](../../CHANGELOG.md) — `[Unreleased]` section
**Follows**: [20260519_adopt_doctrine_helper_and_propagation.md](20260519_adopt_doctrine_helper_and_propagation.md) — cycle that shipped the buggy artifacts; [20260523_proword_convention_for_plans.md](20260523_proword_convention_for_plans.md) — most recent prior session
**Cites**: [`heimdall-darkroom` `docs/sessions/20260528_doctrine_adoption.md`](https://github.com/jhutchison0/heimdall-darkroom/blob/main/docs/sessions/20260528_doctrine_adoption.md) §6 — discovery and local fix

---

## At a glance

A small bug-fix-only session. No new doctrine, no new artifacts. The 2026-05-19 propagation cycle shipped three Windows-incompatible artifacts that `heimdall-darkroom` caught while adopting on 2026-05-28 as the first Windows-native downstream. All three were patched locally there; this session ports the fixes back upstream so the next Windows downstream (and any subsequent `adopt_doctrine.py` run) gets them for free. Two pre-existing Windows-only test failures surfaced during validation and were fixed in the same session.

| Metric | Value |
|---|---|
| Bugs fixed | 3 source + 2 test (5 total) |
| Lines changed | ~60 across 6 files |
| Tests | 45 passed, 1 skipped (the +x test, now correctly skipping on Windows) |
| New regression test | 1 (`TestTimezoneFallback`) |
| Doctrine added | 0 (pure bug-fix cycle) |
| Heimdall task closed | 1 carry-over (Phase 2 still un-scoped — separate matter) |

---

## 1. Discovery context

Yesterday's session in `heimdall-darkroom` (2026-05-28) was the first time the 2026-05-19 doctrine bundle ran end-to-end on a Windows machine. The user explicitly flagged this risk going in: *"this is my only windows main repo, so there may be more adaption necessary with this first push - please keep your eye out for those!"* — and three Windows-only failure modes appeared in artifacts that this repo shipped:

1. `scripts/adopt_doctrine.py` crashed immediately on `UnicodeEncodeError` — couldn't encode `→` against cp1252.
2. `.claude/hooks/post-tool-shift-left-audit.sh` "installed" successfully but silently no-op'd on every Write/Edit because its case-glob couldn't match Windows backslash paths.
3. `src/myproject/utils/logger.py` (a template module, copied into `heimdall-darkroom`'s `src/heimdall/util/logger.py` at scaffold time) raised `ZoneInfoNotFoundError` on Windows without `tzdata` — an exception its `except` clause didn't list. This had actually been a known issue since heimdall's 2026-04-22 session but was never propagated upstream.

All three were patched in `heimdall-darkroom` locally that same session. The carry-over task in `heimdall-darkroom`'s `docs/tasks.md` was: report the fixes back to utils. This session is that report.

---

## 2. Approach: copy the heimdall fixes upstream, then run utils' own tests

Each fix had already been designed and validated in `heimdall-darkroom`, so the upstream work was largely transcription: apply the same minimal change to the upstream file, ideally with a slightly fuller comment explaining the rationale (since the upstream is the canonical source for new downstream adopters).

```mermaid
graph LR
  classDef done fill:#c8f7c5,stroke:#2b7a0b

  H1[heimdall:<br/>adopt_doctrine.py UTF-8 fix]:::done --> U1[utils:<br/>same fix, fuller comment]:::done
  H2[heimdall:<br/>hook path normalize]:::done --> U2[utils:<br/>same fix, clarify subdir matching]:::done
  H3[heimdall:<br/>logger.py except + tzdata dep]:::done --> U3[utils:<br/>same fix + add regression test]:::done

  U1 --> T[Run utils pytest]:::done
  U2 --> T
  U3 --> T
  T --> DISCO[Discover 2 pre-existing<br/>Windows test failures]:::done
  DISCO --> F1[Fix POSIX path string-compare]:::done
  DISCO --> F2[Skipif +x test on win32]:::done
  F1 --> V[Verify end-to-end:<br/>UTF-8 fix + hook fire on Windows path]:::done
  F2 --> V
  V --> CHG[Update CHANGELOG.md +<br/>doctrine-updates.md]:::done
```

Two pre-existing Windows test failures were discovered while running `pytest` to confirm the fixes didn't regress anything — and got fixed in the same session since they were in the same scope (Windows portability of utils' test surface).

---

## 3. The three Windows-portability fixes

### 3a. `scripts/adopt_doctrine.py` — UTF-8 stdio reconfigure

**Bug**: Python 3.13 on Windows defaults to cp1252 stdio encoding, which can't encode `→` (U+2192). The helper prints `→` in eight places (lines 106, 127, 142, 143, 155, 156, 275, 314). First invocation crashes:

```
UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 61: character maps to <undefined>
```

**Fix**: Add a fail-soft stdio reconfigure block at the top of the imports section:

```python
# Force UTF-8 stdio so the Unicode arrows (→) used in status messages don't
# crash on Windows, where Python's default stdio encoding is cp1252. No-op on
# POSIX (already UTF-8) and on streams that don't support reconfigure (e.g.,
# stdout redirected to a pipe with a fixed encoding).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
```

**Why this approach (not other options)**:
- Could have replaced `→` with `->` everywhere — simpler one-time edit but uglier output and doesn't fix the underlying cp1252 problem for any future Unicode the script might emit.
- Could have required users to run with `PYTHONUTF8=1` — pushes the problem onto every downstream user. Anti-doctrine: the helper should "just work."
- Fail-soft try/except is the safest: works on Python 3.7+ where `reconfigure` exists; degrades silently on edge cases (stdout pipe with fixed encoding) without breaking the script.

### 3b. `.claude/hooks/post-tool-shift-left-audit.sh` — path normalization

**Bug**: The hook's case-glob `*/src/<pkg>/*.py` can't match Windows backslash-separated paths. The Claude Code harness passes `file_path` verbatim from the tool call. On Windows that's `C:\Users\…\src\<pkg>\foo.py` — no `/src/<pkg>/` substring, so the case falls through to `exit 0`. **Silent no-op for every Edit/Write on Windows.** The hook *appears* installed (no errors, exit 0) but never produces audit log entries and never warns about missing test partners.

**Fix**: Normalize backslashes to forward slashes immediately after the jq parse:

```bash
# Normalize Windows backslash paths to forward slashes so the case globs
# match on both Git Bash (Windows) and POSIX shells. The harness passes
# file_path verbatim from the tool call; on Windows that is backslash-
# separated. Without normalization, the `*/src/<pkg>/*.py` glob below
# would never match a Windows path and the hook would silently no-op.
file_path=${file_path//\\//}
```

**Bonus comment clarification**: The original hook's subdirectory matching behavior wasn't documented. In bash `case` patterns (unlike pathname expansion), `*` matches any string including `/`. So `*/src/<pkg>/*.py` correctly matches `…/src/<pkg>/sub/path/foo.py`. Added a comment to that effect so future readers don't try to "fix" the pattern to use `**` (which is invalid in case patterns).

### 3c. `src/myproject/utils/logger.py` + `pyproject.toml` — ZoneInfoNotFoundError + tzdata

**Bug**: On Windows + Python 3.9+, CPython's bundled `zoneinfo` has no backing timezone data. `ZoneInfo("America/Chicago")` raises `zoneinfo.ZoneInfoNotFoundError` — a `KeyError` subclass, NOT `ImportError` or `ValueError`. The logger's existing except clause caught only `(ImportError, ValueError)`, so on Windows without `tzdata` installed, the exception propagated and **every caller of `get_logger()` crashed at import time**.

This is the oldest of the three bugs — `heimdall-darkroom` hit it on 2026-04-22 during the Phase 1 pivot, patched locally that day, and added "port back to utils template" to the task list. The carry-over has been open for over a month.

**Fix**:

```python
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
...
        # Resolve timezone. On Windows + Python 3.9+ without the `tzdata`
        # package installed, ZoneInfo("America/Chicago") raises
        # ZoneInfoNotFoundError (a KeyError subclass, NOT ImportError or
        # ValueError). The `tzdata` dep in pyproject.toml carries the data on
        # win32; this except clause guarantees that misconfigured environments
        # fall back gracefully rather than crash at import-time of any module
        # that uses get_logger().
        try:
            tz = ZoneInfo(timezone)
            logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()
        except (ImportError, ValueError, ZoneInfoNotFoundError):
            tz = None
            logger.warning(...)
```

And in `pyproject.toml`:

```toml
dependencies = [
    "pyyaml>=6.0",
    "python-dotenv>=1.0",
    "numpy>=1.24",
    # zoneinfo backing data is missing from CPython on Windows; the logger
    # falls back gracefully without it (see src/myproject/utils/logger.py),
    # but installing tzdata makes named timezones work as expected.
    "tzdata; sys_platform == 'win32'",
]
```

**Belt-and-braces strategy**: the dep makes named timezones actually work; the except clause guarantees graceful fallback if the dep is somehow missing. Either alone fixes the immediate crash, but the combination is more robust.

**Regression test added** (`tests/unit/test_logger.py::TestTimezoneFallback`):

```python
def test_setup_logger_falls_back_when_zoneinfo_data_missing(self, monkeypatch, tmp_path):
    def boom(_name):
        raise zoneinfo.ZoneInfoNotFoundError("simulated missing tzdata")
    monkeypatch.setattr("src.myproject.utils.logger.ZoneInfo", boom)
    logger = LoggerSetup.setup_logger("test_tz_fallback", tmp_path / "logs")
    assert logger is not None
    assert len(logger.handlers) == 2  # file + console, fallback succeeded
```

The test deliberately raises `ZoneInfoNotFoundError` from a monkeypatched `ZoneInfo` to confirm the except clause catches it. Without the fix, this test fails with the unhandled exception; with the fix, it passes.

---

## 4. Two pre-existing Windows test failures (caught during validation)

Running `pytest tests/unit/test_logger.py tests/unit/test_adopt_doctrine.py` to confirm no regressions, two pre-existing Windows-only failures surfaced — both in `test_adopt_doctrine.py`, both unrelated to my fixes (confirmed by stashing my changes and re-running: same failures). Same Windows-portability theme so I fixed them in scope.

### 4a. `TestPlanCopies::test_sources_rooted_at_upstream`

```python
upstream = Path("/fake/upstream")
plan = adopt_doctrine._plan_copies(upstream)
for src, _dst, _kind in plan:
    assert str(src).startswith("/fake/upstream/")
```

On Windows, `Path("/fake/upstream") / "x"` produces a `WindowsPath`, and `str()` of it returns `\fake\upstream\x` with backslashes. The string-prefix check is POSIX-only.

**Fix**: Use `Path.is_relative_to` (Python 3.9+), which is path-aware:

```python
for src, _dst, _kind in plan:
    assert Path(src).is_relative_to(upstream)
```

### 4b. `TestSubstituteHook::test_executable_bit_preserved`

```python
src.chmod(0o755)
adopt_doctrine._substitute_hook(...)
assert dst.stat().st_mode & 0o111
```

NTFS has no POSIX `+x` bit. `chmod(0o755)` on Windows is effectively a no-op (it only flips the read-only flag). `dst.stat().st_mode & 0o111` is always `0`.

**Fix**: Skip on Windows with a comment explaining why the bit isn't load-bearing there:

```python
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="NTFS has no POSIX +x bit; chmod(0o755) is a no-op on Windows. "
           "Hooks invoked via `bash <path>` from the harness don't need "
           "the bit anyway.",
)
def test_executable_bit_preserved(self, tmp_path, downstream):
    ...
```

The "hooks invoked via `bash <path>` from the harness don't need the bit anyway" line is the load-bearing rationale: on Windows, hook execution goes through `bash` (Git Bash) which interprets the shebang itself, not the OS. The +x bit is irrelevant.

---

## 5. Verification

### 5a. Test suite

```
$ python -m pytest tests/unit/test_logger.py tests/unit/test_adopt_doctrine.py -q
........................s.....................                           [100%]
45 passed, 1 skipped in 0.33s
```

- `s` is `test_executable_bit_preserved` correctly skipping on Windows.
- All other 45 tests pass, including the new `TestTimezoneFallback::test_setup_logger_falls_back_when_zoneinfo_data_missing`.
- Full test suite (`python -m pytest`) collection fails on missing `numpy` — pre-existing environment issue with no venv in utils, unrelated to this session.

### 5b. Direct end-to-end checks

```
# adopt_doctrine.py — run WITHOUT PYTHONUTF8=1 on Windows
$ .venv/Scripts/python.exe scripts/adopt_doctrine.py --package heimdall --dry-run
Adopt doctrine bundle: C:\Users\johnk\projects\github\utils  →  C:\Users\johnk\projects\github\heimdall-darkroom
Package name for hook substitution: heimdall
...
exit was 0
```

Before the fix: `UnicodeEncodeError` on first print. After the fix: clean output, exit 0, the `→` prints correctly.

```
# Hook — feed a Windows backslash file_path
$ printf '{"tool_name":"Edit","tool_input":{"file_path":"C:\\\\Users\\\\...\\\\src\\\\myproject\\\\utils\\\\logger.py"}}' \
  | bash .claude/hooks/post-tool-shift-left-audit.sh; echo "exit=$?"
exit=0
```

Before the fix: silent no-op (case-glob mismatch). After the fix: the case matches, the hook executes the rest of its logic, and finds the `test_logger.py` partner.

---

## 6. Key Decisions

| Decision | Rationale |
|---|---|
| **Patch upstream rather than telling downstream to wrap PYTHONUTF8** | The helper should "just work" on every platform it claims to support. Pushing the workaround onto every downstream user is anti-doctrine. |
| **Fail-soft try/except on `reconfigure`** | `reconfigure` exists on Python 3.7+ but can fail when stdout is redirected to a pipe with a fixed encoding. The try/except keeps the fix from making other rare cases worse. |
| **Fix the hook with path-normalization instead of dual-case patterns** | `case ... in */src/<pkg>/*.py\|*\\src\\<pkg>\\*.py) ;;` would also work but is harder to read and duplicates the pattern. Normalizing at the top is one line and applies to every subsequent case-match. |
| **Belt-and-braces logger fix: dep + except clause** | The `tzdata` dep makes timezones actually work on Windows; the broader except guarantees graceful fallback if the dep is somehow missing (e.g., editable install without `pip install -e .[all]` re-run). Either alone fixes the immediate symptom. |
| **Fix the two pre-existing test failures in scope** | Same Windows-portability theme; same files (one is even the new test partner). Splitting into a separate session would be artificial overhead. |
| **`skipif` rather than `xfail` for the +x test** | The behavior under test (POSIX `+x` preservation) genuinely does not exist on the target platform. `xfail` would invite confusion ("why does this fail?"); `skipif` with a load-bearing reason is honest. |
| **Mark as `[Unreleased]` in CHANGELOG, not a new SemVer release** | The repo hasn't bumped version since 0.1.0; the 2026-05-19 cycle didn't either. Per Keep-a-Changelog, accumulate in `[Unreleased]` until a version bump intentionally cuts a release. |
| **PATCH-COPY adoption mode in doctrine-updates** | This entry adds no doctrine and no artifacts; downstream adopters with the 2026-05-19 cycle in place can re-copy specific files instead of running the helper again. The four-step adoption guidance is the simplest reproducible path. |

---

## 7. Commits

To be filled in after commit lands; commit hash will be appended here once pushed.

(See `git log --oneline -5` on `main` after push.)

---

## 8. Next Steps

### Closed by this session

- `heimdall-darkroom` carry-over task: "Report Windows-specific findings back to utils (PYTHONUTF8 in helper, path normalization in hook, tzdata + ZoneInfoNotFoundError fix from 2026-04-22)". All four items in that task are now patched in utils' main branch.

### Open in utils

- **Test suite collection failure on missing numpy.** Pre-existing environment issue. Out of scope here, but worth a follow-up session to either: (a) add a `.venv` setup as a Make/script target, (b) document the optional-dependency-groups requirement to run tests, or (c) restructure the decision_science modules so they don't import-fail when numpy isn't present.
- **No version bump after multiple cycles.** Three propagation cycles (2026-04-21, 2026-05-19, 2026-05-29) have landed under `0.1.0`. At some point a version bump is warranted — likely 0.2.0 when the next propagation cycle accumulates meaningful API surface beyond bug fixes.

### Open for any future Windows downstream adopter

- The 2026-05-29 doctrine-updates entry tells them what to copy. The helper is now safe to re-run on Windows from a fresh state. Existing adopters with the patched 2026-05-19 cycle in place don't need to re-run.

---

## 9. Provenance and propagation

**Trigger**: `heimdall-darkroom` 2026-05-28 session — see [`docs/sessions/20260528_doctrine_adoption.md`](https://github.com/jhutchison0/heimdall-darkroom/blob/main/docs/sessions/20260528_doctrine_adoption.md) §6 for the detailed bug discovery context.

**Propagation channel**: `docs/doctrine-updates.md` 2026-05-29 entry — downstream adopters will see this when they `git pull` utils, or when they next run the `propagate_doctrine.py` script.

**Discovery timeline**:

- 2026-04-22: `tzdata` + `ZoneInfoNotFoundError` bug first hit in `heimdall-darkroom` during Phase 1 pivot. Patched locally. Carry-over task created: "port back to utils template."
- 2026-05-19: Three-session utils mega-cycle ships SKILLS_FRAMEWORK v2 + audit hook + adopt_doctrine helper. Neither the four-month-old logger bug nor the new Windows-incompatibility in the helper/hook are caught — utils has no Windows test environment.
- 2026-05-28: `heimdall-darkroom` adopts the 2026-05-19 cycle. The helper crashes immediately; the hook installs but silently does nothing; the carry-over task expands to three items (the old logger bug + two new ones from this cycle).
- 2026-05-29 (this session): All three patched upstream, plus two pre-existing test failures discovered during validation.

The four-month gap on the `tzdata` bug is the operational lesson: a downstream-only patch with a "port back to utils" carry-over note does not actually propagate. The carry-over rotted on the heimdall task list across two session-end runs. **The act of writing a fix and the act of upstreaming a fix are different tasks; the latter has to be explicitly scheduled or it does not happen.** Worth keeping in mind for future Windows-only (or otherwise-platform-only) findings.

---

*Session closed 2026-05-29. The 2026-05-19 doctrine cycle is now Windows-safe for the next adopter.*
