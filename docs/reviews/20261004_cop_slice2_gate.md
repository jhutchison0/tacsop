# Review: Gate, `topic/cop-slice2-state-block` (the hub's second slice of the common operating picture)

**Author**: code-reviewer
**Date**: 2026-10-04
**Type**: Code review (merge gate)

Verdict: GO-WITH-FIXES. The `state:` block is gone, nothing in code or CI reads it, the tags in `/session-start` match the skill's horizons, and every number in the commit messages and the changelog re-runs. Seven findings need fixing before the merge or before the entry is sent. The Focus section still names slice 2 as the next step while the same branch marks slice 2 done. The doctrine entry says "the entry below" about an entry that a delivered notification prints above it. The count regex misses `53% coverage`, which was half of the README line that motivated it, and the Focus section, the first thing `/session-start` reads, is not checked for counts at all. With the state block gone, "the newest session doc" has no collector: on a fresh clone, Step 3's "most recently modified" picks the March session. Two surfaces still describe the old layout. Several claims carry no `Evidence:` line, though none was refuted.

Scope: `git diff main..HEAD` (0ebd059, 93de829, fe3dd77, 09d42e2, 02b39d6; nothing after). I ran every probe in scratch exports of main, of each commit and of HEAD (`git archive`, a `.venv` symlink, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, `--basetemp` in scratch), and in one scratch `git clone` of the hub. In the repo I ran only read-only commands: `git` reads and `/pcc` check 7, which scanned the 5 unpushed commits and printed nothing. This file is the only one I wrote in the repo. I did not read any other repository, and I did not run `propagate_doctrine.py --dry-run`, because it reads consumer marks in other repositories.

## Critical

None.

## Warnings

**W1. The Focus names slice 2 as the next step, and the same branch marks slice 2 done** (`docs/tasks.md:7`, `:11`; the P1 at `:18`).
Item 1 reads "2026-10-04, on Nidhogg: slice 2 of the hub's common operating picture (this section is part of it), then the `assay` exclusion". Commit 93de829 changed the P1 to "**Slice 2**, done 2026-10-04" and left the Focus as it was. After the merge, the first intent line `/session-start` reports is a step already finished: this is the failure the slice exists to prevent, appearing on the slice's own surface. Item 5's "once 1 to 3 are done" also depends on the numbering.
Fix: in the merge, make item 1 "2026-10-04, on Nidhogg: the `assay` exclusion (P1 below), which gates every propagation run from any box", and make item 5 "once the exclusion, `assay`'s adoption and the propagation cycle are done". Optional: `/session-start` Step 3.5 flags a Focus step whose task is marked done.

**W2. "The entry below" points the wrong way in a delivered notification, and "supersedes row 6" claims more than slice 2 does** (`docs/doctrine-updates.md:9-10`, `:25-26`).
`entries_to_deliver` returns entries oldest first (`scripts/propagate_doctrine.py:155`). The two 2026-10-04 entries are unsent, so they will arrive in one notification with the skill entry first and slice 2 second. Slice 2's "the gap register in the entry below" and "row 6 of the entry below" then point at nothing below them.
Evidence: `extract_entries` on HEAD's file, then `entries_to_deliver` for a mark that holds every heading except the two 2026-10-04 ones, returns `The Common Operating Picture` and then `The State Block Leaves the Config`. In the joined body the skill entry starts at offset 0, slice 2 at 5265, and "the entry below" at 6478.
Row 6 also covers more than slice 2 delivers. It deferred "Rewrites ... once the first repo has rendered a picture", and the `/session-start` rewrite in `ADOPTION.md:70` is "renders the picture". Slice 2 adds tags and two reads; rendering is still slice 3. The entry lifts the deferral without saying why.
Fix: name the other entry by its heading, and say what moves: "This lifts the deferral in row 6 of the 2026-10-04 entry *The Common Operating Picture* for the Focus, the gap-register read and the summary tags in `/session-start`, `/session-end` and `/sitrep`; rendering a picture at `/session-start` waits for slice 3, and `/task brief` stays deferred. It needs that entry's first slice: Step 3.7 reads `docs/gaps.md`."

**W3. The count regex misses half of the README line it was written for, and Detect misses agents** (`tests/unit/test_state_block.py:32`; Detect at `docs/doctrine-updates.md:40`).
The motivating line was `| **Testing** | 189 tests, 53% coverage, pytest-cov configured |`. Coverage now measures 73%, so `53%` was as stale as `189`, and the regex cannot see it. It also misses this hub's own phrasing, "Propagated to 15 downstream repos" (`CHANGELOG.md`), along with `491 passing tests`, `5 unit tests`, `20 repositories` and `508 passed`. Detect's grep omits `agents?`, which row 7 and the test both include, so it misses main's `README.md:18` ("4 agents"). Neither can see the other class the skill names at `maintaining-project-context/SKILL.md:44`, a "most recent" with a date (mutant B below).
Evidence: README mutants `53% coverage` and "reached 16 downstream repos" leave all 14 tests passing. `.venv/bin/pytest --cov` at HEAD: `TOTAL 680 182 73%`. Detect run against main's tree prints README.md:19, :85, CONTEXT.md:34, :35, :67 and LANGUAGE.md:83, but not README.md:18.
Fix (tested in scratch: 15 passed at HEAD, so no false positive in the five orientation files or the Focus; it kills mutants A and C and still flags every count main held):

```python
# A count of something that drifts, or a percentage. "Level 0 agents" names a tier.
DRIFTING_COUNT = re.compile(
    r"(?<![Ll]evel )(?<![Ll]evel-)\b\d[\d,]*(?:\.\d+)?"
    r"(?:%|\s+(?:\w+\s+)?(?:tests?|repos?|repositories|consumers?|agents?|passed|passing)\b)"
)
```

The groups are non-capturing, so `findall` reports `189 tests`. The current regex reports `tests`. For Detect, which runs on any grep:

```bash
grep -n -E '\b[0-9][0-9,]*(\.[0-9]+)?(%| ([a-z]+ )?(tests?|repos?|repositories|consumers?|agents?|passed|passing)\b)' README.md CONTEXT.md LANGUAGE.md CLAUDE.md .claude/README.md | grep -v -i -E 'level[ -][0-9]+ agent'
```

At HEAD it prints nothing (exit 1). Against main it prints 7 lines, including README.md:18 and :19. For "most recent", a pattern such as `(most recent|latest)[^.]*20[0-9]{2}-[0-9]{2}-[0-9]{2}` flags main's CONTEXT.md 3 times and LANGUAGE.md once. At HEAD its only hit is CONTEXT.md:29's own history sentence (S6). Cut that sentence and add the pattern, or file the class as a gap.

**W4. The Focus section's own rules are not pinned** (`tests/unit/test_state_block.py:29`, `:48-53`; the rule at `.claude/commands/session-end.md:45`).
Step 4.5 says the Focus "holds no count and no status". `ORIENTATION` leaves out the task list, and the Focus test asserts only that the section's body is not blank. A Focus step that reads "Suite: 508 tests pass; 16 repos reached." passes all 14 tests. So does a Focus that holds only its intro sentence. `/session-start` reads this section first (Step 3.5, summary item 5).
Fix (tested: HEAD's Focus has 5 numbered steps and 0 count hits, and both mutants are killed):

```python
    assert re.findall(r"^\d+\. ", focus.group(1), re.M), "the Focus has no numbered step"
    assert [m.group(0) for m in DRIFTING_COUNT.finditer(focus.group(1))] == []
```

**W5. "The newest file in `docs/sessions/`" has no collector, and Step 3 still says "most recently modified"** (`.claude/commands/session-start.md:40`, `.claude/commands/sitrep.md:14`; the pointer at `config/project.yaml:83`, `CONTEXT.md:34`, `.claude/commands/session-end.md:46`, Step 5 item 4).
The branch deleted `last_session.file`, the one exact pointer, and row 1 says "`last_session` needs no new home". Step 3 picks by modification time. In a fresh clone every session doc has the same mtime, and `ls -t` breaks the tie by name, so it returns the oldest. Five dates already have two docs (20260312, 20260317, 20260519, 20260828, 20261001), so "newest" is ambiguous by name as well. This is the skill's second-box case (`ADOPTION.md:33-35`), and a summary line tagged `[record: <file>, <date>]` would then carry the wrong file under a confident tag.
Evidence: in a scratch clone at 02b39d6, `stat` shows 1 distinct mtime across 26 session docs, and `ls -t docs/sessions/ | head -1` prints `20260312_infrastructure_audit.md`.
Fix: Step 3 and `/sitrep` source 4 say "the newest session doc by name, `ls docs/sessions/*.md | sort | tail -1` (names are date-first; modification times are not, and a fresh clone gives every file the same one); on a date with two docs, read both". The config comment and CONTEXT.md:34 say "by name".

**W6. Two surfaces still describe the old layout** (`.claude/README.md:114`; `docs/design/from_template_to_project.md:130`, `:437-441`).
- `.claude/README.md:114`: "`config/project.yaml` is the shared schema contract and project state". The file's own Work Organization section, changed by this branch, now says otherwise. Fix: "the shared schema contract and the project's identity".
- The template guide tells a new project to "Reset `docs/tasks.md` to empty Active/Blocked/Completed sections", and its sample list starts at `## Active`. A bootstrap that follows it and keeps `test_state_block.py` fails on day one. Evidence: HEAD's test against a scratch `tasks.md` of `# Task Tracker`, `## Active`, `## Blocked`, `## Completed` gives `1 failed, 13 passed` (`test_the_focus_lives_at_the_head_of_the_task_list`). Fix: change :130 to "Reset `docs/tasks.md` to an empty `## Focus` section and empty Active/Blocked/Completed sections" and put a `## Focus` stub above :440. Or add an "ADDED 2026-10-04" line to the existing P2 drift task (`docs/tasks.md:46`).

**W7. Claims with neither an `Evidence:` line nor `UNVERIFIED:`** (Claim Style rule 4).
I re-ran every claim below; none was refuted.

| Claim | Where | Re-run |
|---|---|---|
| "the suite runs 505 with this commit"; "Suite: 505 passed" | 0ebd059 | main `491 passed`; 0ebd059 `505 passed` |
| "14 tests, was 9 failed ... against main's files ... still 9 failed" | 0ebd059 | HEAD's test file in a main export: 9 of 14 failed |
| "the grep for the two keys prints 0, and pytest -k state_block selects 14 and passes" | 0ebd059, `docs/tasks.md:18` | `0`; `14 passed, 494 deselected` |
| "Detect (two greps, both 0 at the hub)"; "an eight-row Adoption-Mode Table" | 93de829 | no output, exit 1, at 93de829 and HEAD; 8 rows at 93de829, 9 at HEAD |
| "extract_entries reads the two same-day entries as two headings" | 93de829 | 17 entries; two distinct 2026-10-04 headings |
| "Both are unsent" | 93de829 | UNVERIFIABLE (below) |
| "red with the shipped range" | fe3dd77 | fe3dd77 `1 failed, 507 passed` |
| "3 passed"; "38 paths, 0 MISSING"; "the directory pass prints nothing"; "Suite: 508 passed" | 09d42e2 | all four reproduce at 09d42e2 and HEAD |
| "README.md said 189 tests while the suite ran 491" | entry `:11-12`, test docstring | main `README.md:19`, `:85`; main `491 passed` |
| "after cycles on 2026-07-20, 2026-08-03 and 2026-10-02" | `CONTEXT.md:29`, entry | the three session docs record 14, 15 and 16 repos |
| "(14 tests)"; "(3 tests run the shipped block)" | `CHANGELOG.md:11` | 14 and 3 collected |

Fix: carry these with their `Evidence:` lines into the session doc's `## Claims` table and the hand-back. The commits are unpushed, so the lead can also amend the messages.

## Suggestions

**S1. The Step 5 tags have no shape for a check that could not run, and item 6 conflicts with the rule above it** (`.claude/commands/session-start.md:103-125`).
`SKILL.md:131-134` says a summary line the renderer could not produce "renders `unchecked` with the blocker, never blank and never copied from the previous session". When `.venv/bin/pytest` cannot run on a fresh box, the Test Status line has no legal tag, and copying the last count is the easy way out. Add `- [unchecked: <blocker>]: a measured line whose command could not run; no value.` and accept `unchecked` in `TAG`. Item 6 asks for a "blocked count", a status written in the task list, two paragraphs after "Never restate a count or a status from a record or the task list as if it were current". Rewrite item 6 as: "**Tasks**: how many are active and blocked, counted this turn, and the top-priority items `[intent: docs/tasks.md]`". Add to the rule: "A count of the task list's items is taken this turn; a number or a status written inside an item is not current."

**S2. The process text the slice claims is unpinned** (`tests/unit/test_state_block.py`).
Each of these leaves all 14 tests passing: deleting the never-restate paragraph, the Step 3.7 heading, the Focus bullet in Step 3.5, `/sitrep`'s Focus source, or a tag-legend line; adding a Step 5 item without bold (`12. Coverage: 73% ...`); and moving `active_work:` to the config's top level. Add `"config/project.yaml"` to `SURFACES`. Its comment writes "last session" with a space, and the scratch run passed at HEAD. Then add one test:

```python
def test_session_start_reads_the_focus_and_the_register_and_forbids_restating():
    text = (REPO / ".claude" / "commands" / "session-start.md").read_text(encoding="utf-8")
    assert "## Step 3.7: Read the Gap Register" in text
    assert "`## Focus`" in text
    assert "Never restate a count or a status" in text
```

Use `^\d+\. ` as the item pattern at `:59`, so an item without bold is still checked.

**S3. `test_gaps.py:37` now reads an empty dict** (`tests/unit/test_gaps.py:37-38`).
With no `state:` key, `.get("state") or {}` is always `{}`. A top-level `known_issues:` passes both test files (mutant S). Check the parsed config's top level, or the raw text: `assert "known_issues" not in (REPO / "config" / "project.yaml").read_text(encoding="utf-8")`.

**S4. Read with `encoding="utf-8"`** (`tests/unit/test_state_block.py:38`, `:44`, `:49`, `:53`, `:57`, `:66`).
Under Python 3.11 or 3.12 on Windows the default is the locale code page. `.claude/README.md` does not decode as cp1252 (byte `0x90`), so two parametrizations raise `UnicodeDecodeError` there. Row 8 sends this file to consumers. `test_pcc_reference_integrity.py:15` already passes the encoding; `test_verifying_claims.py:212` has the same exposure.

**S5. The skill still describes slice 2 as marking lines** (`.claude/skills/maintaining-the-common-operating-picture/ADOPTION.md:113-115`).
ADOPTION says the second slice "marks every existing status line ... as a measurement ... or an estimate", "which is where the config's prose block starts to shrink". The hub's slice 2 marked none. It deleted the block, replaced each count with its command, and pinned the absence. Both entries are unsent and will travel together, so fold the lesson into the skill (0.1.2), as 0.1.1 did for slice 1: "marks or moves: a status line carries its fields, or it leaves for its home and the orientation file names the command that measures it."

**S6. Prose, `CONTEXT.md:29`.**
[Minor] Rule 3: "Until 2026-10-04 a snapshot here still named the 2026-04-21 propagation as the latest, after cycles on 2026-07-20, 2026-08-03 and 2026-10-02 (the `maintaining-the-common-operating-picture` skill)." The parenthetical does not say how the skill relates to the sentence. The sentence is also a record inside an orientation file, and `CHANGELOG.md:11` and the skill's 1.1.0 history already hold it.
Rewrite: "This section names where each part of the current state lives and holds no snapshot; the `maintaining-the-common-operating-picture` skill says why." Then W3's "most recent" pattern can run clean.

**S7. The skill's distinguishing table lags CONTEXT.md's** (`.claude/skills/maintaining-project-context/SKILL.md:56`, `:62-71`).
CONTEXT.md:107-108 adds `docs/tasks.md` and `docs/gaps.md` rows. The template that consumers copy (row 6) does not. Add both rows, and add "tasks vs gaps" to the `:56` placeholder.

**S8. `/sitrep` reads the Focus but does not use it, and still pulls record numbers undated** (`.claude/commands/sitrep.md:35`, `:69-70`).
"Metrics: Pull specific numbers from session docs" restates record numbers as current, which is what the new `/session-start` rule forbids. NEXT is "[Priority items from task list]". Rewrite: "Metrics: a number from a session doc carries the doc's date", and "NEXT: the Focus order, then priority items from the task list".

**S9. `/pci` calls the config "Project status & phases"** (`.claude/commands/pci.md:130`).
Change it to "Project identity & phases". `pci.md` is a gate surface, so it goes in its own `[gate]` commit (check 6).

**S10. The entry's Rollback leaves the Focus in place** (`docs/doctrine-updates.md:67-70`).
Restoring the `state:` block while the `## Focus` section stays gives active work two homes. Add: "move the Focus back into `active_work`, delete the section, and restore `.claude/README.md`'s Strategic line".

## Answers to the brief

### 1. Completeness: readers and writers of the state block

No code, script, CI workflow or agent definition reads `state`, `active_work` or `last_session`. I checked `.claude/agents/*` (`python-prototyper.md:16` says "Project identity and structure"), every skill (only the picture skill's `ADOPTION.md:69` and `EXAMPLES.md:9-10` name the block, as the thing to remove), `docs/design/roadmap.md:41` (phase status, which is identity), `docs/session-doc-format.md:34` (phase), `scripts/` (no reader; `adopt_doctrine.py` delivers `session-end.md` only, at `:61`), the README tree (fixed) and `.github/` (absent). Four places remain: `.claude/README.md:114` and the template guide (W6), `pci.md:130` (S9), and `test_gaps.py:37` (S3). Records were not counted.

### 2. Can each new test fail?

The `/pcc` tests are tight: each of three range mutants is killed by a different test, and the exact-output assertions leave no slack. `test_state_block.py` kills the restored block, the old README counts, an untagged bold item and a missing `---` (by `AttributeError`, an opaque failure for a consumer whose file lacks the rule). Its gaps are in W3, W4 and S2.

| Mutant (scratch copy of HEAD) | HEAD's tests | With the W3, W4 and S2 config fixes |
|---|---|---|
| README `189 tests` restored (control) | killed | killed |
| `state:` block restored (control) | killed | killed |
| README `53% coverage` | survives | killed |
| CONTEXT "reached 16 downstream repos" | survives | killed |
| CONTEXT "Most recent doctrine propagation: the 2026-10-02 cycle." | survives | survives (W3, S6) |
| top-level `active_work:` in config | survives | killed |
| Focus step "Suite: 508 tests pass; 16 repos reached." | survives | killed |
| Focus holds only its intro sentence | survives | killed |
| Step 5 item `12. **Coverage**: ...` with no tag | killed | killed |
| Step 5 item `12. Coverage: ...`, no bold, no tag | survives | survives (S2's item pattern) |
| never-restate paragraph, Step 3.7, Step 3.5 Focus bullet, `/sitrep` Focus, or a legend line deleted | survive | survive (S2's new test) |
| top-level `known_issues:` | survives (`test_gaps.py` too) | survives (S3) |
| config block renamed `status:` | survives | survives (accepted) |
| check 5 range back to `/^## Active/`; whole file; from `/^## Focus/` | killed, by three different tests | not re-run |

False positives of the shipped regex: `level 0 agents` (lower case), `Level-0 agents` and `Python 3.12 tests`. None occurs at the hub. The fix covers the first two.

### 3. The `/session-start` tag scheme

The scheme is faithful. The tags map onto rule 7's horizons and `ADOPTION.md`'s "Where things live" table one to one: `measured` is current operations, `register` is the running estimate and its gaps, `intent` is plans and the task list, `record` is history, and `identity` is the config. Every line carries a tag its source supports. Machine is a hostname looked up in the identity roster, tagged by the command that ran (`session-start.md:16-18`). Git State names the two commands Step 4 runs (`:70-71`). Version and Phase come from the config. Two gaps remain against the skill's own procedure for this summary (`SKILL.md:131-134`): no `unchecked` shape, and no age. A same-turn measurement makes the missing age harmless for now. S1 covers the first.

On "Tasks: active count ... `[intent: docs/tasks.md]`": tagging the line `intent` is honest about its subject. The count is a measurement taken this turn of a document that holds intent, and the tag tells a reader it says nothing about the system. The blocked count is the problem: it restates a status written in the task list, which the rule above it forbids. S1 rewrites the line.

### 4. The Focus section

Its form is right: intent, absolute dates, no counts, an order. Item 1 was the right content while the branch was open; at merge it becomes the defect (W1). A Focus step goes stale when its work completes, not when its date passes, and 93de829 shows the two can drift apart inside one branch. Items 2 to 5 read as intent and will stay true until their steps complete. Nothing in the section is checked for counts (W4).

### 5. The doctrine entry

- **Mechanism.** Row 6 is accurate. `adopt_doctrine.py:117-121` skips any existing target, and `:46` lists the skill directory. Row 2 is accurate for the same reason. Rows 3 and 4 say PATCH, and `adopt_doctrine.py` never delivers `session-start.md` or `sitrep.md` at all, so that is right too.
- **Detect.** It prints nothing at the hub (exit 1, grep's convention for no match) and flags every state-block line on main. It misses agents and percentages (W3).
- **Supersession.** The entry has the direction wrong when both entries arrive together, overstates the scope, and omits its dependency on slice 1 (W2).
- **Same-day entries.** Delivery marks keep the two headings apart. A repo that adopts the skill entry and skips slice 2 is consistent; the reverse breaks Step 3.7 (W2's fix names the dependency).

### 6. Claims and prose

- **Claims.** W7. No number was refuted.
- **UNVERIFIABLE: "Both are unsent"** (93de829). The probe reads consumer marks in other repositories, which is outside this review's scope. The hub's record shows no cycle after 2026-10-02. The Focus (`docs/tasks.md:9`) and the P1 (`:15`) hold propagation until the `assay` exclusion lands.
- **Em dashes.** The branch adds four, at `sitrep.md:11`, `:12`, `maintaining-project-context/SKILL.md:101` and `CONTEXT.md:91`. All four are label separators in lists whose siblings use them, which `REVIEWING.md` pass 4 exempts. The commit messages and the doctrine entry contain none.
- **Cruft.** No word from `LANGUAGE.md`'s list appears in any added line.
- **Private terms.** `/pcc` check 7 over the index and the 5 unpushed commits printed nothing.

## Counts

Verdict: GO-WITH-FIXES. Critical 0, Warning 7, Suggestion 10.

## Disposition (lead, 2026-10-04)

Applied before merge; each Warning reproduced or re-run first.

| Finding | Disposition |
|---|---|
| W1 | Applied: Focus step 1 is the `assay` exclusion; slice 2 is no longer named as next. |
| W2 | Reproduced: `entries_to_deliver` returns `reversed(wanted)`, oldest first. The entry names the skill entry by title, says a notification lists it first, and limits its supersession to rows 2 to 4; rendering at `/session-start` stays with slice 3, `/task brief` stays deferred. Row 3 says Step 3.7 needs slice 1's register. |
| W3 | Applied the reviewer's pattern in the test and in Detect, plus the "latest ... date" pattern for orientation files. Test-first: 7 stale shapes and 3 non-counts as parameters, 6 red against the old pattern. Detect at the hub: 0, 0, 0; against main's files: 9 count lines. |
| W4 | Applied: the Focus needs a numbered step and no drifting count. Both mutants caught (a step quoting "508 tests" and "16 repos"; a Focus holding only its intro). |
| W5 | Reproduced: 5 dates hold two session docs. Step 3, `/sitrep` source 4, the config comment, `CONTEXT.md` and `/session-end` say "by name"; Step 3 gives `ls docs/sessions/*.md | sort | tail -1` and says to read both docs on a two-doc date. |
| W6 | Applied: `.claude/README.md:114` says identity; the template guide resets `docs/tasks.md` with a `## Focus` section and its sample list starts with one (the Focus test passes on that sample). |
| W7 | Applied in the hand-back to the user. "Both are unsent" stands on the delivery marks on this machine only (0 of 19 held either heading); other machines are gap G3. |
| S1 | Applied: `[unchecked: <reason>]` in the legend, pinned; the Tasks line reports counts "as the list stands", a reading of the list, not a status claimed as current. |
| S2 | Applied: Step 3.5's Focus read, Step 3.7's register read and the never-restate rule are pinned; `config/project.yaml` joins `SURFACES`. |
| S3 | Applied: `test_gaps.py` checks the config's text for `known_issues`; the unused `yaml` import is gone. |
| S4 | Applied: every read in `test_state_block.py` passes `encoding="utf-8"`. |
| S5 | Applied: `ADOPTION.md`'s second slice says most lines leave; the skill moves to 0.1.2 and the skill entry's heading follows (no mark on this machine holds the old heading). |
| S6 | Applied: the history sentence left `CONTEXT.md`; the "latest ... date" pattern now guards that file. |
| S7 | Applied: the `maintaining-project-context` table gains the task-list and gap-register rows. |
| S8 | Applied: `/sitrep` Metrics carry their dates and are measured again when acted on; NEXT reads the Focus first. |
| S9 | Applied in its own `[gate]` commit: `pci.md`'s Key Files row says identity. |
| S10 | Applied: the entry's Rollback moves the Focus steps back into `active_work`. |

No second round: 0 Critical, and each Warning's fix was checked by the command named in its row. Suite after the fixes: 520 passed.
