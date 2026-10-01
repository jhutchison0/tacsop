# Review: Doctrine Transport Backlog Gate (`topic/doctrine-transport-backlog`, `c2eb3f2`)

**Author**: code-reviewer
**Date**: 2026-10-01
**Type**: Code review

## Verdict: GO-WITH-FIXES (2 Critical, 7 Warning, 6 Suggestion)

The consumer-side date mark is a sound design, but line 149 of `scripts/propagate_doctrine.py` writes a mark that can claim deliveries that never happened. Two defects lose entries silently and for good. (1) An entry dated the same day as an already-propagated entry never reaches any marked repo. (2) A malformed mark, a `--since` typo, or a run from an older checkout overwrites the mark as if everything had been sent. Fix both before the first real run. Real runs will write marks into 19 repos, and after that the mark format becomes a compatibility problem. Re-gate the fix commit.

Scope of this review: `git diff main...HEAD` (one commit, `c2eb3f2`). Probes ran on scratch trees only. See Scope Confirmation at the end.

## What Holds

- **Write order is right.** The notification is written before the mark (lines 141 to 149). When the notification write fails, no mark is left behind (probe F1 below; a proposed test kills the swapped-order mutant).
- **Dry run and real run agree.** On a six-state scratch fleet (unmarked, marked, partly unread, garbage mark, future mark, empty notification), the two runs produced identical delivery sets in all six cases. They also agree on the wrong answers listed under C2.
- **CRLF is handled.** `read_text()` uses universal newlines. A CRLF hub file parses into 3 entries, and a CRLF unread file dedupes correctly (probe P7).
- **The new tests are real.** All 21 new tests fail against `main`'s script (21 failed, 9 passed). No test is vacuous: `test_a_second_run_delivers_nothing_new` survives M2 and M3 alone but fails when both are applied together.
- **The commit's claims check out.** 16 net new tests (21 added, 5 removed). `CI=1 .venv/bin/pytest -q` gives `367 passed, 1 warning`. The real dry run covers 19 consumers, sends 5 entries to each, and writes 0 marks.
- **Consumers can commit the mark.** `git check-ignore .claude/doctrine-delivered` matches nothing in 19 of 19 consumers, and no consumer's `.claude/` is a symlink.
- **The merge is clean.** `main` is one commit ahead (`2a2e725`, which only touches `tests/unit/test_session_start_checks.py`).
- **The prose is clean mechanically.** Added lines in `docs/propagation-protocol.md` contain 0 em dashes and 0 words from the LANGUAGE.md cruft list.

## Critical

### C1. An entry dated the same day as a propagated entry never ships, and the protocol says it will

`scripts/propagate_doctrine.py:84` (`e[0] > mark`) and `:149` (the mark is a bare date). `docs/propagation-protocol.md:113` says "two entries written on the same day either both go or both wait". `:48` says one cycle carries two entries.

Probe P1 (scratch): hub entry X dated 2026-10-01; run; then entry Y is added, also dated 2026-10-01.

```
--- run2 after adding Y same day
  out: Up to date: github/c1
  headings: ['## 2026-10-01: X first']
  mark: '2026-10-01\n'
--- run3 next day, nothing new
  out: Up to date: github/c1
```

Y is lost for every repo that has a mark, on every future run, because `2026-10-01 > 2026-10-01` is false. A follow-up entry written the same day is a normal event here: the hub already holds two 2026-06-28 entries, and a review round often produces a correction on the day of the original. The dry run shows "Up to date", so nothing warns the maintainer.

**Fix**: store the headings already sent on the mark date alongside the date, and deliver a same-date entry when its heading is not among them. Changing the format costs nothing now because no marks exist yet (`find ~/projects -maxdepth 6 -name doctrine-delivered | wc -l` gives `0`). After the first real run it would cost a migration.

```
2026-10-01
## 2026-10-01: X first
```

### C2. The mark is written unconditionally, from the top entry, over whatever was there

`scripts/propagate_doctrine.py:129` reads the mark with no validation. `:149` then writes `entries[0][0]` for every repo on every real run: whether or not anything was offered, whether or not the old mark parsed, and even if the new value is older than the old one. A mark then claims "everything up to this date was sent" when it was not. Every case below ran on scratch trees, with hub entries C 2026-09-18, B 2026-08-30, A 2026-08-21.

**Malformed marks (P4).** Every case sends nothing and then overwrites the mark with the hub's date:

```
  garbage        sent=[] newmark='2026-09-18\n'
  unpadded       sent=[] newmark='2026-09-18\n'     (mark was "2026-8-21")
  BOM            sent=[] newmark='2026-09-18\n'     (mark was "﻿2026-08-21")
  conflict       sent=[] newmark='2026-09-18\n'     (mark held git conflict markers)
  future         sent=[] newmark='2026-09-18\n'     (mark was "2027-01-01")
```

A conflicted mark is plausible, because the protocol asks consumers to commit the mark (`docs/propagation-protocol.md:111`) and two machines can both write it. `--since` is validated (`:152` to `:160`) but the mark, which matters more, is not.

**A `--since` typo on the first run (P9).** `--since 2026-10-18` (meant 08-18) matches nothing, yet the run marks the repo as delivered. The corrected rerun is then ignored, because a mark wins over `--since`:

```
--- run since 2026-10-18 (meant 08-18)
  out: Up to date: github/c1     mark: '2026-09-18\n'
--- rerun with correct since 08-18
  out: Up to date: github/c1     mark: '2026-09-18\n'
```

On the real tree, one typo would close the backlog for all 19 repos without sending a single entry.

**A run from an older checkout moves the mark backward (P3).** The consumer had received C and deleted the notification after review. A run from a checkout that lacks C rewrites the mark to 08-30. The next run from `main` sends C again:

```
--- run on old checkout      out: Up to date: github/c1   mark: '2026-08-30\n'
--- run back on main         out: Notified 1 (2026-09-18) headings: ['## 2026-09-18: C title']
```

This repo does its work on topic branches, and a hub clone on a second machine can lag `main`.

**An entry merged out of date order (P2a).** An entry drafted on a topic branch and dated 09-10 lands on top after 09-18 has shipped. It is never sent, the mark drops to 09-10, and the next run sends the reviewed 09-18 entry again:

```
--- run2 with backdated X on top   out: Up to date          mark: '2026-09-10\n'
--- run3 no doc change             out: Notified 1 (2026-09-18)
```

**Fix** (one rule, about 15 lines). Verified in a scratch sketch (`scratchpad/fixsketch`). With it, 29 of the 30 existing tests pass. The one failure is the mark-format assertion at `tests/unit/test_propagate_doctrine.py:306`, which must change if C1's format lands. All 10 proposed tests pass, and probes P1, P3, P4 and P9 come out right.

```python
def read_mark(mark_file: Path) -> tuple[str | None, frozenset[str]]:
    """(date, headings already sent on that date); raises ValueError if malformed."""
    if not mark_file.exists():
        return None, frozenset()
    lines = mark_file.read_text(encoding="utf-8").splitlines()
    first = lines[0].strip() if lines else ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", first):
        raise ValueError(f"malformed delivery mark {first!r}")
    return first, frozenset(l for l in lines[1:] if l.strip())

# in propagate():
newest = max(d for d, _ in entries)                 # not entries[0][0]
...
if mark and mark > newest:                          # hub behind: refuse, do not regress
    raise ValueError(f"mark {mark} is newer than the hub's newest entry {newest}")
offered = entries_to_deliver(entries, mark, since, "", sent_on_mark)
...
if mark or offered:                                 # a --since that matched nothing writes no mark
    mark_file.write_text(newest + "\n" + "\n".join(newest_heads) + "\n", encoding="utf-8")
```

The sketch does not fix P2b: an entry inserted below the top in date order, after a later entry has shipped, still never ships. That is the limit of any date-based mark. State it in the protocol: "Date an entry the day it lands on `main` and put it on top. Re-date a branch-drafted entry at merge."

## Warning

### W1. The default and the global `--since` cannot express what this fleet holds; the real run would send at least 20 entries that repos already have

`scripts/propagate_doctrine.py:85` to `:88` (one `since` for every unmarked repo; with no `since`, the newest entry only). `docs/propagation-protocol.md:109` says the newest-only default "is right for a repo bootstrapped from the template: it already holds everything older".

The real dry run (`--dry-run --since 2026-08-21`) sends 5 entries to each of 19 repos, 95 deliveries in all. I checked read-only which skill each consumer already holds for each entry: traversing-the-knowledge-base (08-21), designing-clear-data-displays 1.1.0 (08-27), and lake-conventions 1.1.0 (08-29 and 08-30). I also checked for the bare `uv venv` CI defect (09-18):

| Repo (first commit) | Already holds | Sent by `--since 08-21` | Redundant |
|---|---|---|---|
| fist (2026-09-10) | all five; it is the origin of the 09-18 fix | 5 | 5 |
| schelling-point (2026-09-27) | 08-21 to 08-30; its CI has no bare `uv venv` | 5 | 5 |
| stx-server (2026-08-26) | 08-21 to 08-30 | 5 | 4 |
| propter (2026-08-30) | 08-21 to 08-30 (no CI workflow) | 5 | 4 |
| beesly-equilibrium | 08-21, 08-27 | 5 | 2 |
| 14 others | none of the five | 5 each | 0 |

The plain dry run (no `--since`) shows the claim at `:109` failing the other way too. It sends 09-18 to fist and schelling-point, which already hold it: `[dry-run] Would write: .../schelling-point/.claude/upstream-update.md (new): 1 entries (2026-09-18)`. A repo bootstrapped after the newest entry receives that entry again. A repo bootstrapped in the middle of a backlog lacks the entries between its bootstrap and the newest.

Once a real run writes marks, `--since` is inert for those repos (P10: a routine run followed by a `--since 08-21` run gives `Up to date`). The protocol gives no recovery path.

**Fix**: (a) in the protocol, document seeding a mark by hand before the backlog run. For this fleet: `2026-09-18` for fist and schelling-point, `2026-08-30` for stx-server and propter, `2026-08-27` for beesly-equilibrium. With those seeds the run makes 75 deliveries instead of 95, none of them redundant. (b) Document that deleting a repo's mark lets `--since` backfill it, while dedupe keeps unread entries from being sent twice. (c) Have the bootstrap write the mark, so a new repo starts at the hub's newest date. (d) Rewrite `:109` to say which repos the default is right for.

### W2. A dated heading inside a fenced block splits an entry, and under HEAD's mark rule the fragment is sent again after every review

`scripts/propagate_doctrine.py:67` splits on every column-0 `## YYYY-MM-DD:` line, including lines inside code fences. The protocol prescribes headings of this exact shape (`docs/propagation-protocol.md:62`, `:131`), and the real file already carries fenced markdown headings (`docs/doctrine-updates.md:260` `## Step 1.5: Identify the Machine` and `:2044`, both undated today).

Probe P6 used an entry dated 2026-10-01 whose body shows an example heading `## 2026-10-05: REVERT — Old subject` inside a fence:

```
  parsed: [('2026-10-01', '## 2026-10-01: X about reverts'), ('2026-10-05', '## 2026-10-05: REVERT — Old subject'), ...]
--- run1   out: Notified 1 (2026-10-01)   mark: '2026-10-01\n'
--- run2 after review+delete   out: Notified 1 (2026-10-05)   mark: '2026-10-01\n'
--- run3 after review+delete   out: Notified 1 (2026-10-05)   mark: '2026-10-01\n'
```

Run 1 delivers X cut off at an unclosed fence. From then on the fragment goes out again after every review. Under the C2 fix (mark = max date) the loop stops, but the fragment replaces X, and a later real entry with the same heading is falsely skipped (P6b on the sketch: `out: Up to date`).

**Fix**: make the split fence-aware: track fence state line by line and treat `## ` as a heading only outside fences. Checked against the real file: an awk pass finds 0 undated column-0 `## ` lines outside fences and 2 undated ones inside fences, so a fence-aware parser accepts today's file unchanged.

### W3. A typo in a new entry's heading drops the entry silently (a regression), and the protocol's own REVERTED marker glues entries together

`scripts/propagate_doctrine.py:68` to `:71` drop any chunk whose first line fails `^## \d{4}-\d{2}-\d{2}:`.

New top entry with a heading typo, scratch:

```
'2026-10-01 —' [('2026-09-18', '## 2026-09-18: C')] | [dry-run] Up to date: github/c1
'2026-10-1:'   [('2026-09-18', '## 2026-09-18: C')] | [dry-run] Up to date: github/c1
```

`main`'s script shipped the same file's top entry (`extract_latest_entry` returned `'## 2026-10-01 — New top entry\n\nnew body\n'`), so this is a regression. The dry run reports "Up to date" and shows no error.

`docs/propagation-protocol.md:133` tells authors to mark a reverted entry "with `(REVERTED YYYY-MM-DD)` after its date header". If the marker goes between the date and the colon, the entry drops out of the list and its whole text rides inside the newer entry above it:

```
'2026-08-30 (REVERTED 2026-10-05)' -> [('2026-10-05', ...), ('2026-09-18', '## 2026-09-18: C title', True), ('2026-08-21', ...)]
```

(`True` means C's text now contains B's body.) The real file has 0 REVERTED markers today.

**Fix**: refuse to run, and name the line, when a column-0 `## ` line outside a fence after the header fails the dated pattern. Also pin the REVERTED form in the protocol to the end of the subject: `## 2026-08-30: Subject (REVERTED 2026-10-05)`.

### W4. One bad repo stops the run for the rest of the fleet

`scripts/propagate_doctrine.py:125` to `:149` have no per-repo error handling. Probe F1 made the `.claude/` directory of the second of three repos read-only:

```
  out: Notified 3 (...): github/a1
  err: PermissionError [Errno 13] Permission denied: '.../b2/.claude/upstream-update.md'
  b2: headings=[] mark=None
  c3: headings=[] mark=None
```

No mark is left behind (the order is right), and a rerun recovers. But in a 19-repo run, every repo after the bad one is skipped behind a traceback. Probe F3: one non-UTF-8 notification kills both the dry run and the real run before any output (`dry=True: out='' err=UnicodeDecodeError`).

**Fix**: per repo, catch `OSError`, `UnicodeDecodeError` and `ValueError` (which also covers C2's malformed mark), print `FAILED <repo>: <reason>`, continue, and have `main` exit 1. The scratch sketch does this.

### W5. The tests do not pin the two properties the design depends on

I ran one mutant per run on a scratch copy against `tests/unit/test_propagate_doctrine.py` (30 tests):

| Mutant | Result | Caught by |
|---|---|---|
| M1 mark = newest date sent, not the hub's newest | **survived** | none |
| M2 `e[0] > mark` to `>=` | killed | 5 tests, incl. `test_a_reviewed_and_deleted_notification_is_not_resent` |
| M3 dedupe removed | killed | `test_skips_entries_already_in_the_unread_notification` only |
| M4 `e[0] >= since` to `>` | killed | 4 tests |
| M5 newest first instead of oldest first | killed | 4 tests |
| M6 mark written before the notification | **survived** | none |
| M7 mark written only when something was sent | survived | (a design choice, not a defect) |
| M8 dry run writes the mark | killed | `test_dry_run_names_what_each_consumer_would_get_and_writes_nothing` |
| M9 mark read without `.strip()` | survived | (equivalent for well-formed marks) |
| M10 no mark, no since sends everything | killed | `test_with_no_mark_and_no_since_delivers_the_newest_only` |
| M11 `--since` wins over the mark | killed | 3 tests |
| M12 trailing `---` kept in entry text | killed | `test_returns_every_entry_newest_first_with_its_date` |
| M15 append separator dropped | killed | `test_appends_to_existing` |

M1 is the property the `propagate` docstring (`:110` to `:113`) and the protocol (`:107`) state outright. M6 is the failure ordering this gate asked about. Both of these tests pass at HEAD and kill their mutant (verified in scratch):

```python
def test_newest_entry_skipped_as_unread_is_not_resent_after_review(world):
    doctrine, repo = world
    doctrine.write_text(_doc(("2026-03-26", "Second"), ("2026-03-24", "First")))
    (repo / ".claude" / "upstream-update.md").write_text("# U\n\n---\n\n## 2026-03-26: Second\n\nSecond body.\n")
    propagate_doctrine.propagate(since="2026-03-24")
    (repo / ".claude" / "upstream-update.md").unlink()
    propagate_doctrine.propagate()
    assert _note(repo) == ""

def test_a_failed_notification_write_leaves_no_mark(world):
    doctrine, repo = world
    doctrine.write_text(_doc(("2026-03-26", "Second")))
    note = repo / ".claude" / "upstream-update.md"
    note.write_text("# U\n\n---\n\n## 2026-03-01: Old\n\nold\n")
    os.chmod(note, 0o444)  # only the notification fails; a read-only .claude/ blocks both writes and cannot tell the order
    try:
        try:
            propagate_doctrine.propagate()
        except PermissionError:
            pass
    finally:
        os.chmod(note, 0o644)
    assert _mark(repo) is None
```

Add tests for C1, C2 (malformed mark, regression, `--since` past every entry, out-of-order top entry), W2 and W3 as part of their fixes. Each C1 and C2 test fails at HEAD (`scratchpad/proposed_tests.py`: 8 of 10 fail at HEAD; all 10 pass on the sketch).

### W6. The protocol doc makes claims the script does not meet

Each claim below was checked against the script:

| Line | Claim | Measured |
|---|---|---|
| `:44` | "four entries were never sent and three more stacked up behind it" | Four holds: 04-21, 05-29 and both 06-28 entries are absent from all 10 unread files. "Three more" does not: the dry run sends five (08-21, 08-27, 08-29, 08-30, 09-18), and no unread file in the fleet holds 08-21 or 08-29. "It" has no referent. |
| `:44` | "It now sends each repo every entry it has not been sent" | False for unmarked repos without `--since` (P10), for same-day entries (C1), and for backdated entries (P2b). |
| `:46` vs `:48` | Rule 1 title "One propagation cycle = one entry"; bullet "one cycle carries both" | The rule's title now contradicts its own body. |
| `:95` | Append Mode "appends the new entry" | It now appends every due entry. |
| `:107` | "after writing a repo's notification, the script records the date of the hub's newest entry" | It records the top entry's date (`:149`), which differs when the file is out of order (P2a). It also writes the mark when it wrote no notification. |
| `:113` | same-day entries "both go or both wait" | False (C1). |

**Fix**: correct each line, and name dates rather than counts in `:44`. The prose review below gives rewrites.

### W7. `entries_to_deliver` is the only public signature without type hints

`scripts/propagate_doctrine.py:75`: `def entries_to_deliver(entries, mark, since, existing)`. Every other function in the file is annotated.

**Fix**: `entries: list[tuple[str, str]], mark: str | None, since: str | None, existing: str`.

## Suggestion

- **S1. Dry-run output** (`:136`, `:138`). It prints `1 entries`. It prints an absolute path on "Would write" lines but a relative one on "Up to date" lines. It does not show the mark change (`mark: none -> 2026-09-18`), which is the one effect of a real run that cannot be undone. It has no total line (for example `19 repos, 95 entries, 19 marks created`).
- **S2. Contradictory docstrings.** `:78` calls the mark "the newest date this consumer was sent". `:110` to `:113` and the protocol call it the hub's newest date. Use the second wording in both places.
- **S3. Explicit encoding.** The script reads and writes text containing `—` and `→` in the locale encoding (`:63`, `:129`, `:130`, `:144`, `:147`, `:149`). The sibling `scripts/adopt_doctrine.py:29` already forces UTF-8 after a Windows crash (doctrine entry 2026-05-29). Pass `encoding="utf-8"`.
- **S4. Name shadowing.** `:132` `", ".join(date for date, _ in due)` reuses the name of the imported `datetime.date` inside the generator. It is harmless (the generator has its own scope) but misleading next to `_entry_date`. Rename it to `d`.
- **S5. Dedupe is exact-match on the heading line.** A retitled entry (P5) and an editor that strips a trailing space from a heading (P5b) both cause the entry to be sent again under its new form. Real headings have 0 trailing spaces today. Compare `line.rstrip()`, and add to the protocol: "never retitle a propagated entry; amend its body".
- **S6. Consumers will not learn to commit the mark from this protocol.** `docs/propagation-protocol.md:111` says consumers should commit `.claude/doctrine-delivered`, but only that file mentions the mark (`grep -rln doctrine-delivered docs/ .claude/`). The next doctrine entry should carry the instruction. Also record the remaining failure direction: when the notification write succeeds and the mark write fails, the entry goes out once more after review (probe F2: `Notified 1 (2026-09-18)` after delete). A duplicate is the safe direction.

## Prose Review (writing-simple-and-direct, added lines only)

```
[Major] Pass 1 (point): "**Rule 1 — One propagation cycle = one entry.**" (docs/propagation-protocol.md:46)
        now heads a bullet saying one cycle carries both entries (:48).
Rewrite: "**Rule 1 — One entry per change.** If you have two unrelated changes, write two entries,
        or combine them into one when they are coherent or co-dependent. One cycle carries both."
```

```
[Minor] Rule 2 (concrete): "so four entries were never sent and three more stacked up behind it" (:44)
Rewrite: "so 2026-04-21, 2026-05-29 and both 2026-06-28 entries were never sent, and the five entries
        from 2026-08-21 to 2026-09-18 were still unsent on 2026-10-01."
```

```
[Minor] Rule 3 (one idea per sentence): "the repo gets the newest entry only, which is right for a repo
        bootstrapped from the template: it already holds everything older." (:109; also false, see W1)
Rewrite: "the repo gets the newest entry only. That is right only for a repo bootstrapped after the
        second-newest entry and before the newest. Seed the mark by hand for any other repo."
```

```
[Minor] Rule 7 (read it back): "Since the delivery mark, one cycle carries both" (:48). "Since" reads as either "because" or "after".
Rewrite: "With the delivery mark, one cycle carries both; without it, the second waited a full cycle."
```

## Real Dry Run (task item 6)

Command: `.venv/bin/python scripts/propagate_doctrine.py --dry-run --since 2026-08-21`, exit 0. Result: 19 "Would write" lines (10 append, 9 new), each with `5 entries (2026-08-21, 2026-08-27, 2026-08-29, 2026-08-30, 2026-09-18)`. No "Up to date" lines.

A maintainer should expect the shape: the 10 append repos' newest unread entry is 2026-08-03 in every case, so the old script's last delivery was 08-03. The content is not what a maintainer should accept: at least 20 of the 95 deliveries go to repos that already hold the skill (W1 table). The dry run cannot show this, and the script has no per-repo control to prevent it short of seeding marks by hand. Recommended sequence after the fixes: seed the five marks listed in W1, dry run again, and expect 75 deliveries. Then run for real once with `--since 2026-08-21`.

## Scope Confirmation

- I ran the script against the real `~/projects` tree only with `--dry-run`: twice, once with `--since 2026-08-21` and once without.
- Every probe that writes ran on scratch trees under `/tmp/claude-1000/-home-jhutchison-projects-github-tacsop/4e9044e9-74ac-444f-bde7-7aa7f9c8fd81/scratchpad/worlds/`. Each imported a scratch copy of the module (`scratchpad/hubcopy/scripts`) with `PROJECTS_DIR`, `TACSOP_ROOT` and `DOCTRINE_FILE` monkeypatched. Mutants ran in `scratchpad/mut/`.
- My reads of consumer repos were read-only: `cat`/`grep` of notification files, skill `SKILL.md` versions and CI workflows, `git log`, and `git check-ignore`.
- `find ~/projects -maxdepth 4 -name doctrine-delivered` prints nothing. At `-maxdepth 6` the count is `0`.
- Incidental writes outside the scratchpad, disclosed:
  - `.venv/bin/pytest` runs in the hub updated its gitignored `__pycache__/` and `.pytest_cache/`.
  - pytest's `tmp_path` fixtures wrote under `/tmp/pytest-of-jhutchison/`.
  - One `git merge-tree --write-tree main HEAD` added unreferenced objects to the hub's `.git/objects`. No ref changed.
  - I added one agent-memory file (`.claude/agent-memory/code-reviewer/project_doctrine_transport_review_patterns.md`) and one index line in that directory's `MEMORY.md`.
  - Nothing was written to any consumer repo, no cache was cleaned, and no global config changed.
