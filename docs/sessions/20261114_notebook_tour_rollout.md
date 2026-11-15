# Session: The Notebook Tour, From One Repo's Habit to Thirteen Reviewed Branches

**Date**: 2026-11-14 into 2026-11-15 (Nidhogg)
**Branch**: main
**Tags**: #session #doctrine #testing #decision-science #agents

**Documents**: [20261114_notebook_tour_proposal.md](../plans/20261114_notebook_tour_proposal.md), the proposal; [20261115_notebook_tour_correction_entry_draft.md](../plans/20261115_notebook_tour_correction_entry_draft.md), the unsent correction; [20261114_notebook_tour_preflight.md](../reviews/20261114_notebook_tour_preflight.md), the pre-flight review
**Implements**: [doctrine-updates.md](../doctrine-updates.md), the entry "2026-11-14: A Notebook Tour, Held by the Suite"
**Follows**: [20261104_handbook_as_trimmed_tacsop_downstream.md](20261104_handbook_as_trimmed_tacsop_downstream.md)

---

## Summary

The user asked to formalize a habit that began in `assay`: a notebook that walks a repo's main path over committed fixtures, with the test suite running every cell. The session built the hub's own tour, wrote the proposal and a doctrine entry, propagated the entry, and then had the hub's agents build a first tour in thirteen repos overnight, each on an unpushed topic branch in a separate worktree, each reviewed by `code-reviewer` and fixed. Every review returned merge-after-fixes. The reviews found faults the entry's rules did not name, so a correction is drafted and unsent. Nothing was pushed or merged; the user rules on each branch.

| Measure | Value | How measured |
|---|---|---|
| Hub suite at close | 576 passed, 1 warning | `.venv/bin/pytest -q` |
| Hub suite at session start | 566 passed, 1 warning | `.venv/bin/pytest -q` at `/session-start` |
| Repos sent the entry | 23, one entry each; `assay` skipped | the live run's output; a repeat dry run printed "would send nothing" for all 23 |
| Tours built, reviewed and fixed | 13 | `git log` in each worktree: a build, a review and a fix-up commit |
| Tours built and not reviewed | 1 (`urd`; recommended for dropping) | the same |
| Review verdicts | 13 of 13 merge-after-fixes; 5 held at least one Critical | each review's final message |
| Branches on a remote | 0 of 14 | `git branch -r --contains HEAD` in each worktree |

---

## Work Completed

### 1. Two decision-science fixes before the tour (`acdab6e`)

`exponential()` raised `ZeroDivisionError` for a rate under about 2.2e-16 and returned a wrong utility at 1e-12 without raising. Rates below 1e-8 in magnitude now return the linear value, the function's limit. Both `ImportError` hints now print `uv pip install --python .venv`. Tests first: four hint tests and four of five small-rate cases failed before the change. The source edits went through Bash, so the audit hook logged nothing for them (gap G2).

### 2. The hub's own tour (`a7ab4ca`)

`notebooks/tour_from_a_model_to_a_ranking.ipynb`, 23 cells, ranks four invented depot sites on four criteria: the model as YAML, value functions, one score explained, the ranking and dominance check, three figures, three sensitivity tools, a hands-on section, and a guarded cell for the reader's own model. `tests/unit/test_notebooks.py`, ported from `assay`, was written first and seen failing with no notebook. A `notebook` extra holds `ipykernel` alone.

The first render showed that `radar_chart` plots weighted contributions; the text beside it said unweighted. The text was corrected. The tour also showed that the March proposal for a `direction: minimize` key is not needed: `low` above `high` expresses a cost.

### 3. Proposal, entry, pre-flight, propagation (`8c3b69a`, `ccf8eca`)

The proposal states seven rules, three held by the test module and four by review, with suggestions by repo shape. `code-reviewer` pre-flighted it and the entry: go-with-fixes, 2 Critical and 8 Warning. Nineteen of thirty further mutants passed the first test module: a comment satisfied the import rule, seven one-line import forms evaded the charting rule, a notebook in a subfolder was never collected. The module now reads imports from the syntax tree and globs recursively. The entry's rollback no longer deletes notebooks the tour did not create. All findings were applied before the live run.

The live run sent one entry to each of 23 repos. At the dry run, 11 of the 23 still held an unread notification and 12 had consumed theirs, which is this cycle's consumption record (protocol step 6).

### 4. Thirteen first tours

Builders were `python-prototyper`, reviewers `code-reviewer`, each briefed from one shared file that grew as reviews came back. Each tour lives in a worktree outside the tree that propagation discovery scans, on `topic/notebook-tour`, so no working checkout changed under its owner.

Repos: `skald`, `hallmark`, `stx-server`, `propter`, `daily_weather`, `paperboy`, `fist`, `schelling-point`, `veil-engine`, `quest-engine`, `agent-eval`, `tactics-game`, `project-megan`. `urd` was built and not reviewed: its tour covers only a template utility, so the lead recommends dropping it. `assay` was left alone as the origin of the practice, and `elephant-graveyard` because its consumer status is an open task.

Per-repo findings stay in each repo: the review report is `docs/reviews/20261115_notebook_tour_review.md` on that repo's branch. The lead's summary for the owner, with commit hashes and the defects the tours found, is a file outside every repository, beside the worktrees.

### 5. The test module, hardened twice more (`b3890e2`, `97b3c42`)

The first tour review showed a tour committed with its own-data guard switched on still passed, so the suite would read a reader's data on every run. A fifth test now requires each guard name to be assigned `None`. A later review evaded that test with an annotated assignment, a tuple target and a walrus; the test now reads those forms too. Each change was driven by its mutant: passing before, failing after. Two forms still evade it (`globals()[...] = `, a `for` target) and are left to review.

### 6. What the reviews taught

The same faults recurred across repos, which is the case for putting them in the rules. The full list is the correction draft. The ones that mattered most:

- **A true assert under a false sentence.** Negating every assert found no survivor in tours whose prose described the wrong function, the wrong concept, or a file the product does not read. Review must ask whether the assert would fail if the sentence were false.
- **Offline is not hermetic.** Tours read a per-user cache, installed-package metadata, an inherited `GIT_DIR`, and a name lookup, while making no connection.
- **The own-data cell is where a tour does harm.** One executed a reader's code string; one scored real text against a reference fitted on invented text and would have reported the wrong answer in a known direction; one would have been copied into an evaluation harness's worktrees with a task's answer in it.
- **A tour finds defects.** Reviews confirmed defects in the toured code in most repos. The useful pattern: state the defect in the cell, pin it with an assert marked as known, file a task.
- **A builder's "suite passed" needs a second run.** One builder ran the suite before staging, so a test that reads tracked files never saw the new folder.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes at close | tested | `.venv/bin/pytest -q` → `576 passed, 1 warning`; the same with `CI=true` after the last module change |
| The entry reached 23 repos and not `assay` | observed | live run exit 0 with 23 `Notified` or `Appended` lines and one `[skip] github/assay`; `grep -c` of the entry's heading printed 1 in four sampled notification files; a repeat dry run printed "would send nothing" for 23 |
| The hardened module kills the evasions it was changed for | tested | five formerly surviving mutants each failed after `8c3b69a`; the guard-on mutant passed at `8c3b69a` (4 passed) and failed at `b3890e2`; annotated, tuple and walrus forms passed at `b3890e2` and failed at `97b3c42` |
| The hub tour runs in a real kernel | tested | a script over `jupyter_client` ran every code cell in `ipykernel`: `errors: 0`, one PNG from each of three figure cells |
| Each of the 14 worktrees is clean and on no remote | observed | per worktree, `git status --porcelain` printed nothing and `git branch -r --contains HEAD` printed nothing |
| The lead re-ran the whole suite in 5 of the 13 reviewed branches after the last commit | tested | `skald` 274 passed; `hallmark` 293 passed; `propter` 1299 passed, 8 skipped; `paperboy` 369 passed, 1 skipped with `-W error`; `agent-eval` 1068 passed |
| The lead re-ran only the notebook tests in the other 8 | tested | `5 passed` in each of `stx-server`, `daily_weather`, `fist`, `schelling-point`, `veil-engine`, `quest-engine`, `tactics-game`, `project-megan` |
| No private term is in the hub's unpushed commits | tested | `/pcc` check 7 over the index and the unpushed commits: 0 content hits, 0 message hits, list present |
| Any tour opens correctly in a notebook front end | UNVERIFIED | no front end was opened; gap G14 |
| The whole suite passes in the 8 branches where the lead ran only the notebook tests | UNVERIFIED | the builders' and reviewers' runs say so; the lead did not repeat them. One of those repos' suites makes live requests and one runs device tests, so the lead chose not to |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 3, all the lead's, in the proposal before it was committed: "the test module is 70 lines" (71), "ports by changing two constants" (the entry's own row changed a third thing), and "the suite runs the notebook on every run" (it skipped where matplotlib was absent). A fourth belongs to a subagent: a builder reported a suite green that was red at its commit.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Formalize the tour; propagate; build first tours overnight | the user | Stated 2026-11-14 |
| Musts and recommendations, not one rule set | the lead, accepted by the user | Three rules a test can hold; the rest need a reader |
| "Show a result", not "draw a chart" | the lead | Twelve of thirteen tours drew nothing; a table is a result |
| An entry and a test file now, a skill later | the lead | Evidence was two repos; thirteen reviews later the rule list is skill-sized, and the correction draft asks the user |
| Worktrees outside `~/projects`, topic branches, no push | the lead | A working checkout may be dirty or run by a timer, and discovery would have found a worktree under `~/projects` |
| The correction stays a draft | the lead | It changes a file 23 repos were told to copy; that is the user's call |
| One harness-integrity line and one dependency pin, each in its own commit on its repo's branch | the lead | Each branch was red without it; alone, the owner can accept or drop it |
| Seven packages a reviewer installed into the hub venv by mistake were left in place | the lead | Prior absence is unproven; removing a package the user had is the worse error |
| No per-repo defect detail in this public repo | the lead | Output goes to the repository that owns the sensitivity of its input |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS, with a flag | The test module grew from 71 to 130 lines across three hardenings, each closing an evasion a review demonstrated. The correction draft proposes renames that would simplify it for repos that draw nothing. |
| **Shift-Left Testing** | PASS | Every source change and every module change was driven by a failing test or a surviving mutant first. Source edits went through Bash, outside the audit hook (gap G2). |
| **Config-Driven** | PASS | The hub tour's model and alternatives are YAML fixtures. |

Deviations from the environment rules, caused by this session's agents: a wrong-venv install into the hub's `.venv` (a bare name after `--python`); a repo's whole suite run where it makes live requests; a repo's whole suite run where its marker does not exclude device tests; 1,663 temporary folders left under `/tmp` by a probe whose cleanup was refused.

---

## Commits

| Hash | Subject |
|---|---|
| `acdab6e` | [fix] exponential() is linear below rate 1e-8; install hints name --python .venv |
| `a7ab4ca` | [feat] A notebook tour of decision_science, held by the suite |
| `8c3b69a` | [test] The notebook test reads imports from the syntax tree and holds subfolders |
| `ccf8eca` | [doc] Notebook tour: proposal, doctrine entry 2026-11-14, and the pre-flight review |
| `b3890e2` | [test] The notebook test refuses a tour committed with its own-data guard on |
| `97b3c42` | [test] The own-data guard test reads annotated, walrus, augmented and tuple assignments |
| this doc | [doc] Session 2026-11-14: the notebook tour rollout |

All local. The hub is not pushed; the user did not ask for a push.

---

## Next Steps

1. The user reads the summary beside the worktrees and rules on each of the fourteen branches: merge, change, or drop.
2. The user accepts or drops the two stand-alone commits (a worktree strip-list line in one repo, a dependency pin in another).
3. The user rules on the correction: an entry or a skill, and whether the module's constants are renamed.
4. The user decides about the seven packages in the hub venv, and pushes the hub.
5. Open one tour in a notebook front end (gap G14) before merging any.
6. The four decisions in the proposal are still open.

---

## Addendum, 2026-11-15: Critical repairs, the hook fix, and the merges

The user asked for the reviews' Critical findings to be repaired under the lead's review, then for the duckdb pin to be lifted, the hook flaw fixed, and the branches merged.

- **Seven Criticals, five repos.** The lead re-checked each at its branch head with a probe that could fail; all seven were closed. Two had been contained in the tour while the cause stayed in the repo's code, so a `python-prototyper` repaired each cause in one commit: `hallmark`'s git calls and test fixtures no longer follow an inherited `GIT_DIR`, and `propter`'s store runs under DuckDB 2. The lead re-ran both whole suites, the second under both DuckDB versions, and then lifted the pin.
- **The hook flaw, found by that review.** With `GIT_DIR` inherited, the shift-left audit hook resolved another repository as the project root and wrote its log there, and the hook's tests built their throwaway repos in the wrong place. A test written first failed (`1 failed, 19 passed`); the hook now unsets git's own list of local variables before `git rev-parse` (`c5f1c96`, a `[gate]` commit alone; the test is `1c3212d`). Consumers still carry the old hook: the fix is not propagated.
- **Thirteen merges.** Each tour branch was merged with a merge commit into the branch it was cut from, and its branch and worktree deleted. `urd` was left unmerged. Nothing was pushed, here or in any consumer.

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes with the hook fix | tested | `.venv/bin/pytest -q` → `577 passed, 1 warning` |
| The hook tests hold under an inherited `GIT_DIR` | tested | `GIT_DIR=<scratch>/.git GIT_WORK_TREE=<scratch> .venv/bin/pytest -q tests/unit/test_shift_left_hook.py` → `20 passed`; the scratch folder held `.git` alone afterwards |
| Each merged tree is the tree that was tested | observed | per repo, `git diff --quiet HEAD topic/notebook-tour` exited 0 after the merge; the notebook tests printed `5 passed` on each branch head before it |
| Thirteen topic branches are gone | observed | `git branch --list topic/notebook-tour` printed nothing in each of the thirteen |
| The hook fix reached any consumer | not done | no entry was written or sent |
| Any tour opens correctly in a notebook front end | UNVERIFIED | still gap G14 |
