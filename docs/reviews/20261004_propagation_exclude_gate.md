# Review: Propagation exclusion gate (`topic/propagation-exclude-assay`)

**Author**: code-reviewer
**Date**: 2026-10-04
**Type**: Code review

Scope: `git diff main..HEAD`, commits `ef13e2b` and `56fb8e8`.

The exclusion works as configured today, but a plausible config edit can switch it off without any signal. In a live run, a dry run, and a `--since` run, `github/assay` gets no notification and no mark. On this machine the real dry run prints the skip line and makes no writes. The gaps are in what happens when the config is wrong. A one-entry list written as a scalar turns the guard off, and the pin test still passes. An entry that matches no repo is silent, so a trailing slash or a typo sends to the mirror with no warning. Neither is live now. Both cost a few lines to close.

## Write paths into an excluded repo

Probes ran on scratch trees under the session scratchpad: a hub, `github/assay`, and one other repo, with `TACSOP_ROOT`, `PROJECTS_DIR`, and `DOCTRINE_FILE` patched and `main([...])` run live.

| Path | Result | Matters? |
|---|---|---|
| Live run, `- github/assay` | skipped; nothing written under the repo | covered by the test at 206 |
| Dry run | skipped; real dry run made 0 write-mode opens | covered by the test at 220 |
| `--since 2026-01-01` | skipped; nothing written | same loop, same skip |
| A repo nested inside the excluded one | discovery keeps only the outer repo, which is skipped; nothing written | no |
| Excluded repo nested inside another discovered repo | discovery drops it; only the outer repo's own `.claude/` is written | no |
| Excluded repo loses its own `.claude/commands/` but holds a nested repo that has one | the nested repo is written (`vendor/tmpl/.claude/upstream-update.md` and the mark) | hypothetical (S1) |
| `github/assay/`, `./github/assay`, `github\assay`, absolute path, `~/projects/github/assay`, `github/Assay`, a typo | no match; notification and mark written; no warning | yes, the silent mismatch is W2 |
| Symlink elsewhere under `~/projects` pointing at the repo | not discovered (Python 3.12 `rglob` does not follow it); nothing written | no |
| `~/projects` itself a symlink | by code reading: `PROJECTS_DIR` derives from `Path(__file__).resolve()`, so `rglob` and `relative_to` both use the resolved root, and `rel` matches | no |
| Hub cloned one level shallower (root becomes `~`) | `rel` is `projects/github/assay`; no match; written | hypothetical here, since the real dry run prints the skip; part of W2 |
| Windows hub | `rel.as_posix()` gives `github/assay`, so the config value matches; the printed `[skip]` and `[dry-run]` lines show `github\assay` | S2 |

Evidence: `.venv/bin/python scratchpad/probe.py` printed `files written under assay: []` for the baseline, `--since`, nested, and symlink-alias rows, and `['.claude/doctrine-delivered', '.claude/upstream-update.md']` for each of the seven mismatched forms, the shallower hub, and the config failures marked open below.

## Config read: fail open or closed

| Config state | Behavior | Right for a write guard? |
|---|---|---|
| No `config/project.yaml` | open: sends to every repo | Acceptable. The file is tracked, and the pin test reads it. Refusing here would make every test that patches `TACSOP_ROOT` (9 sites) write a config first. |
| No `propagation` key, `propagation:` null, `exclude: []` | open | Yes, if absence means "no exclusions declared". The pin test holds the hub's own entry, and template-derived projects carry no list. |
| `exclude: github/assay` (a scalar) | **open**: `set("github/assay")` is a set of characters | No (W1) |
| Malformed YAML | closed: `ParserError` traceback, exit 1, nothing written | Right outcome, wrong form (W1) |
| `propagation: github/assay` | closed: `AttributeError` traceback | Right outcome, wrong form |
| `exclude: [{path: github/assay}]` | closed: `TypeError: unhashable type: 'dict'` traceback | Right outcome, wrong form |

Every closed case is closed only because `excluded_repos()` runs before the loop (line 211) and the exception escapes `main()`, which catches `ValueError` alone. For a guard against writes, the rule should be this. An absent list means no exclusions. A list that is present but unparseable or the wrong shape refuses the run with `Refused, nothing written: ...`.

## Critical

None. No path writes into `github/assay` under the config as committed.

## Warnings

**W1. A scalar `exclude:` switches the guard off, and the pin test still passes.** `scripts/propagate_doctrine.py:69`, `tests/unit/test_propagate_doctrine.py:692-699`.

`exclude: github/assay` is a natural slip for a one-entry list. `set()` of a string is a set of its characters, so nothing matches and the mirror is sent to. The pin test parses the YAML itself and asserts `"github/assay" in exclude`. On a string, `in` is a substring test, so the test passes. The script's reader and the test's reader disagree. The test name says "never writes into", but the test checks the YAML text only.

Evidence: mutant M11 (`  exclude: github/assay` in `config/project.yaml`) in a scratch export: `SURVIVED [] | 60 passed`. Probe f: exit 0, `files written under assay: ['.claude/doctrine-delivered', '.claude/upstream-update.md']`.

Fix: validate the shape and refuse on anything else (add `PurePosixPath` to the `pathlib` import). Pin through the reader.

```python
def excluded_repos() -> set[str]:
    config = TACSOP_ROOT / "config" / "project.yaml"
    if not config.exists():
        return set()
    try:
        data = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as err:
        raise ValueError(f"cannot read propagation.exclude from {config}: {err}") from None
    section = data.get("propagation") or {} if isinstance(data, dict) else None
    exclude = section.get("exclude") or [] if isinstance(section, dict) else None
    if not isinstance(exclude, list) or not all(isinstance(e, str) for e in exclude):
        raise ValueError("propagation.exclude must be a list of paths relative to ~/projects")
    return {PurePosixPath(e.strip().replace("\\", "/")).as_posix() for e in exclude}
```

```python
def test_the_hub_never_writes_into_the_assay_mirror():
    assert "github/assay" in propagate_doctrine.excluded_repos()
```

Evidence: with that pin test in a scratch copy and the scalar config, `AssertionError: assert 'github/assay' in {'/', 'a', 'b', 'g', 'h', 'i', ...}`. With the committed config: `1 passed`. The normalization maps `github/assay/`, `./github/assay`, `github\assay`, and ` github/assay ` to `github/assay`. The reader snippet, run in scratch as printed here, refuses a scalar list, malformed YAML, a scalar `propagation`, a dict entry, and a top-level list. It returns an empty set for a missing file, no key, null, and `[]`, and `{'github/assay'}` for `- ./github/assay/`. Add one test per refusal: scalar list and malformed YAML.

**W2. An entry that matches no repo is silent.** `scripts/propagate_doctrine.py:215`, `docs/propagation-protocol.md:62`.

The match is an exact string comparison. Each of these forms sends to the mirror with no line that says the exclusion missed: a trailing slash, a leading `./`, a backslash, an absolute path, a `~/projects/` prefix, a case difference, or a typo. The backslash form matters because the config comment and protocol line 80 say to use "the form a dry run prints", and a Windows dry run prints `github\assay`. A hub cloned at another depth misses the same way, since the root is the hub's grandparent and not literally `~/projects`. The guard against all of these is Focus item 2 (`docs/tasks.md:8`): "The dry run must print `[skip] github/assay` before the live run." That holds for the next cycle only, and `/session-end` rewrites the Focus.

Fix, in two parts.
1. Code: before the loop, print a `[warn]` line for each entry that matches no discovered repo. Do not refuse, since a box without the mirror cloned has a legitimate unmatched entry.
   ```python
   found = {r.relative_to(PROJECTS_DIR).as_posix() for r in repos}
   for e in sorted(excluded - found):
       print(f"[warn] propagation.exclude {e}: matches no repo discovered under {PROJECTS_DIR}")
   ```
2. Protocol step 3 (line 62): make the Focus rule standing. Add: "Confirm that each `propagation.exclude` entry for a repo on this machine prints a `[skip]` line. A `[warn]` line means the entry matched nothing."

**W3. Claims without `Evidence:` lines.** Per the verifying-claims skill, these claims need an `Evidence:` or `UNVERIFIED:` line:
- `ef13e2b`: "three tests, all red before the change"; "The dry run on Nidhogg exits 0 with 19 [dry-run] lines and one [skip] line for github/assay"; "no notification on the machine is newer than 15:42 today"; "Suite: 523 passed."
- `docs/tasks.md:77`: "Three tests, red first."; "The dry run on Nidhogg printed the skip line for `github/assay` and wrote nothing."

My re-runs:
- Dry run: holds. Evidence: the real `--dry-run` run under a Python audit hook gave exit 0, 20 lines (19 `[dry-run]`, 1 `[skip]`, 0 `FAILED`), the line `[skip] github/assay: excluded by config/project.yaml propagation.exclude`, 0 `[dry-run]` lines naming `github/assay`, and 0 write-mode opens. The hook caught 1 of 1 writes on a canary file.
- Suite: holds. Evidence: `.venv/bin/pytest -p no:cacheprovider --basetemp=<scratch>` gave `523 passed, 1 warning`.
- "Red first": consistent with the code. The no-skip mutant M1 and the config mutant M9 each fail a new test. UNVERIFIABLE from history, because one commit holds both the tests and the change.
- "No notification newer than 15:42": UNVERIFIABLE. Re-running it needs a scan of `~/projects`, which this review may not do.

The claims that could be re-run hold, so the problem is format, not substance. Fix: put `Evidence:` lines in the merge commit message and on the Completed line.

## Suggestions

**S1. Match on the path and every parent.** `scripts/propagate_doctrine.py:215`. The nested-repo row above is hypothetical, and the fix is one line: skip when `PurePosixPath(rel.as_posix())` equals an entry or has the entry among its `parents`. With this, nothing under an excluded path is written, whatever discovery finds there.

**S2. Print the form the config uses.** `scripts/propagate_doctrine.py:216` and `:231` print `str(rel)`, which shows backslashes on Windows. Print `rel.as_posix()` instead, so "the form a dry run prints" is the config form on every OS. On Linux nothing tests the `as_posix()` call. Evidence: mutant M5 (`str(rel) in excluded`) gave `SURVIVED | 60 passed`. With W1's normalization this no longer matters for matching.

**S3. State the limit precisely.** `docs/propagation-protocol.md:80`, `docs/tasks.md:77`, and `56fb8e8` say an exclusion "matches one machine's layout". The scope is in fact the layout, not one machine. The match is exact. The root is the directory two levels above the hub. A second clone on the same machine is not excluded either. Suggested wording: "A path matches only where the repo sits at that path under the directory two levels above the hub (`~/projects` when the hub is at `~/projects/github/tacsop`). A clone under any other path, on this machine or another, is not excluded."

**S4. Stale example.** `docs/propagation-protocol.md:130` still uses "requires `propagate_doctrine.py` v2 with the new opt-out flag" as its example. Line 85 now rejects an opt-out mechanism of that kind. Swap the example for "requires `propagate_doctrine.py` with `propagation.exclude`".

## Tests: can each fail?

Eleven mutants ran in a scratch export of HEAD.

| Mutant | Result |
|---|---|
| M1 remove the skip block | killed (test at 206) |
| M2 skip in live runs only | killed (test at 220) |
| M3 print the skip line but fall through | killed (206) |
| M4 `excluded_repos()` returns `set()` | killed (206) |
| M5 `str(rel)` for `as_posix()` | survived (Linux; S2) |
| M6 write a mark, then skip | killed (206) |
| M7 key typo `excludes` in the script | killed (206) |
| M8 skip in dry runs only | killed (206) |
| M9 config drops `github/assay` | killed (pin test) |
| M10 config `github/assay/` | killed (pin test) |
| M11 config scalar `exclude: github/assay` | **survived** (W1) |

Evidence: `scratchpad/mutate.py` output, one line per mutant, as tabled.

## Prose and other checks

- No em dashes in added lines or commit messages. Evidence: `git diff main..HEAD | grep '^+' | grep -c '—'` gives 0, and the same count on `git log --format=%B main..HEAD` gives 0.
- Private-term list (5 terms): 0 hits in added diff lines and 0 in the branch's commit messages. Evidence: a count-only `grep -c -i -F -f` over each.
- The hub's working tree was unchanged by this review apart from this report. Evidence: `git status --porcelain | wc -l` gave 0 before the report was written.

Verdict: GO-WITH-FIXES

Critical: 0, Warning: 3, Suggestion: 4

## Disposition (lead, 2026-10-04)

| Finding | Disposition |
|---|---|
| W1 | Applied. `excluded_repos()` returns no exclusions only when the list is absent; a present list that is a single value, not a mapping, or unparseable YAML raises `ValueError`, and `main()` prints `Refused, nothing written`. Entries are normalized (whitespace, `./`, trailing `/`, backslashes, case). The hub pin reads through `excluded_repos()`. Test-first: 3 refusal cases and 4 slip cases red, then green; M11 (the hub config as a single value) now fails 1 test in a scratch export. |
| W2 | Applied. Before the loop, each entry that matches no discovered repo prints `[warn] <entry>: in propagation.exclude, but no discovered repo is at or under it`, and the run goes on. Protocol Cycle Anatomy step 3 says to resolve any `[warn]` before step 4. Test red, then green. The real dry run prints no `[warn]`. |
| W3 | Applied in the hand-back and the session doc: each claim carries its command and output. "Red first" is reported as seen in the session, not provable from the commits, which hold test and change together. |
| S1 | Applied: a repo at or under an excluded path is skipped. Test red, then green. |
| S2 | Applied: `rel` is computed once as `as_posix()` and used in every printed line. A Linux test cannot kill M5; accepted. |
| S3 | Applied: the protocol and the Completed line say the match is a path under the root two levels above the hub checkout, and a second clone at another path, on this machine or another, is not excluded. |
| S4 | Applied: the Version Coordination example no longer mentions an opt-out flag. |

No second round: 0 Critical, and each Warning's fix was checked by the command or test named in its row. Suite after the fixes: 532 passed (540 with the traversal fixes that follow).
