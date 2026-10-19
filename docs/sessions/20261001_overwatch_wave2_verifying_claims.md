# Session: OVERWATCH Wave 2, the Verifying-Claims Skill

**Date**: 2026-10-01
**Branch**: main; topic branches `topic/whetstone-capture-point` and `topic/overwatch-verifying-claims` (both merged and deleted)
**Tags**: #session #doctrine #overwatch #whetstone #testing #review #infra
**Documents**: [SKILL.md](../../.claude/skills/verifying-claims/SKILL.md), [EXAMPLES.md](../../.claude/skills/verifying-claims/EXAMPLES.md), [session-end.md](../../.claude/commands/session-end.md), [session-doc-format.md](../session-doc-format.md), [code-reviewer.md](../../.claude/agents/code-reviewer.md), [docs/tasks.md](../tasks.md)
**Implements**: [conop_overwatch_claim_verification_and_irreversible_guards.md](../plans/conop_overwatch_claim_verification_and_irreversible_guards.md) (Wave 2 tasks 2a to 2c); [conop_whetstone_recursive_doctrine_loop.md](../plans/conop_whetstone_recursive_doctrine_loop.md) (the `KB-graph:` capture point)
**References**: [20261001_overwatch_kernel_wording.md](../reviews/20261001_overwatch_kernel_wording.md), [20261001_overwatch_wave2_gate.md](../reviews/20261001_overwatch_wave2_gate.md), [20261001_whetstone_capture_point_review.md](../reviews/20261001_whetstone_capture_point_review.md), [ISOLATION.md](../../.claude/skills/shift-left-testing/ISOLATION.md)
**Follows**: [20260930_overwatch_claim_checks_and_data_loss_guards.md](20260930_overwatch_claim_checks_and_data_loss_guards.md)

---

## Summary

The user reviewed OVERWATCH's Wave 1 and found the part that answers the plan's main problem missing: no skill existed for overclaims. The release was held, and this session built Wave 2's tasks 2a to 2c on Nidhogg: the `verifying-claims` skill, its kernel in `CLAUDE.md`, a required Claims table at `/session-end`, and a reviewer checklist line. All of it is merged and pushed.

Wave 2 is not complete. Its exit test, task 2d, replays real incident turns with and without the kernel, and those transcripts are on the work terminal. Task 1e waits there too. Nothing propagated downstream.

The WHETSTONE capture point went first, because 2c edits the same file. Its review found that half of the task conflicted with WHETSTONE's own plan, and the user held that half.

| Metric | Value |
|---|---|
| Tests on `main`, start of session | 403 |
| Tests on `main`, end of session | 432 (26 for the skill, 3 capture-point pins) |
| Commits | 29 on `main` before this doc (25, plus 4 merges, 2 of them into `main`) |
| Review agent runs | 8: proposer 1, code-reviewer 6 (two gates, three rounds each), test-runner 1 |
| Subagent tokens, as reported at each agent's last run | about 0.65M (resumed runs count earlier context again) |
| Gate findings, Wave 2 | 1 Critical, 18 Warning, 25 Suggestion |
| Gate findings, capture point | 0 Critical, 5 Warning, 15 Suggestion |
| Lead claims a reviewer refuted | 12 (Appendix A) |
| Lead errors the lead caught itself | 6 (Appendix A) |
| PCC check 5, at close | 0 MISSING over 34 paths (33 at `84dd487`, before this session's task-list edits); 0 MISSING-DIR over 15 |
| Downstream repos written to | 0 |

## Work Completed

### 1. The WHETSTONE capture point (merged `85342b4`)

`KB-graph: outbound from the capture-point task line to WHETSTONE D4, D10, the traversal skill, and the two canaries' session-end files → tagged the commit [gate] and copied Step 5.5 from the canaries. The walk stopped short of the plan's Wave 4 section and its "What We Do NOT Build" list; the reviewer found the conflict there. (Written at close.)`

`/session-end` Step 5 and the session doc format now ask for the `KB-graph:` line, inside the sub-topic it informed. Three pin tests hold the ask, its step, and its place.

The first commit also put Step 5.5, the upward-lesson step, into the template, on the task line's authority. The review's W4 showed the WHETSTONE plan ships that step at its Wave 4 and bars new downstream obligations before the canaries validate. The user chose to hold it, and a second commit removed it. The WHETSTONE Status Log defines the boundary between prompted and unprompted sessions by commit `1ed229c`, not by date, and reports this session apart from both.

Three review rounds: GO-WITH-FIXES, GO-WITH-FIXES, GO.

### 2. Tasks 2a and 2b: the skill (merged `ff0d8b2`)

`KB-graph: read the OVERWATCH plan, both debate reviews, the held source file, the two sibling kernel skills, and SKILLS_FRAMEWORK's Level 0 rule before drafting → chose the slim shape D1 names, kept hub-only documents out of the skill's references, and wrote incidents as shapes. (Written at close.)`

`SKILL.md` holds a six-rule kernel, the four claim states, seven probe rows, and five traps, in 105 lines of a 110 cap. `EXAMPLES.md` holds seven before/after pairs and one clean report. Each section was written against a failing test.

`proposer` stress-tested the wording and returned SHIP-WITH-FIXES. Its findings moved four rules: an absence is a claim; evidence comes after the last change; the check names the claim's outcome; evidence goes under claims a reader will act on. One proposal was declined: folding the read-only rule into rule 3, because decision D10 names it as a kernel rule.

### 3. Task 2c: the wiring

- `CLAUDE.md` gains a Claim Style block. A test fails if its six rules differ from the skill's.
- `/session-end` requires a `## Claims` table and two counts: `Overclaims the user caught this session: N` and `Overclaims a reviewer caught this session: M`.
- `code-reviewer` gains a checklist line, alone in a `[gate]` commit.
- The skill is registered in `SKILLS_FRAMEWORK.md` and `.claude/README.md`.

### 4. The Wave 2 gate

Three rounds: GO-WITH-FIXES, GO for 2a to 2c, GO for merge. The Critical finding: the skill said the read-only rule "holds" for tests through the tripwire, and the tripwire does not see overwrites. Other findings that changed the text:

- The ambient block exempted plans, and the unbuilt-venv incident is a plan. The belief a plan rests on is now a claim.
- The Pushed row held with uncommitted work, and a bare branch name in `git ls-remote` matches `feature/<branch>`.
- Example pair 1 taught a probe with a silent default: `systemctl show` prints `ExecMainStatus=0` for a unit that does not exist.
- The first 15 tests let 22 of the reviewer's 47 mutants through. There are 26 tests now, and the reviewer's last score is 61 of 81.

## Claims

| Claim | State | Evidence |
|---|---|---|
| The suite passes on `main` | tested | `.venv/bin/pytest -q` → `432 passed, 1 warning in 4.45s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `432 passed, 1 warning in 5.27s`, `exit=0`; `.venv/bin/python -V` → `Python 3.12.13`; at `84dd487`. The hub has no CI config. |
| The suite passes on Python 3.11, apart from tests that need matplotlib or pandas | tested | In a scratch venv with the dev extras: `python -m pytest -q` → `394 passed, 5 skipped, 1 warning in 1.80s`, `exit=0`; `python -V` → `Python 3.11.15`; at `84dd487`. The 5 skips are 38 tests that did not run (432 minus 394). |
| The session's work is on `origin/main` | deployed | `git rev-parse HEAD` → `84dd4871df…`; `git ls-remote origin refs/heads/main` → `84dd4871df… refs/heads/main`; `git status --porcelain` → five untracked March docs, none from this session |
| Both topic branches are merged | deployed | `git merge-base --is-ancestor d91441f main; echo "exit=$?"` → `exit=0`; the same for `2bc48cc` → `exit=0`; `git rev-parse main` equals the remote SHA in the row above |
| Both topic branches are deleted | observed | `git branch --list 'topic/*'` → no output; `git ls-remote --exit-code origin 'refs/heads/topic/*'` → no line, `exit=2`. Neither was ever pushed. |
| `SKILL.md` meets task 2a's caps, and `CLAUDE.md`'s kernel equals the skill's | tested | `wc -l` → `105`; `.venv/bin/pytest tests/unit/test_verifying_claims.py tests/unit/test_session_end_capture.py -q` → `29 passed in 0.02s`, `exit=0`; at `84dd487` |
| Living docs name no missing path | tested | PCC check 5 at `84dd487`: file pass over 33 paths → no MISSING line; directory pass over 15 → no MISSING-DIR line |
| No work-system name is in the session's changed files | tested | A 16-term grep over the changed files, the plan and the task list excepted: 1 term matches, the ordinary word "slice", in `CLAUDE.md` lines that predate the session and one review line; 0 system names. The gate reviewer's own check used 39 strings and found 0 names. |
| Nothing propagated downstream | observed | `find ~/projects -maxdepth 5 \( -name upstream-update.md -o -name doctrine-delivered \) -newermt '2026-10-01 00:00' -not -path '*/tacsop/*'` → no output, with 11 `upstream-update.md` files in range; `git diff --stat b1c3e36 HEAD -- docs/doctrine-updates.md scripts/` → no output |
| Both gates ended in GO | observed | `grep -n 'verdict' -i` on the two reports → capture point line 430, `Round 3 verdict: GO`; Wave 2 line 705, `Verdict, round 3: GO` for merge |
| The kernel changes what a model claims | observed | UNVERIFIED: task 2d, the controlled replay, needs incident transcripts that exist only on the work terminal. Until it runs, the kernel is untested text. |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 16

(12 at the close. The review in the addendum refuted 4 more.)

## Key Decisions

| Decision | Chosen | Over | Why |
|---|---|---|---|
| Release shape (user) | Hold every OVERWATCH entry until 1e and Wave 2 are done | Ship Wave 1's four entries now | Downstream gets the plan in one cycle, with the overclaim fix in it |
| Step 5.5 in the template (user) | Hold for WHETSTONE Wave 4 | Ship early, logged as out of sequence | The WHETSTONE plan bars it; OVERWATCH needs neither half |
| Rule 5's scope (user) | A checkout a timer or service runs from | Every "deployed" claim, as D10 was worded | D10's wording voids push claims in any repo with untracked files |
| Rule 4's bound (user) | Each claim a reader will act on | Every success claim, as D2 was worded | The unbounded form puts a line under every sentence and fails 2d's clean-turn limit |
| Ledger counts (user) | Two lines, N and M | N only; or one folded count | N stays comparable to the baseline; reviewer catches still get recorded |
| Merge before 2d (user) | Merge 2a to 2c now | Hold the branch for the replay | The work terminal pulls `main` to run 2d |
| Read-only rule | Its own kernel rule | Folded into rule 3 (proposer) | D10 names it as a rule |
| Commit messages | In the skill's scope | Dropped from scope | Last session's refuted claims included commit messages |

## Pillar Compliance

- **Shift-Left Testing**: every skill section, wiring surface, and gate fix had a failing test first, with two stated exceptions. The capture-point pins were written after the doc change, and four probe pins at gate round 2 pinned text already fixed; both are labeled as pins. Tests and text share commits, so "red first" cannot be re-run from history. The reviewer confirmed each commit's tests fail on its parent's tree.
- **Simplicity First**: the skill ships two files, as D1 requires. One addition goes past the plan: the second count line, which the user approved. The ledger now has two counts and three cases, and that is more than the one line the plan named.
- **Config-Driven**: no tunable entered code. The line cap and rule cap are test constants taken from the task Standards.
- **Branching**: one topic branch per plan, each merged at its own gate and deleted. The Wave 2 branch merged the capture-point branch twice to stay current, which the branching skill warns against; both merges followed a review round on that branch.

## Lessons

1. **A result written in the same command as its check is a guess.** Twice a commit message cited a number before the run printed it: tests on a tree not yet run, and 37 paths where the check counted 33. Both were amended before push. Run, read, then write.
2. **A task line is not authority over its own plan.** The capture-point task asked for Step 5.5; the WHETSTONE plan held it for Wave 4. The walk reached the plan's decisions and missed its exclusions.
3. **A probe needs one run on a name known to be wrong.** `systemctl show` reports status 0 for a unit that does not exist; `git ls-remote origin main` matches `feature/main`; a mutant that kept the pinned substring passed the pin.
4. **Tests on prose hold presence, not sense.** Only a reviewer's mutants showed what the pins missed, and even at the end 20 of 81 survive.
5. **Ambient text did not stop the author's slips.** After the kernel was in `CLAUDE.md`, the lead still made the two errors in lesson 1, and the gate rounds that followed refuted five more of its claims (Appendix A, 8 to 12). The control that worked was a second agent's re-run. Task 2d should be read with that in mind.
6. **The review write-scope rule blocks reviewer memory.** Both reviewers noted they could not update agent memory under a one-file rule. Filed as a task.

## Next Steps

1. On the work terminal: Wave 0 (0b to 0d), then task 1e (ask rules), then task 2d (the replay). 2d decides Wave 2.
2. Then the release, one cycle: seed marks for five repos, draft the OVERWATCH entries (1c alone as breaking; the Wave 2 entry lists the six surfaces its tests read), pre-flight, dry run, propagate on the lead's go. The cycle also carries the 08-27, 08-30, and 09-18 entries.
3. Watch items for 2d, from the reviews: rule 2 asks for a re-run at every report; "the belief a plan rests on is one" may raise the flag rate on clean turns.
4. WHETSTONE: settle the Wave 1 session count, and report M1 for prompted and unprompted sessions separately.
5. Filed this session: the adoption helper copies `session-end.md` without the traversal skill it points to (P3); the review write-scope rule and reviewer memory (P3); a sixth trap for the skill, from lesson 1 (P3, after 2d).

## Addendum: After the Close

The session doc was pushed at `d1deddc`. The user then asked to close the oldest P3 on the list: five untracked decision-science docs.

### 5. The five March docs

The files are the reports of the 2026-03-26 session's "Team Review + Hardening" phase, never committed. They are now tracked (`7968ee0`): four moved to `docs/reviews/` under date-first names, and the gap proposal kept its name. The task is closed (`eede414`), `/pcc` check 5 lost the allowlist line it carried for them (`68486c9`, `[gate]`), and the traversal skill lost a sentence that described that line (`2c24821`).

A fourth review, of this cleanup, returned GO-WITH-FIXES: 0 Critical, 4 Warning, 4 Suggestion ([20261001_march_docs_cleanup_review.md](../reviews/20261001_march_docs_cleanup_review.md)). Three of its findings changed the outcome:

- **The remote had moved.** Another machine pushed `952c7b3` two minutes after this box's session close. A fetch this session did not run moved the local tracking ref, and the lead committed three times on the old tip without checking it. One of the incoming commits was a `[gate]` change to the two lines above the one being removed in check 5.
- **The record overstated what was undecided.** The lead wrote that three of the gap proposal's items shipped and the rest was never decided. Five of ten shipped.
- **One phrase was new to the public tree.** The reviewer read all 1,368 lines and found nothing private, and flagged one section heading for the user. The user chose to reword it. The phrase sat in an unpushed commit, so the lead rebuilt the cleanup on the new `origin/main` in place of merging: the old commits never left this machine.

| Claim | State | Evidence |
|---|---|---|
| The suite passes after the cleanup | tested | `.venv/bin/pytest -q` → `432 passed, 1 warning in 4.70s`, `exit=0`; `CI=true .venv/bin/pytest -q` → `432 passed, 1 warning in 5.24s`, `exit=0`; Python 3.12.13; at `2c24821` |
| Check 5 is clean without the allowlist line | tested | Both bash blocks of `pcc.md` section 5, extracted and run as written → no MISSING line, no MISSING-DIR line, `exit=0`; 34 paths; at `2c24821`. Fed one old path, the file pass prints `MISSING`. |
| Both machines' gate changes to check 5 survive | tested | `git diff 952c7b3 68486c9 -- .claude/commands/pcc.md` → two removed lines, the March allowlist and its bullet, and nothing else |
| Four of the five files are unchanged from the originals; one differs by one line | written | `sha256sum` before the move and at `7968ee0` → the same four prefixes; `diff` of the fifth against its original → one line removed, one added |
| The reworded label is in no commit that will be pushed | tested | A `git log -G` search for the label over `origin/main..main` → 0 commits, `exit=0`; `git grep` for it over the tracked tree → `exit=1`; the same search over the discarded commits prints one, so the search can fail; at `2c24821` |

**Lesson 7. Check the remote before committing on top of it.** `git ls-remote origin refs/heads/main` against the commit the work sits on takes one line. Two machines push to this repo's `main`, and `/session-start` is the only step that syncs.

## Commits

| Commit | Change |
|---|---|
| `d565df9`, `8c31948`, `1ed229c`, `3820b95`, `7e2778b`, `23fbf17`, `c1d5b66`, `d91441f` | The capture point, its pins, and three rounds of review fixes |
| `85342b4` | Merge the capture point |
| `ef5b488`, `4b11ec3` | Tasks 2a and 2b |
| `d2cdaf8` | The kernel after the proposer's stress test |
| `cbd2ef5`, `1edf0d4`, `d1614fc` | Task 2c: the ambient kernel and registry, the reviewer line, the Claims table |
| `f100c2b`, `c97c79e`, `cea55fe`, `fcf63c3`, `2bc48cc` | OVERWATCH Status Log entries |
| `1b50924`, `6bde122` | Gate round 1 fixes |
| `278a426` | Gate round 2: four pins, three wording slips |
| `447a459`, `c58e69e` | The ledger's two counts and their definitions |
| `ff0d8b2` | Merge tasks 2a to 2c |
| `84dd487` | Task list |
| `d1deddc` | Session close |
| `7968ee0`, `eede414`, `68486c9`, `2c24821` | After the close: the five March docs, the task close, the check 5 allowlist, the traversal skill sentence |

## Appendix A: The Lead's Claims and Errors, by Who Caught Them

**Refuted by a reviewer's re-run (16, the M count; 13 to 16 came after the close)**

| # | Claim | Where | Caught by |
|---|---|---|---|
| 1 | The capture point "shipped", on an unmerged branch | `docs/tasks.md` | capture round 2, N2 |
| 2 | "Three lines in the format doc" (five were added) | `1ed229c` | capture round 2, N3 |
| 3 | "Three pin tests" in `8c31948` (they span later commits) | `docs/tasks.md` | capture round 2, N3 |
| 4 | Placement lets the M3 order check work (it tells the verifier which edit to read) | WHETSTONE Status Log | capture round 2, N4 |
| 5 | "The pin now matches the whole instruction" | `7e2778b` | capture round 3 |
| 6 | "Each probe was run in this repo" (two rows have nothing to run against here) | `ef5b488`, and a message to the user | gate round 1, claim 4 |
| 7 | "Rule 6 holds for them through the test tripwire" | `SKILL.md` | gate round 1, C1 |
| 8 | The tests pin "each markable Standard" | OVERWATCH Status Log | gate round 1, W14 |
| 9 | "From `1b50924` on the messages carry them" | OVERWATCH Status Log | gate round 2 |
| 10 | "The new tests expect five surfaces" (six) | OVERWATCH Status Log | gate round 2 |
| 11 | "Every refuted claim lands in one" count | `447a459` | gate round 3 |
| 12 | The release entry "lists all six" surfaces (no entry exists) | OVERWATCH Status Log | gate round 3 |
| 13 | The gap proposal's "rest was never decided" (five of ten shipped) | first cleanup commit, rebuilt before push | cleanup review, W2 |
| 14 | "Four bias items" never decided (one shipped as the range warning) | first task-list line | cleanup review, W2 |
| 15 | The task was "open since March" (the line dates from 2026-07-20; the files from March) | first cleanup commit | cleanup review, S1 |
| 16 | `d1deddc` is `origin/main`, and "nothing has gone to origin" (another machine had pushed) | the review brief, and a message to the user | cleanup review, W1 |

Number 6 is counted here although the reviewer marked it unverifiable: the lead said it to the user, and it was true of five rows, not seven. The user did not act on it, so it is not in N. Text defects the reviewers found in the skill (a pasted `exit=1` that `tail` cannot print, the Pushed row, pair 7's line) are findings, not claims, and are in the reports.

**Caught by the lead's own re-run (7, in neither count)**

1. An exit status read after a pipe reported `tail`, not pytest. The trap is now in the skill.
2. `1b50924`'s message said the tests pass before they ran on that tree. Amended to cite the run; the tree did not change.
3. The task-list commit said 37 paths; the check printed 33. Amended.
4. A merge command failed (`git merge` cannot read its message from stdin) while the next line printed "merged". The unchanged SHA and the 403 count showed it.
5. A Status Log draft said 26 Suggestions and "5 of 86" claims; a count of the report's headings gave 25, and 3 of 86 plus 2.
6. `6bde122` marked the full 3.11 run UNVERIFIED. It was a skipped check; the lead then ran it.
7. After the close, an exit status read after a pipe a second time (`git grep` piped to `cut`), in the search for the reworded label. Re-run with the status read directly.
