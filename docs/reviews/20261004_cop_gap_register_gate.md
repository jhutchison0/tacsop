# Review: Gate, `topic/cop-gap-register` (the hub's first slice of the common operating picture)

**Author**: code-reviewer
**Date**: 2026-10-04
**Type**: Code review (merge gate)

Verdict: GO-WITH-FIXES. The register, the module and the test do what slice 1 asks, every fact in the five gap rows checks out, and every number in the commit messages re-runs. Six findings need fixing before the doctrine entry is sent. The padding defence lets "None exists." through, and that phrase opens three of the register's own collector cells. The amended entry tells consumers that `adopt_doctrine.py` delivers `session-end.md`, but the script never overwrites an existing file. The entry's copy instruction names the wrong test. Its rollback leaves a test that the rollback itself turns red. One task and one commit message claim command done-conditions that two slices do not have. And several claims carry no `Evidence:` line.

Scope: `git diff main..HEAD` (87e9009, 87c3661, 4e0d718). I ran every probe against string input or in scratch exports of each commit (`git archive`, with a `.venv` symlink, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, `--basetemp` in scratch). Only this file was written in the repo. I did not read any other repository, and I did not run `propagate_doctrine.py --dry-run`, because it reads consumer marks in other repositories.

## Critical

None.

## Warnings

**W1. The padding defence accepts fillers, including the one the register itself invites** (`src/myproject/utils/gaps.py:18`, `:52`; claim at `docs/gaps.md:5`).
The filler check compares the lowercased cell to six exact strings. `None exists.` passes, and it is the opening phrase of the G1, G2 and G3 collector cells. So do `None.`, `TBD.`, `—`, `` `none` ``, `*TBD*`, `unknown`, `nothing` and `N/A (later)`. Rule 5's two fields are the skill's only defence against a padded list (`SKILL.md:144-145`). `docs/gaps.md:5` says the test "fails ... when an open row lacks either field".
Evidence: `problems()` on the HEAD register with G1's collector set to `None exists.` and its decision to `TBD.` returns `[]`. The same holds for `None.` and `—`.
Fix (tested in a scratch export: 25 passed; the four new cases fail against HEAD's module):

```python
FILLERS = {"tbd", "none", "none exists", "n/a", "unknown", "nothing"}

def _says_nothing(cell: str) -> bool:
    """True when a cell, stripped of punctuation and markup, names nothing."""
    words = re.sub(r"[^a-z0-9/]+", " ", cell.lower()).split()
    return not words or " ".join(words) in FILLERS
```

Use `if _says_nothing(row[key])` at `:52`, and add `"None exists."`, `"TBD."`, `"—"` and `` "`none`" `` to the parameters at `tests/unit/test_gaps.py:58`.

**W2. Row 5 says `adopt_doctrine.py` copies `session-end.md`; it skips that file in every consumer that already has one** (`docs/doctrine-updates.md:55`, `:68-70`; the rationale in commit 4e0d718).
`scripts/adopt_doctrine.py:102` says "Never overwrites", and `:117-121` skips any target that exists. A repo bootstrapped from this template has `.claude/commands/session-end.md`. A maintainer who follows Action required steps 1 and 3 deletes `known_issues` (row 4) and keeps a Step 4.5 that writes the key back at the next `/session-end`. If they copied `test_gaps.py`, it then fails. The amendment was still right, for a different reason: the entry is the only notice a consumer gets, because the script will not deliver the file.
Evidence: a dry run from a scratch consumer that already has `session-end.md` (`adopt_doctrine.py --upstream <scratch HEAD export> --package foo --dry-run`) prints `[skip] .claude/commands/session-end.md — already exists; review by hand`.
Fix: in row 5, write "PATCH both by hand: `adopt_doctrine.py` skips `session-end.md` when it exists. Copy the hub's Step 4.5 `docs/gaps.md` bullet." In step 3, write "patch `/session-end` Step 4.5 and `/sitrep`". The branch is unpushed, so the 4e0d718 message can be corrected too if the lead wants.

**W3. Row 3's copy instruction names the wrong test and holds for one layout only** (`docs/doctrine-updates.md:53`).
"The last test's parameters" means the command parameters, and those belong to `test_known_unknowns_live_only_in_the_register`. That test is the second of ten (`tests/unit/test_gaps.py:30-31`). The last test (`:84-91`) has no command parameter. I copied the module and the test into scratch consumers:
- Template layout (`src/foo/utils/`, `src/__init__.py`, `pythonpath = ["."]`), import renamed only: 21 passed.
- Package without `utils/` (`src/foo/gaps.py`): 3 failed with `FileNotFoundError`, because `gaps.py:11`'s `parents[3]` resolves one directory above the repo.
- `state:` present with no value: 2 failed with `TypeError` at `test_gaps.py:36`.
- The header's first words are load-bearing. Renaming "Collector that would close it" to "What would close it" raises `KeyError: 'collector'`, which conflicts with "The rows are yours" unless the entry says to keep the header.

Rewrite the notes: "The rows are yours; keep the header. Both files copy unchanged into a repo laid out like the template (`src/<pkg>/utils/`, tests importing `src.<pkg>`): change the package name in the test's import, and cut `test_known_unknowns_live_only_in_the_register`'s parameters to the commands your repo has. Another layout changes `parents[3]` in `gaps.py`."

**W4. Rollback and Reversible turn the copied test red** (`docs/doctrine-updates.md:33-34`, `:74-76`).
Both lines say to restore `known_issues` and revert Step 4.5. Neither says to remove `test_known_unknowns_live_only_in_the_register`, which fails on exactly that.
Evidence: in a scratch export of HEAD, re-adding `state.known_issues` gives `2 failed, 19 passed`, and restoring the `known_issues` bullet in `session-end.md` gives `1 failed, 20 passed`.
Fix: append "and delete `test_known_unknowns_live_only_in_the_register`, or remove `docs/gaps.md`, `gaps.py` and `test_gaps.py` together."

**W5. Two of the three planned slices lack a command done-condition, and commit 4e0d718 says each has one** (`docs/tasks.md:8`).
Slice 2 has a command (`grep -c ... prints 0`; it prints 2 today). Slice 3 has no done-condition at all. Slice 4's "a test renders the picture over an empty report root and asserts no line reads clean" is observable but names no command. The skill puts the executable form first (`SKILL.md:125-129`). That matters most for slice 3, whose subject is done-conditions as commands.
Fix: slice 3, "Done when `grep -c -E '^- \[ \]' docs/tasks.md` equals the count of open tasks carrying `Done when \``, over the scope the forward-only decision sets." Slice 4, "Done when `.venv/bin/pytest -q -k empty_root` prints `1 passed` and fails with the probe removed."

**W6. Claims with neither an `Evidence:` line nor `UNVERIFIED:`** (Claim Style rule 4).
I re-ran every check below that can be re-run; only W2's and W5's claims failed.

| Claim | Where | Re-run |
|---|---|---|
| "Suite: 19 in test_gaps.py, all passing" | 87e9009 | 19 passed at 87e9009 |
| "Suite: 483 passed (462 before the branch)" | 87c3661 | main 462 passed; 87e9009 481; 87c3661 483; HEAD 483 |
| "was red on both" | 87c3661 | HEAD's test against the 87e9009 tree: 2 failed at `test_gaps.py:36` |
| "21 tests" | `CHANGELOG.md:28` | 21 passed |
| "each red before green" / "each behavior red first" | 87e9009, `CHANGELOG.md:28` | UNVERIFIABLE (below) |
| "adopt_doctrine.py copies session-end.md downstream" | 4e0d718 | refuted (W2) |
| "each done-condition a command and the output" | 4e0d718 | refuted for slices 3 and 4 (W5) |
| "fails ... when an open row lacks either field" | `docs/gaps.md:5` | refuted for fillers (W1) |

For the red-first claim, the honest line is `UNVERIFIED: no collector records test-before-code order (gap G1)`. The CHANGELOG asserts the very thing G1 says nobody can see.

## Suggestions

**S1. Six of 22 mutants survive; two of them matter** (`gaps.py:28`; `tests/unit/test_gaps.py:71`).
- M3 drops the `$` from `STATUS`. Under it, a Status of `opened` or `open (narrowed)` matches but is not `== "open"`, so the row escapes both the field checks and the status check. That is the case the comment at `test_gaps.py:76-77` says the test guards.
- M11 replaces the date with `\S+`, which accepts `closed today by G3`.
- Adding `"opened"` and `"closed today by G3"` to the status parameters kills both. In scratch, HEAD passes 23; M3 and M11 each fail 1.
- The other four survivors are benign. M1 and M4 change only which message prints. M2 checks fields on closed rows too, which is stricter. M9 drops indented tables, and the register has none.

**S2. A fenced example row can satisfy the never-empty rule** (`gaps.py:56-66`).
Placed after a table whose rows are all closed, a fenced example row with Status `open` returns `[]`. That is hypothetical here, since `docs/gaps.md` has no fence. It is plausible in a consumer's copy that adds a "Row format" example. Rows before the header, or a renamed header, raise `KeyError` rather than report a problem. Fix: skip lines inside fences, take the header as the line above the separator, and report a missing key such as `collector`, `decision`, `status` or `id` as a problem.

**S3. Rule 4's pointer and the "never delete" rule are format-checked only.**
Several inputs pass:
- a duplicate ID
- `superseded 2026-10-04 by G99` when no G99 row exists
- an empty Gap cell on an open row
- `closed 2026-13-45 by x`

The cheapest worthwhile additions are the Gap cell as a third required field and unique IDs. An ID-contiguity check (G1 to Gn, no hole) would catch a deleted middle row, the one deletion a text-only test can see.

**S4. Three decision cells could name better decisions** (`docs/gaps.md:10-12`).
- G2's cell names the tasks that would build its own collector ("The audit-hook pin (P1) and the Bash blind spot (P2)"), which is circular. A blocked decision: "whether the audit log can stand as test-first evidence for `scripts/` and Bash edits, and whether the hub widens the matcher".
- G3's first clause ("What the fleet ledger is") has the same problem. Its second clause already names a real decision, so drop the first.
- G4 says the blocked decision is whether `ISOLATION.md` "may say the wire is armed only while a test runs". `.claude/skills/shift-left-testing/ISOLATION.md:48` says that now. Rewrite: "Whether ISOLATION.md:48's 'armed only while a test runs', stated today with no test behind it, stays, and whether release entry C repeats it."

**S5. The `/sitrep` pin passes on the output heading alone** (`tests/unit/test_gaps.py:38-39`; `.claude/commands/sitrep.md:13`, `:63`).
Replacing the Sources line `docs/gaps.md` with another path leaves 21 passed, because `GAPS (open rows in docs/gaps.md):` still matches. Assert on the "Sources to Read" section instead. Separately, `KNOWN ISSUES` (`:60`, guidance at `:36`, `:81`) lost its source with the key; say it lists the defects tracked in `docs/tasks.md`.

**S6. Step 4.5 writes the register after the only test run** (`.claude/commands/session-end.md:50`).
Step 2 (`:10`) runs `/pcc`, Step 3 commits, and Step 4.5 edits `docs/gaps.md` and amends. The hub has no CI, so a malformed row stays in until the next session's `/pcc`. The bullet also lumps the close and supersede cases together without the exact Status form. Rewrite: "...set its Status to `closed YYYY-MM-DD by <pointer>` when a collector now covers it or a measurement found it absent, or `superseded YYYY-MM-DD by <row>` when a newer row restates it; never delete a row. Then run `.venv/bin/pytest tests/unit/test_gaps.py -q`."

**S7. The entry, the skill and the P1 tell three slightly different stories** (`docs/doctrine-updates.md:54`, `:68`; `ADOPTION.md:96-110`; `docs/tasks.md:8`).
- Row 4 is labelled CONDITIONAL but states no condition, and Action step 3 makes the move unconditional.
- Row 4 names two dispositions (gap, task). The hub's own migration needed four: a decision goes to the record, and an operating note goes to the command it governs.
- `ADOPTION.md`'s first slice is still a register and one test, with the config shrinking at slice 2. A reader of the skill alone will repeat the original DEFER.
- The P1 renumbers ADOPTION.md's slices: ADOPTION.md's slice 3 is the probe, and the P1's slice 4 is the probe.

Fix: give row 4 the condition "where the config carries a known-issues list" and add the two dispositions. Consider a one-line note in `ADOPTION.md` (0.1.1). Say in the P1 that its numbering departs from ADOPTION.md.

**S8. `test_gaps.py:35` raises `TypeError` when `state:` has no value.**
That will be the hub's own state at slice 2 if `config/project.yaml:88`'s comment is left under an otherwise empty `state:`. Use `.get("state") or {}`.

**S9. `/session-start` no longer sees known unknowns.**
Step 1 reads the whole config (`.claude/commands/session-start.md:7`), so `known_issues` used to be in view; now Step 1 sees a pointer. Row 6 defers this command, so the command every session runs is the one that skips the register. The smallest step is one summary line, "Gaps: N open in docs/gaps.md". It can wait for slice 2.

## Answers to the brief

### 1. `problems()` on inputs a maintained file will see

| Input | Result | For this register |
|---|---|---|
| Leading or trailing whitespace; a table indented 2 spaces | handled | no effect |
| CRLF | handled (`splitlines`) | no effect |
| `\|` in a cell | loud: "has 7 cells where the header has 6 (a \| inside a cell?)" | matters; G2's author already wrote around `Write\|Edit`, and the check works |
| Escaped `\|` (legal in GFM) | loud false positive | hypothetical; `docs/gaps.md:5` forbids `\|` |
| Missing or renamed header column | `KeyError` | hypothetical here; matters for consumer copies (W3) |
| A row, or a fenced row, before the header | `KeyError` or a misleading count message | hypothetical; fails loudly |
| A fenced example row after a closed-only table | counted as open; never-empty passes | hypothetical here; plausible downstream (S2) |
| A second table of the same shape | its header row is flagged as a bad status | fails loudly |
| A second table of another shape | cell-count messages | fails loudly |
| A row without outer pipes | silently skipped | hypothetical; GFM renders it as a row |
| A blank line inside the table | the next row still counts | harmless |
| Filler variants | pass | matters (W1) |

### 2. Can every test fail?

Yes. Each of the ten test functions failed under at least one mutant or repo edit. For example, the pin fails when G5's collector becomes `TBD`. The command test fails when `known_issues` returns to the config or to `session-end.md`. The empty-register test fails when the no-table guard is removed. Of 22 module mutants, 16 were killed; S1 covers the survivors. One repo-file mutant survived: removing the `/sitrep` source line (S5).

### 3. Faithfulness to the skill

- **First slice** (`ADOPTION.md:96-103`). The register has entries. The test fails on an empty file (`test_gaps.py:46`; the pin raises if the file is gone), on an entry lacking a field (weakened by W1), and when only superseded entries remain (`:50`). Nothing the slice requires is missing.
- **Rule 4.** Only `open` rows count; mutants M14 and M21 are killed. Closed and superseded marks carry a date and a pointer, but the pointer is not resolved and a deletion is invisible (S3). Deleting the eight config lines in favour of a one-line pointer (`config/project.yaml:88`) is consistent: rule 4 governs register lines, git keeps the block, and ADOPTION.md's config row ends at "identity only".
- **Rule 5.** Both fields are required and the list is never empty. The padding defence is weak (W1).
- **Added beyond the skill.** These are the `closed` form (it matches the two closing paths in `ADOPTION.md:61-63`), the Opened column, the cell-count check, the config-and-commands test, and the two command patches. Each serves the migration. Only the command patches go against the original entry, which deferred them.

### 4. The five gap rows

Every factual statement checks out today. All five rows are gaps in the skill's sense: a known unknown, a collector, a blocked decision. G4 is the closest to a to-do, and G5 is the cleanest.

| Row | Checked | Result |
|---|---|---|
| G1 | The hook logs `MISSING_TEST` or `OK_TEST_EXISTS`, never the order (`post-tool-shift-left-audit.sh:95-107`). Layers 5 and 6 are in `ENFORCEMENT.md:19-20`, the task at `tasks.md:35`. `git log -S soft-deterministic -- config/project.yaml` returns 028ed67, 2026-05-19. | true; Opened matches |
| G2 | Matcher `"Write\|Edit"` at `.claude/settings.json:28`; glob `*/src/myproject/*.py` at hook `:43`; P1 at `tasks.md:47`, P2 at `tasks.md:13`. The config line entered 2026-10-01 (539ba3a); the Bash blind spot was filed 2026-08-24 (eea6cf3). | true; Opened is defensible as first discovery; decision cell is circular (S4) |
| G3 | `propagate_doctrine.py:27` (`PROJECTS_DIR`) and `:41` (`rglob(".claude/commands")`); P1 at `tasks.md:18`, P2 at `tasks.md:48`; dcee439, 2026-08-28. The dropped "20 repos as of 2026-10-02" is a measurement; no tracked file carries it now, which fits the skill's placement rule. | true |
| G4 | M7 (`finally: pass` at `tests/isolation.py:223-224`) in a scratch export: `43 passed`, the same as the baseline. R2-S1 is at review `:480`. Entry C is at release draft `:165`. The review's commits are dated 2026-09-30. | true; decision already taken in ISOLATION.md:48 (S4) |
| G5 | Kernel live in `CLAUDE.md`. 2d is the controlled replay on the work terminal (CONOP `:75`, `:206`; `tasks.md:5`); d1deddc, 2026-10-01. The refutation counts it dropped survive in three records. | true |

The three entries dropped as not gaps each have a home: the `exponential()` defect at `tasks.md:33`, the history decision at `tasks.md:69` (Completed), and fetch-first at `pcc.md:133`.

### 5. The doctrine-entry amendment and the original DEFER

The amendment gets the direction right. It gets the mechanism wrong in row 5 (W2) and the instructions wrong in row 3 (W3), its rollback is incomplete (W4), and row 4 lost its condition (S7).

Moving `known_issues` before slice 2 was sound for the hub. The skill's placement table puts gaps in a maintained register (`ADOPTION.md:12`), and `known_issues` was the gap list's predecessor. The user's decision named shrinking `project.yaml`.

- **Risk of the move.** Slice 1 grows from "a register and one test" to six artifacts per consumer. Two of them are commands the original author deferred until a picture renders. The entry and the shipped skill now describe different first slices. A consumer that follows the entry without the test gets the delete without the pin.
- **Risk of the DEFER.** Every consumer that starts a register keeps `known_issues` beside it, and `/session-end` keeps writing the untested list. Since the real known unknowns would stay in config, the register would likely start with exactly the trivia rule 5 exists to refuse.

On balance the move is the better call. W2 to W4 and S7 make it safe to send.

### 6. Prose and claims

- **Em dashes.** The branch adds one em dash net, at `sitrep.md:13`. It is a list separator matching its five siblings, which `REVIEWING.md` pass 4 exempts. The commit messages contain none.
- **Claims.** W6 covers them.
- **UNVERIFIABLE: red-first per behavior** (87e9009, `CHANGELOG.md:28`). No collector records test-before-code order; that is gap G1. The local audit log shows 9 writes of `src/myproject/utils/gaps.py` on 2026-10-04, all `OK_TEST_EXISTS`, so the test file existed before the module's first write. That is consistent with the claim but does not prove it.
- **UNVERIFIABLE: the 2026-10-04 entry is unsent.** The probe reads consumer marks in other repositories, which is outside this review's scope. The hub's record shows no cycle after fcc094e: no session doc and no commit since then runs one.

## Counts

Verdict: GO-WITH-FIXES. Critical 0, Warning 6, Suggestion 9.

## Disposition (lead, 2026-10-04)

Applied before merge, each reproduced first where it claimed a defect:

| Finding | Disposition |
|---|---|
| W1 | Applied as proposed (`_says_nothing`, a widened filler set). Reproduced first: the HEAD register with G1's collector `None exists.` and decision `TBD.` returned `[]`. Six new cases red, then green. |
| W2 | Applied. Reproduced: `adopt_doctrine.py:117-121` skips any existing target. Row 5 and step 3 now say to patch both commands by hand. The rationale in 4e0d718's message is wrong; the fix commit says so. |
| W3 | Applied in the reviewer's wording, with "keep the header". |
| W4 | Applied: Reversible and Rollback delete `test_known_unknowns_live_only_in_the_register` with the key. |
| W5 | Applied. The P1 now numbers slices as `ADOPTION.md` does; slices 2 and 3 name a command each, and the plans-and-tasks step states its done-condition in the blocked form, naming the instrument. 4e0d718's claim that every done-condition was a command was false; the fix commit says so. |
| W6 | Applied in the hand-back to the user: each claim carries an `Evidence:` line. "Each behavior red first" is reported as observed in the session's tool output and recorded nowhere else, which is gap G1. |
| S1 | Applied: `opened` and `closed today by G3` added. Re-run: M3 (no `$`) and M11 (undated close) both killed, each by its new case. |
| S2 | Declined for now. No fenced block or second table in the hub's register; a missing or renamed column raises, which still fails the pin. Revisit if a consumer reports it. |
| S3 | Declined: duplicate IDs, dangling pointers, empty Gap cells and impossible dates sit outside rule 5's two fields. |
| S4 | Applied: G2 and G3 name decisions their gaps block, not the tasks that would build their collectors; G4 names the open decision (entry C shipping the claim as tested). |
| S5 | Applied: the pin requires `docs/gaps.md` on a list line; with the sources line removed and the heading kept, 1 failed. `/sitrep`'s task-list source now feeds KNOWN ISSUES. |
| S6 | Applied: Step 4.5 gives the three Status forms and says to re-run the register's test after editing. |
| S7 | Applied: row 4 states its condition and the four homes; `ADOPTION.md`'s first slice gains the move as item 3; the skill moves to 0.1.1; the P1 follows `ADOPTION.md`'s numbering. |
| S8 | Applied: `.get("state") or {}`; an empty `state:` in a scratch export gives 29 passed. |
| S9 | Applied to the P1: slice 2's `/session-start` rewrite reports open gaps. |

No second round: 0 Critical, and every Warning's fix was checked by the command named in its row.
