# Review: WHETSTONE Capture Point (`[gate]` commit d565df9)

**Author**: code-reviewer
**Date**: 2026-10-01
**Type**: Code review (doc-only `[gate]` commit, non-author review under CONOP WHETSTONE D4)

**Verdict: GO-WITH-FIXES.** 0 Critical, 4 Warning, 6 Suggestion.

The commit does what the task line asks. The `KB-graph:` format is byte-identical to the skill's, Step 5.5 matches the canaries, and no count already taken changes. Two warnings concern the committed text and both bear on metric M3. Two concern the record around the commit and one Status Log entry fixes both.

## Scope and method

- Commit `d565df9` on `topic/whetstone-capture-point`, parent `b1c3e36` (`main`). Two files, 24 insertions, 0 deletions (`git show --stat d565df9`).
- I read both files with `git show d565df9:<path>`, not from the working tree. `HEAD` moved from `d565df9` to `4b11ec3` while I worked.
- Files cited by line (the CONOP, the traversal skill, `docs/tasks.md`, `scripts/adopt_doctrine.py`, the session docs) are identical in the working tree and at `d565df9`: `git diff --stat d565df9 -- <those paths>` printed nothing.
- Line numbers for the two changed files are lines at `d565df9`.

## Checks run

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Does the task, no more, no less | Pass, with three additions that are sound | See "Task fit" below |
| 2 | Step 5.5 against both canaries | Two intended differences, one unlisted (backticks) | `diff` output below; S1 |
| 3a | `KB-graph:` format identical to the skill | Pass, byte-identical | `grep -F` of skill line 56 matches `session-end.md:64` and `session-doc-format.md:87` |
| 3b | M1 claim matches the skill | Pass, trigger wording wider than the skill's | Skill lines 53, 59, 65; S2 |
| 3c | Timing rule matches M3 | Content matches; delivery and template placement do not | W1, W2 |
| 4 | D9 fields absent from the channel line | Not a defect of this commit | "Channel schema" below |
| 5 | Conflict with Wave 2 | Does not block; overlaps in one sentence | "Wave 2" below; S3 |
| 6 | Changes a count already taken | No | "Measurement window" below; W3 |
| 7 | Prose, em dashes | 0 em dashes and 0 en dashes in 24 added lines; 0 banned cruft words | `grep -c '—'` on the added lines returned 0 |
| 8 | Named paths resolve | Pass | "Paths" below |
| - | Commit message claim "403 tests pass" | Confirmed | `403 passed, 1 warning in 4.40s`, run on a `git archive d565df9` export in the scratchpad, `myproject` imported from the export |

## Critical

None.

## Warning

### W1. The body template puts the `KB-graph:` line where record order stops meaning anything

`docs/session-doc-format.md` lines 83 to 91 at `d565df9`:

```
## Work Completed

[Organized by sub-topic or wave. Each sub-topic gets a heading.]

`KB-graph: <traversal run> → <what it changed or confirmed>`

(One line per knowledge-base walk, written when the walk happens. Omit when the session ran none.)

### 1. <Sub-topic>
```

The template fixes every line above every sub-topic. The only M3 verification method on record reads order inside the document. `docs/sessions/20260828_cross_repo_feedback_loop_check.md` line 59: "each traversal precedes the edit in the record's own order and the edit carries the traversal's content", and line 111: "Verify stx-server's M3 lines by the record's order, not commit timestamps". A line that sits above all work precedes every edit by construction, so the order test passes for any line, decorative or not.

Existing practice is split, which shows the choice is live:

| Session doc | Where its `KB-graph:` lines sit |
|---|---|
| `20260827_figure_style_doctrine_from_stx_server.md` | Inside sub-topics 2 and 4 (lines 40, 42, 46, 54) |
| `20260828_cross_repo_feedback_loop_check.md` | Inside sub-topics 1 to 4 (lines 40, 55, 69, 71, 77) |
| `20260828_fleet_poll_and_loop_closure_audit.md` | Inside sub-topics 1 and 2 (lines 44, 67) |
| `20260829_machine_identity_and_lake_conventions.md` | Above all sub-topics (lines 38, 40) |
| `20260930_overwatch_claim_checks_and_data_loss_guards.md` | Above all sub-topics (lines 35, 37) |

The template makes the weaker placement the default. This is a change to how M3 is captured, which is the scope of this gate.

Fix: move the line into the sub-topic block.

```markdown
## Work Completed

[Organized by sub-topic or wave. Each sub-topic gets a heading.]

### 1. <Sub-topic>

`KB-graph: <traversal run> → <what it changed or confirmed>`

[What was done, why, what files changed.]

(One `KB-graph:` line per knowledge-base walk, in the sub-topic it informed, above the edit it led to. Omit when the session ran none.)
```

### W2. The Step 5 reminder sets a deadline that has passed when the reader meets it

`.claude/commands/session-end.md` line 64 at `d565df9` ends: "Write it when the walk happens, before the edit it informs, not at session close." The sentence lives in the session-close command. Line 55 of the same step says "Create a session doc in `docs/sessions/`", so the document the line belongs in does not exist until close.

The content matches M3. Skill line 67: "a decorative line written after the edit fails verification". CONOP line 160: "A line whose traversal did not precede and inform the edit fails". The defect is the missing instruction for the one case the reminder exists for: an author at close who walked the knowledge base and has no line. The text tells that author to record the walk and not to record it now. The author will add the line anyway, and nothing marks it as added late. CONOP line 137 names the cost: "a decorative line is otherwise traceless".

Fix, option A (recommended): say what to do at close and leave a trace.

```markdown
- If a traversal informed the session's work, record it in Work Completed as a `KB-graph: <traversal run> → <what it changed or confirmed>` line, in the sub-topic it informed. That line is uptake metric M1 in `.claude/skills/traversing-the-knowledge-base/SKILL.md`; a walk with no line cannot be counted. The skill asks for the line when the walk happens, before the edit it informs. A line added now ends with `(added at close)`: M1 counts it and the M3 verifier sets it aside.
```

The `(added at close)` marker is a new capture rule. It needs the lead's and the user's acceptance, and it belongs in the skill's M3 text too.

Option B (smaller): delete "not at session close" from line 64 and leave timing to the skill, which loads when the walk happens (skill line 53). This removes the contradiction and leaves late lines untraceable, as they are today.

### W3. Nothing dates the change in capture regime, and the window count is still open

The commit touches no session doc and no Status Log entry, so no count already taken changes (see "Measurement window"). The risk is forward.

- From `d565df9` on, `/session-end` prompts for the line. A1 tests uptake "without enforcement" (CONOP line 50). The skill's outcome matrix calls a pointer of this kind "one escalation rung (orientation pointer in `/session-start`)" (skill line 74). A session-end pointer is the same kind of rung, taken before the window's verdict.
- `docs/tasks.md` line 7 leaves the window "between 4 and 6 of 5" and the count unresolved. If the qualifying rule leaves the window open, or the M1 >= 3/5, M3 = 0 cell extends it by three sessions (skill line 73), prompted sessions and unprompted sessions land in one M1 figure.
- The CONOP is "append-only from this point, changes land in the Status Log" (line 3). The Status Log ends at the 2026-08-28 entry (line 235). No entry records this change.

Fix: a follow-up commit, separate from the `[gate]` commit per D4, appends a Status Log entry that states: the capture point shipped at `d565df9` on 2026-10-01; every session doc dated before that is unprompted; the Wave 1 amendment reports M1 for the two regimes separately. The same commit closes `docs/tasks.md` line 9. Make it a condition of the merge.

### W4. Step 5.5 in the template is Wave 4 surface, shipped ahead of its gate and unrecorded

CONOP line 171 places "the downstream session-end addition that writes fleet-scope lessons to the upstream-lesson file" in Wave 4, gated on Wave 2. Line 185 says "No new downstream obligations before the canaries validate A3 and A6".

The hub's `session-end.md` is the template's `session-end.md`. Two paths carry it downstream:

- Every new bootstrap copies it.
- `scripts/adopt_doctrine.py` lines 51 and 52 list `docs/session-doc-format.md` and `.claude/commands/session-end.md` as verbatim copies. The helper skips a file that exists (lines 93 to 110), so it reaches only repos that lack the file.

Existing downstream repos that hold the file are untouched. New consumers get the D10 channel by default.

A6's state: `docs/tasks.md` line 6 records a favorable read on one canary (veil-engine, 6 of 6, 2026-08-28) and no data on the other. The Status Log holds no A6 verdict. Today veil-engine's channel file holds 10 lesson lines. tactics-game has no channel file and 14 commits since its seed (`git log --oneline c498a94..HEAD | wc -l`); I did not read its session docs, so that is a count, not an A6 reading.

The 2026-08-21 entry (CONOP line 213) is the precedent: Wave 4 surface reached early was "logged as an out-of-sequence action rather than as Wave 4 progress", "by user direction". I cannot establish from the repo that the user directed this one; the P1 task line (`docs/tasks.md` line 9) is the only authority I found.

Fix: the Status Log entry from W3 also records Step 5.5 in the template as an out-of-sequence Wave 4 action, names who directed it, and states the A6 read it rests on. Update `docs/tasks.md` line 32, which still says the capture point "must ship with the template at Wave 4 rollout".

## Suggestion

### S1. One unlisted difference from the canaries

`diff` of the hub's Step 5.5 against each canary gives three hunks. Two are the intended ones (`<this-repo>` in the schema line; the added fourth rule). The third:

```
< ... The upstream template repo (tacsop) harvests it on machine visits and clears it after intake.
> ... The upstream template repo (`tacsop`) harvests it on machine visits and clears it after intake.
```

Backticks around `tacsop` on hub line 80. Cosmetic. The two canaries differ from each other only in the repo name, and each matches its seed commit (`c498a94`, `b23413d`). Either drop the backticks or say "verbatim except" in the Status Log entry.

### S2. The reminder's trigger is wider than the skill's, and its recipe list is not the skill's

```
[Minor] Rule 2: "If the session walked the knowledge base (lineage, backlinks, blast radius), record each walk"
        (.claude/commands/session-end.md line 64)
Rewrite: "If a traversal informed the session's work (lineage, blast radius, neighbors, why), record it"
```

Skill line 53 sets the trigger: "When a traversal informs your work". The reminder says any walk. The skill's recipes are lineage, blast radius, neighbors, why, integrity (lines 23 to 40); "backlinks" is a mechanism, not a recipe. The new text also says "walk" three times where the format string and the skill say "traversal". The skill owns the metric, so its words should win.

### S3. Rule 4 is a routing rule in Wave 2's file, and it names the parking lot D2 replaces

Hub line 83: "route the lesson to its owner artifact, or to `docs/tasks.md` when no artifact owns it yet." D2 (CONOP line 106) is the routing step, gated on A1 and A2, and it exists to kill "the no-aging parking lot" (line 32 names `docs/tasks.md` as that lot). Rule 4 describes present practice and the hub needs some instruction in place of the file, so keep it. Record in the Status Log entry that Wave 2 replaces rule 4 and states how Step 5.5's line relates to the D9 line.

### S4. The format string now lives in three files

Skill line 56, `session-end.md` line 64, `session-doc-format.md` line 87. `session-end.md` line 12 records what copies cost: "an earlier copy of the list drifted from `pcc.md` and was caught 2026-08-14". The repo already pins prose with tests (`tests/unit/test_session_start_checks.py`, `tests/unit/test_verifying_claims.py`). A three-line test that asserts the skill's line appears in the other two files would hold the copies together. It is a separate commit under D4.

### S5. M1's grep cannot tell a line from a mention, and the template now hands every author the literal string

M1 is `grep -l "KB-graph:"` over session docs (skill line 65). In `20260828_fleet_poll_and_loop_closure_audit.md` the string matches on lines 71, 139, 178 and 197, none of which is an evidence line. A session doc that keeps the template's placeholder, or that merely describes this commit, scores on M1. The format doc sits outside `docs/sessions/`, so the template itself adds no hit. Raise an anchored pattern at the window-close amendment. Do not change it here.

### S6. Capture ships ahead of harvest, and Step 5.5 presumes a section the template lacks

Hub line 80 says the hub "harvests it on machine visits and clears it after intake". Two harvest tasks are open (`docs/tasks.md` lines 14 and 33), and veil-engine's file holds 10 lines dated 2026-08-15 to 2026-09-10. Harvest is Wave 4's step; note the backlog in the Status Log entry so E6's latency is read against it.

Step 5.5 says "check each lesson's scope". The format doc's body template has no Lessons section (`grep -i lesson` finds only the new line 198); 3 of 23 hub session docs carry one. Wave 2 adds D9 to the format doc and owns this.

## Answers to the brief

### Task fit (check 1)

`docs/tasks.md` line 9 names four gaps: neither file asks for a `KB-graph:` line, neither carries Step 5.5. "Two edits to files that already exist."

| Task element | In the commit |
|---|---|
| `session-end.md` asks for the line | Line 64 |
| `session-end.md` carries Step 5.5 | Lines 68 to 83 |
| Format doc asks for the line | Lines 87 to 89 and 197 |
| Format doc carries Step 5.5 | Line 198, as a pointer to `/session-end` Step 5.5 |

Three things go beyond the task's words. All three are sound.

- Rule 4, the hub exception. Without it the hub's own sessions would write a channel file nobody harvests.
- The timing sentence for M3. Right in intent; see W2.
- A pointer in the format doc where the task says "carries". One copy of the step is better than two (see S4).

Nothing is missing. The task line stays open in this commit, which is correct under D4: closure rides the follow-up commit.

### Channel schema (check 4)

Not a defect of this commit. The line is the D10 channel's shape as seeded.

- Status Log, 2026-08-15 (CONOP line 211): the convention is live in both canaries with "fleet-scope test, one-line schema with origin provenance, mirror-of-upstream-update rules (append mode, never gitignore, hub clears at harvest)".
- D10 (line 114): a harvested lesson "enters the hub loop at `OBSERVED` with provenance naming the origin repo and session doc". Status is fixed and `origin:` is required.
- D9 (line 113) defines the line "in session docs". `owner:` and `verdict:` come from D2's routing step, which ships in Wave 2 (lines 106, 165). A downstream session cannot name a hub owner artifact.
- The hub's schema line equals each canary's at its seed commit except for the repo name (S1).

### Wave 2 (check 5)

The commit does not block Wave 2 and pre-empts none of its content. Wave 2 (CONOP line 165) adds the D2 routing step, the D9 schema, D1 statuses and D3 headers. This commit adds none of them. Both changes are additive to the same two files, so the cost is a textual merge around Step 5 and a step number for D2. The one overlap is rule 4 (S3). The commit does pre-empt part of Wave 4 (W4).

### Measurement window (check 6)

No count already taken changes.

- The diff touches two files. Neither is a session doc, the CONOP, or the skill.
- `grep -l "KB-graph:" docs/sessions/*.md` returns five docs (2026-08-27, two on 08-28, 08-29, 09-30). All predate the commit.
- Eight dated candidates predate 2026-10-01: 08-15, 08-21, 08-22, 08-27, two on 08-28, 08-29, 09-30. The window is five sessions. It is still open on 2026-10-01 only if the qualifying rule, when written, excludes four or more of the eight.

The forward risk is W3.

### Prose (check 7)

Four passes per `REVIEWING.md` on the 24 added lines. Step 5.5 is a verbatim copy and I held it to the punctuation pass only, since rewording it would break identity with the canaries.

1. Point: pass. Each new bullet leads with its action.
2. Structure: pass.
3. Words: 0 hits against the ten banned words and two banned phrases in `LANGUAGE.md` lines 147 to 149. One Minor (S2).
4. Punctuation: 0 em dashes, 0 en dashes. The arrow in the format string is specimen text.

### Paths (check 8)

Every backticked path in the added lines, tested against the `d565df9` tree:

```
EXISTS  .claude/skills/traversing-the-knowledge-base/SKILL.md
MISSING .claude/upstream-lesson.md      (runtime artifact)
MISSING .claude/upstream-update.md      (runtime artifact)
EXISTS  docs/tasks.md
```

`/session-end` Step 5.5 exists at line 68. `<this-repo>/docs/sessions/<this-session-doc>.md` is a write-time placeholder. The Day-1 rename (`docs/design/from_template_to_project.md` Step 1) substitutes `myproject` only, so the two `tacsop` mentions survive a bootstrap unchanged. `.gitignore` does not ignore either channel file.

## Fix order

1. W1 and W2 change the capture text. Amend `d565df9` or add a second `[gate]` commit on the branch, before merge.
2. W3 and W4 are one Status Log entry plus the `docs/tasks.md` updates (lines 9 and 32), in a commit that is not the `[gate]` commit.
3. Suggestions at the lead's discretion. S4 and S5 are their own gate changes.

**Verdict: GO-WITH-FIXES**

---

## Round 2

**Date**: 2026-10-01
**Reviewed**: `topic/whetstone-capture-point` at `3820b95` (`8c31948`, `1ed229c`, `3820b95` on top of `d565df9`)

**Verdict: GO-WITH-FIXES.** W1 to W4 are all CLOSED. 0 Critical, 1 new Warning, 6 new Suggestion. The Warning is one sentence in the Status Log entry and one in `docs/tasks.md`, both on an unmerged branch.

### Method

I read the branch only through `git show 3820b95:<path>`, `git diff`, and `git archive` into the scratchpad. `main` and `origin/main` are at `b1c3e36`. The branch has no remote ref and is merged only into `topic/overwatch-verifying-claims` (`2783d6e`). Full suite on the `3820b95` export: `406 passed, 1 warning in 4.29s`.

### Status of the round 1 warnings

| # | Status | Probe against `3820b95` | Output |
|---|---|---|---|
| W1 | CLOSED | Template block, `docs/session-doc-format.md` lines 87 to 93 | `### 1. <Sub-topic>` at 87, the `KB-graph:` line at 89, `[What was done, why, what files changed.]` at 91, the placement note at 93 |
| W2 | CLOSED (option B) | `grep -c 'not at session close'` on `session-end.md`; `grep -c 'when the walk happens'` on both files | 0; 0 and 0. Line 64 now ends "The skill says when to write it." |
| W3 | CLOSED, see N1 | Last Status Log heading; the task lines | CONOP line 237: "2026-10-01 — The `KB-graph:` capture point shipped; the capture regime changes here." The P1 capture task is gone from Active; the Completed line is `docs/tasks.md` line 58; the window-count P1 stays open at line 7 |
| W4 | CLOSED | `grep -c 'Step 5\.5\|upstream-lesson\|LESSON (OBSERVED)'` on `session-end.md`, the format doc, the test file | 0, 0, 0. Step headings run 1, 2, 3, 4, 4.5, 5, 6. `docs/tasks.md` line 30 carries the HELD note |

Other round 1 probes, re-run:

- Format string: byte-identical to skill line 56 in both files (1 match each with `grep -F`).
- No count already taken changes: `git diff --stat b1c3e36 3820b95 -- docs/sessions/ .claude/skills/traversing-the-knowledge-base/` is empty.
- Dashes: one em dash in the added text outside this report, the date separator in the Status Log heading, which matches every other entry and is exempt as a list separator.

W2's known residue stands: a line added at close leaves no trace. The Status Log entry says so and sends it to the window-close amendment.

A limit on W1 that I should have stated in round 1. The template now tells the author to put the line above the edit, so a line placed by the template precedes its edit whether or not the traversal did. Placement gives the verifier the edit to read for the traversal's content. It does not show when the line was written. See N4.

### New Warning

**N1. The regime boundary is stated two ways, and neither is the real boundary.**

- CONOP line 237: "Every session doc dated before 2026-10-01 is unprompted; every later one is prompted." A doc dated 2026-10-01 falls in neither class.
- `docs/tasks.md` line 58: "Sessions from 2026-10-01 on are prompted." That includes the day the Status Log leaves out.
- The prompt exists where the commit exists. `main` and `origin/main` are at `b1c3e36`. The 2026-08-28 Status Log entry records two machines working this same window. A session after 2026-10-01 on a checkout without `1ed229c` is "later" and unprompted.
- The session that ships the prompt is in the position the CONOP ruled on for session 0 (line 206): counting it "would be the self-serving inclusion".

The date wording traces to my round 1 W3 fix text. The error is mine first.

Fix, in the Status Log entry and the Completed line, before merge:

```
A session is prompted when its checkout contains `1ed229c`
(`git merge-base --is-ancestor 1ed229c <the session doc's commit>`); the date is a guide, not the test.
The 2026-10-01 session shipped the prompt and is reported apart from both regimes.
```

The second sentence is a ruling for the lead and the user. Any explicit class for that session closes the gap.

### New Suggestions

**N2. Two claims were written before their evidence.** The Completed line says "shipped" and "all applied"; the Status Log says "all four applied". Both were committed before this round ran and before any merge. Round 2 now supports "all four applied". "Shipped" becomes true at merge. The neighbouring Completed lines cite merge commits (`d602c8e`, `d03e66a`, `d98428a`, each with two parents). After the merge, cite its SHA on line 58. Merge this branch before `topic/overwatch-verifying-claims`, which already contains it, so the `[gate]` commits reach `main` through their own gate merge.

**N3. Two counts are off.**

- `1ed229c` says "three lines in the format doc". `git diff --numstat b1c3e36 3820b95` gives `5 0 docs/session-doc-format.md`: five added lines, three of them non-blank. The session-end count is right: `1 0`.
- `docs/tasks.md` line 58 says "three pin tests, `8c31948`". The tip has three tests. Two come from `8c31948`; the third comes from `1ed229c`, which also deleted `8c31948`'s third. Rewrite: "three pin tests, `8c31948` and `1ed229c`".

**N4. The Status Log's reason for the placement claims more than placement gives.**

```
[Minor] Rule 2: "because the only M3 verification on record reads the record's order; the first version
        put it above every sub-topic, where any line passes that check"
        (docs/plans/conop_whetstone_recursive_doctrine_loop.md line 237)
Rewrite: "so the verifier knows which edit to read for the traversal's content. Placement cannot show
        when a line was written; that question goes to the window-close amendment."
```

A line placed above its edit by instruction also passes the order check. The sentence inherits my round 1 framing.

**N5. The pins hold presence, not the ask.** Ten mutants, seven killed, three survive (table below). The survivors keep the string and change what it says or where it sits. `tests/unit/test_session_start_checks.py` line 28 slices one step with `^## Step 4.*?(?=^## Step 5)`; the same slice for Step 5 would kill the move.

**N6. S2 landed in one of three places.** `session-end.md` line 64 now reads as the skill does. `docs/session-doc-format.md` lines 93 and 197 still say "per knowledge-base walk" and "each knowledge-base walk", the wider trigger.

**N7. Two smaller items.**

- The user's decision to hold Step 5.5 is recorded in the lead's words. The 2026-08-14 entry quotes the user (CONOP line 205). I cannot verify the decision from the repo. Quote it or cite where it was given.
- `scripts/adopt_doctrine.py` copies `session-end.md` to a repo that lacks it and does not list the traversal skill (`grep -c traversing-the-knowledge-base` returns 0). Such a repo receives line 64's pointer to a skill file it does not have. Present since `d565df9`; I missed it in round 1. Low odds; note it for Wave 4.

The Step 5.5 half of the task moved from a P1 line to a P3 line (`docs/tasks.md` line 30). That follows from the hold, and the line says so.

### Net diff count

`git diff b1c3e36 3820b95 -- .claude/commands/session-end.md docs/session-doc-format.md`:

| File | Added | Non-blank | Deleted |
|---|---|---|---|
| `.claude/commands/session-end.md` | 1 | 1 | 0 |
| `docs/session-doc-format.md` | 5 | 3 | 0 |

The content is what `1ed229c` says: one reminder bullet, the template line, the placement note, one best-practice bullet. The line count is N3.

### Pin tests

`8c31948`'s claim holds. Its three tests pass on its own tree and all three fail against `b1c3e36`'s two docs.

Mutants against the three tests at `3820b95`, each applied to a fresh scratch copy:

| Mutant | Result |
|---|---|
| Both docs as on `main` | 3 failed |
| Format doc as at `d565df9` (line above every sub-topic) | 1 failed: the placement test |
| Reminder line deleted from `session-end.md` | 1 failed: the session-end test |
| Arrow changed in the template line | 2 failed |
| Template line moved below the work paragraph | 1 failed: the placement test |
| Second copy of the line added above the sub-topics | 1 failed: the placement test |
| Skill changes its format line | 3 failed |
| Reminder reworded to "Do not record a ...", string kept | 3 passed (survivor) |
| Best-practice bullet deleted from the format doc | 3 passed (survivor) |
| Reminder moved from Step 5 to Step 1 | 3 passed (survivor) |

The tests fail when the ask is dropped, when a copy drifts from the skill, and when the W1 placement regresses. They are what the file's docstring says: pins.

### Fix order

1. N1: one sentence in the Status Log entry and one in the Completed line, before merge.
2. N3 and N4 can ride the same touch. N2's SHA citation follows the merge.
3. N5, N6, N7 at the lead's discretion.

**Round 2 verdict: GO-WITH-FIXES**

---

## Round 3

**Date**: 2026-10-01
**Reviewed**: `topic/whetstone-capture-point` at `23fbf17` (`7e2778b`, `23fbf17` on top of `3820b95`)

**Verdict: GO.** N1 to N7 are closed. 0 Critical, 0 Warning, 3 Suggestion. None of the three needs another round.

### Method

Same as round 2: `git show 23fbf17:<path>`, `git diff 3820b95 23fbf17`, and a `git archive 23fbf17` export in the scratchpad. Full suite on the export: `406 passed, 1 warning in 4.09s`. Net change against `main` is unchanged in size: `git diff --numstat b1c3e36 23fbf17` gives `1 0` for `session-end.md` and `5 0` for the format doc.

### Status of the round 2 findings

| # | Status | Output at `23fbf17` |
|---|---|---|
| N1 | CLOSED | CONOP line 237: "**The boundary is a commit, not a date.** A session is prompted when the checkout it ran on holds `1ed229c`". The command as written exits 0 on the tip and 1 on `b1c3e36`. `grep -c "dated before 2026-10-01"` and `grep -c "from 2026-10-01 on"` both return 0. The 2026-10-01 session "belongs to neither class and is reported apart, as session 0 was". |
| N2 | CLOSED | Entry heading: "The `KB-graph:` capture point, and the regime change it starts." `grep -c shipped` on the Completed line returns 0. The merge SHA can only follow the merge. |
| N3 | CLOSED | Entry: "`1ed229c` says three lines changed in the format doc, and `git diff --numstat b1c3e36 3820b95` shows five added, three of them non-blank". Completed line: "three pin tests across `8c31948`, `1ed229c`, and `7e2778b`". |
| N4 | CLOSED | Entry: "Placement tells the M3 verifier which edit to read the line against; it cannot show when the line was written." |
| N5 | CLOSED | The pin reads Step 5 only (`_step5()`) and matches the ask clause. Mutant runs below. |
| N6 | CLOSED | Format doc line 93: "per traversal that informed the work"; line 197: "Record each traversal that informed the work". `grep -c walk` on the format doc returns 0. |
| N7 | CLOSED | Entry: "the user chose the option \"Hold Step 5.5\"". `docs/tasks.md` line 31 files the adoption-helper gap as a P3. |

### Mutants against the pins at `23fbf17`

| Mutant | Round 2 | Round 3 |
|---|---|---|
| Reminder reworded to "Do not record a ...", string kept | survived | killed: `1 failed, 2 passed` |
| Reminder moved from Step 5 to Step 1 | survived | killed: `1 failed, 2 passed` |
| Best-practice bullet deleted from the format doc | survived | survived: `3 passed`, as `7e2778b` says |
| Placement clause ", in the sub-topic it informed" deleted from the reminder | not run | survived: `3 passed` |
| Everything after the ask clause deleted from the reminder | not run | survived: `3 passed` |

The five mutants killed in round 2 that I re-ran are still killed: `main`'s two docs (3 failed), the `d565df9` format doc (1 failed), the reminder deleted (1 failed), the arrow changed in the template (2 failed), the skill's format changed (3 failed).

### Claims the re-run refutes

One. `7e2778b` says "the pin now matches the whole instruction, from \"If a traversal informed\" on". The pin's string ends at "` line". The last two mutants above delete the rest of the instruction and all three tests pass. The pin holds the ask clause and its step. The entry's own wording is right: "the pins hold the reminder's presence and place, not its good sense".

Both of `7e2778b`'s other claims hold: the two named mutants fail the new pin, and the third survives. Nothing in `23fbf17`'s message or the rewritten entry fails a re-run.

### Rewriting the entry in place

Yes. Line 3's rule protects the approved record that readers of `main` rely on, and the first wording never reached `main` or `origin`: no remote branch contains `3820b95`. The rewrite is its own commit on top of `3820b95`, not an amend, so both wordings stay in history and the commit message says what was done.

### Suggestions

**R1. The pin claim in `7e2778b`.** Either extend the `ask` string in `tests/unit/test_session_end_capture.py` by ", in the sub-topic it informed." or add a third commit-message correction to the entry beside the two it already records. The format doc's placement is pinned; the reminder's is not.

**R2. `topic/overwatch-verifying-claims` still carries the first wording.** It merged `3820b95` at `2783d6e` and does not hold `23fbf17`; its copy of the CONOP is identical to `3820b95`'s. Merge this branch into `main` first, or merge `23fbf17` into that branch, so the rewritten entry is the one that lands.

**R3. Three small record items.**

- The Completed line says "Two review rounds". This section makes three.
- The entry says "`8c31948` holds two of the three pin tests at the tip". `7e2778b` rewrote the body of one of them; the Completed line's three-commit attribution is the accurate one.
- The entry quotes the chosen option as "Hold Step 5.5". The lead reports the option text as "Hold Step 5.5 (Recommended)". I cannot verify either from the repo. If the option is quoted, quote it whole: the label records that the chosen option was the recommended one.

One "walk" remains in `session-end.md` line 64 ("a walk with no line cannot be counted"). The meaning is clear; no finding.

**Round 3 verdict: GO**
