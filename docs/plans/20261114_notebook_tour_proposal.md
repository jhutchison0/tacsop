# Proposal: A Notebook Tour in Every Working Repo

**Date**: 2026-11-14
**Status**: Proposed; rollout directed by the user on 2026-11-14, four decisions open.
**Author**: the lead
**Evidence**: two instances. `assay` (home branch, 2026-11-14, one tour, uncommitted there on that date) and this hub (`a7ab4ca`, `notebooks/tour_from_a_model_to_a_ranking.ipynb`).

---

## The point

A working repo should carry one notebook that walks its main path, from a raw input to a result a person can see, over small committed fixtures, and the test suite should run that notebook wherever its dependencies are installed. The notebook is how a colleague learns what the repo does; the suite is what keeps the notebook true.

## Problem

Several working repos have no way to show a newcomer what they do. A README describes; it does not run. A demo script runs and shows nothing a person can change. Lane 01 of the AI CoP used a notebook with a hands-on section; no comparison was measured.

A notebook without a test rots. Its cells are code that no suite runs, so the first refactor breaks them and nobody learns of it until the next demo. A notebook saved with outputs has a second fault: its last section usually points at the reader's own data, and a saved output publishes that data.

## What a tour is

One notebook per repo, at `notebooks/tour_from_<input>_to_<result>.ipynb`. It builds on the repo's own code, shows a result, and gives the reader something to change. It is not a lesson on a concept (that is a lane) and not an analysis (that is a report).

## The musts

Seven rules. One test module holds the first three, less the fixture, network and secrets clause of rule 1 and one evasion of rule 3; review holds the rest. Pre-flight review: `docs/reviews/20261114_notebook_tour_preflight.md`.

| # | Rule | Why | Held by |
|---|---|---|---|
| 1 | The suite runs every code cell, in order, in one namespace, with the working directory at `notebooks/`. No kernel. | A cell that no suite runs is a cell that breaks unseen. | `test_every_code_cell_runs_in_order_over_the_committed_fixtures` |
| 1a | The cells read only committed fixtures. No network, no secrets. | A tour that fetches or reads a key cannot run everywhere the suite does. | review (and the isolation tripwire, where a repo has `tests/isolation.py`) |
| 2 | The notebook is committed with no outputs, no attachments, and no widget state. | An output from the reader's own data publishes it. | `test_it_is_committed_without_outputs` |
| 3 | The notebook imports the repo's package and imports no charting library. A figure comes from a function in the package. | The demo must show the repo's code, not a second copy of it; and one home for figures keeps them alike. | `test_it_draws_nothing_of_its_own_and_shows_a_display_from_the_display_home`; review for a cell that draws on a figure the package returned |
| 4 | Each code cell asserts what the text above it claims. | Rule 1 proves a cell runs; only an assert proves it shows what it says. | review |
| 5 | The tour ends hands-on: a cell to change, a cell that fails on purpose and prints the real error, and a cell for the reader's own data behind a guard that is off by default. | The reader learns the repo by changing it and by meeting its errors in a safe place. | review |
| 6 | Fixtures are invented or public, small, committed, and say which in a comment. | A tour over private data cannot be shared, and a tour over fetched data cannot run in the suite. | review |
| 7 | The kernel is its own extra, `notebook`, holding `ipykernel` alone, and is left out of `all`. | The suite needs no kernel; a person opening the notebook does. | review |

Rule 3 does not require a chart. A table or a printed line is a result. When a repo has no display function and the numbers are few, the tour prints a table. When a figure would carry more, the function goes into the package, test-first, and the notebook calls it.

The test module (`tests/unit/test_notebooks.py`) ports by changing two constants, the package a notebook must import and the optional dependency its figures need, and one path where tests do not sit in `tests/unit/`. A repo that draws nothing deletes the second constant.

## Recommendations by repo shape

These are suggestions, not rules. Each names the fixture to build, what to show, and what the hands-on cell changes.

| Repo shape | Fixture | Show | Change it, break it |
|---|---|---|---|
| Pipeline (ingest, transform, write) | Three to ten raw records, one of them malformed | One record followed from raw to final row; a table of counts at each stage (read, kept, set aside) | Edit a record; feed the malformed one alone and read the error or the quarantine reason |
| Decision or scoring model | A model file and three to five alternatives | The ranking as a table; what each criterion contributes; how the ranking moves when weights move | Change the weights; give weights that do not sum to 1 |
| Simulation or engine | A seed and the smallest scenario that produces an interesting state | State before and after N steps; one quantity over time as a table or the repo's own figure | Change the seed or one parameter; pass a parameter out of range |
| Service or API | A recorded request and its expected response | The handler called in process, no server and no socket; the response read field by field | Change a request field; send a request that fails validation |
| Command-line tool | A small input tree under the fixtures | The command's entry function called in process; the report it writes, read back | Change an option; point it at an input it refuses |
| Scheduled job or report | One frozen day of input | The artifact the job renders for that day, and the numbers behind one line of it | Change the day's input; remove a required field |
| Anything that calls a model or a remote API | A recorded response, committed | The code path from the recorded response onward | A live call belongs only in the guarded own-data cell, never in the path the suite runs |

Preparing the fixture is most of the work. A repo whose only inputs are private or live needs an invented input first, and writing one often shows where the code assumes its production data.

## What the two instances showed

- **The test catches rot and wrong claims, within limits.** At the hub, four mutants each failed the module: a saved output, a false assertion, a `matplotlib` import, and a cell that raises. The pre-flight review then ran 30 more; 19 passed the first module and 9 still pass the hardened one (a false assert inside `try/except`, every assert deleted, a pasted table in a markdown cell, an environment key read, and the like). Those nine are why rules 1a and 4 to 7 are review rules.
- **A tour finds faults in what it tours.** The hub tour's first render showed that `radar_chart` plots weighted contributions; the text beside it said unweighted. Preparing for the tour found a crash and a silent wrong answer in `exponential()` for small rates (`acdab6e`).
- **A tour answers design questions.** The March gap analysis proposed a `direction: minimize` key. The tour teaches the existing way, `low` above `high`, in one paragraph, so the key is not needed.
- **The rule on charts held in a repo that draws.** All three hub figures come from the package.

## What this is not

- **Not a requirement to chart.** See rule 3.
- **Not a replacement for unit tests.** The tour test is one coarse test of the main path.
- **Not a place for real data.** Rule 2 and rule 6 together keep it out.
- **Not a lane.** A lane teaches a concept to participants and is completable with a terminal and a browser; a tour shows one repo to a colleague. They can share the test module.

## Rollout

1. This proposal and a doctrine entry, reviewed by `code-reviewer` before the entry propagates.
2. Propagation by hand with `scripts/propagate_doctrine.py`, dry run first. Adoption is each repo's call.
3. First tours built by the hub's agents in the repos the user named, each on a `topic/notebook-tour` branch in a separate worktree, unpushed and unmerged, so no working checkout changes under a running job. `assay` is left alone: it is the origin of the practice and the hub never writes into it.
4. Each tour is reviewed by `code-reviewer` against the seven rules; the report goes into that repo's `docs/reviews/` on the same branch.
5. The user reads the branches and merges, changes, or drops each.

## Decisions for the user

1. **A skill, or an entry and a test file?** This proposal ships the practice as a doctrine entry and one test module. A Level 0 skill (`building-notebook-tours`) would give agents the rules at the point of use, at the cost of four registration surfaces. Recommended: decide after the first tours report.
2. **The trigger.** `assay` wrote "a change that adds something a new user would run lands with a notebook section". This proposal says "one tour per repo, on its main path", which a test can check. Should a repo's tour also grow when its main path grows, and who says so?
3. **Does the template ship a tour?** The hub now has one. A bootstrap that copies it would start every new repo with a notebook about decision science, which most would delete.
4. **Rule 3 for a repo with no figures.** Is "print a table, or add the function to the package" enough, or should some repos be allowed to draw in the notebook?
