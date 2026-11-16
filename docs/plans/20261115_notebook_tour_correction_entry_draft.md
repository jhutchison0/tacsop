# Draft: Correction Entry for the Notebook Tour

**Date**: 2026-11-15
**Status**: Superseded 2026-11-16 by the entry "2026-11-16: Notebook Tour Correction" in `docs/doctrine-updates.md`. The user ruled: a correction entry, not a skill, and the narrow module change (rename to `PACKAGE`, `DISPLAY_NEEDS = None`, the split test, plus a cell that skips now fails the run test). This draft's counts ("five tests", "one failure and four skips") predate that change; the entry's are measured.
**Corrects**: the entry "2026-11-14: A Notebook Tour, Held by the Suite", delivered to 23 repos on 2026-11-14.
**Basis**: thirteen first tours built on 2026-11-14 and 2026-11-15, each reviewed by `code-reviewer`. The reviews' "For the hub" sections are in each repo's `docs/reviews/20261115_notebook_tour_review.md` on its `topic/notebook-tour` branch.

---

## Why a correction is due

The delivered entry tells a consumer to copy the test module at `8c3b69a` and expect four tests. Two holes were found in that module within hours, and the hub closed both:

| Hub commit | What it closed | Found by |
|---|---|---|
| `b3890e2` | A tour committed with its own-data guard switched on passed the module, so the suite would read the reader's data on every run. | the first review |
| `97b3c42` | The guard test read plain assignments only; an annotated assignment, a tuple target, or a walrus after the `= None` line evaded it. | a later review |

Every one of the reviews also found a fault that the delivered rules did not name. The same faults recurred across repos, which is the evidence that they belong in the rules and not in one repo's review.

## Proposed changes to the test module

These change a file consumers were told to copy, so they wait for the user's ruling.

1. **Pin `97b3c42` or later** in row 1, and say five tests and three constants (`OWN_DATA_GUARDS` is the third).
2. **Rename for a repo that draws nothing.** Twelve of thirteen tours draw nothing. `DISPLAY_HOME` becomes `PACKAGE`, and the test `test_it_draws_nothing_of_its_own_and_shows_a_display_from_the_display_home` becomes two: one that the notebook imports the package, one that it imports no charting library.
3. **Make the figure parts optional by construction**, not by deletion. Today a no-figure repo deletes `DISPLAY_NEEDS`, the `importorskip` line, the `MPLBACKEND` line, the `finally` block and the `sys` import; every builder had to be told the last two.
4. **Ship it formatted** at 88 columns, so a consumer whose CI runs black or ruff on `tests/` does not reflow it. Three repos reformatted it and their diffs against the hub filled with noise.
5. **Hold what the cells change.** The run test restores the working directory and `sys.path`. It should also snapshot `os.environ` and fail if the cells leave it changed, and collect garbage with `ResourceWarning` as an error so an unclosed temporary directory fails here and not in a later test.
6. **Let a scratch copy be tested.** An environment override for `NOTEBOOK_DIR` would let a mutant battery run against a copy without touching the working tree.

Known limit, to state and not to chase: the guard test still passes `globals()["MY_X"] = path` and `for MY_X in [path]: pass`. Review holds those.

## Proposed additions to the rules

Each line is a fault at least one review found in a built tour.

**Rule 1a (hermetic, not only offline)**

- A cell that runs `git` or another program drops inherited `GIT_*` variables and closes global and system config. One tour committed into an outer repository through an inherited `GIT_DIR`.
- Per-user caches, config files and the metadata of installed packages are pointed at an empty temporary location. One tour's results differed by machine while making no network call.
- Blocking `socket.connect` does not block name lookups or a lazy first-use download. Block `socket.getaddrinfo` and stub the loader.
- A committed config file the package hardcodes may be read, once the reviewer has screened it; `os.chdir` in `try/finally` inside one cell is the accepted workaround.
- A repo whose own suite makes live requests is run by named test paths, not whole.

**Rule 4 (asserts)**

- Negate every assert, one at a time, and report survivors. This is the only mechanical check that reaches rule 4.
- Negation cannot see a true assert under a false sentence. The reviewer asks of each section: would this assert fail if the sentence above it were false?
- An assert on a reduced value (time of day, a rounded number, a prefix, a subset) is checked against what the reduction drops. One such assert hid a wrong date; another hid a defect in a config.
- Where the package turns an exception into a warning, the tour asserts the warnings are clean.
- A status claim about what does not exist yet is asserted (`find_spec(...) is None`), so the tour fails when that changes.
- For each method a section rests on, check the product calls it. Three tours were built on a function with no caller.

**Rule 5 (hands-on)**

- The change-it cell's asserts hold for every value its text suggests. Four tours failed on their own suggested values.
- The own-data cell reads data and never executes a reader's string.
- Where a result depends on a reference fitted from the fixtures (a baseline, a calibration), the reader's data scored against it is wrong in a known direction. The cell takes the reader's own reference or stops before the score.
- The own-data cell takes its date and clock from the reader's data, refuses a URL, and does not suggest a file name inside the repo without an ignore line.
- A safeguard on the main path (a machine gate, an arming flag) may be stood in for over invented fixtures only, inside one cell, never for the own-data cell. The tour states each such flag's default and tells the reader not to change it.

**Rule 6 (fixtures and output)**

- Label per table where a file mixes public and invented data. Where the format has no comment syntax, label in the opening cell and the test docstring.
- A generated fixture ships its generator.
- No printed line carries an absolute path. Where results are sensitive, the printed output says "invented", not only the fixture.

**New: every cell is safe to run twice**, and a patch starts and stops inside one cell. A patch closed in a later cell leaked into the rest of the suite when a cell between them failed.

**New: a defect the tour finds** is stated in the cell, pinned by an assert marked as a known defect, and filed as a task. Fixing it then fails the tour until its text is updated.

**New: say what the tour does not show** in the opening cell, and where the repo is mid-build, name the full path and the part that runs today.

## Proposed additions to the steps

- **Detect**: anything that enumerates top-level tracked paths (one repo copies its tree into agent worktrees, and a new `notebooks/` folder carried a task's answer there until its tripwire test failed). The entry's "nothing else depends on these files" is false for such a repo.
- **Step 1**: with no notebook the module reports one failure and four skips.
- **Step 4**: run mutants without `-x`, with the expected counts (one failure for a saved output or a false assert, two for a charting import or a guard switched on), and add the guard-on mutant and the per-assert negation.
- **Row 2**: the model's first cell becomes two, path setup then imports, so ruff's per-cell E402 needs no suppression. Put the working-directory assert, with a message, above the first fixture read.
- **Row 4**: name the requirements-file form (`requirements-notebook.txt`) for a repo with no `pyproject.toml`.
- **Row 5**: the README install line is run in a venv built from nothing. A hand-patched build venv hid a broken dependency spec from every test. The README names a front end; `ipykernel` gives a kernel and no notebook server.
- **Row 6**: where a repo already has teaching notebooks, ask whether the tour gives away what they ask the learner to predict.
- **New row**: a repo that ignores `*.ipynb` needs `!notebooks/tour_*.ipynb`.
- **New row**: where ruff lints notebooks, run `ruff check .`; if an ignore is needed, E402 only, for `notebooks/**/*.ipynb`.
- **Subject-matter repos**: a tour that explains a method (game theory, stylometry, a scoring model) needs a reader who knows the subject, or the repo's oracle tests as reference. An assert can be true and match its sentence while the sentence teaches the wrong concept.

## For whoever briefs agents to build tours

- Pass `--python` an absolute path or one starting with `./`. A bare name is read by uv as a version request; one reviewer's install landed in the hub's own venv that way.
- Work in a worktree outside the tree that propagation discovery scans, on a topic branch, unpushed.
- Forbid outside lookups, name the tests a reviewer may run in a repo with device or network tests, and require every probe and scratch directory to be removed.
- A builder's "whole suite passed" is checked by the reviewer. One was wrong.

## Decisions for the user

1. Send this as a correction entry, or fold it into a Level 0 skill and send that instead? The list above is long for an entry and is the body of a skill.
2. Apply the module changes in section "Proposed changes to the test module"? The thirteen built tours carry copies between `8c3b69a` and `97b3c42` with local edits.
3. Rename `DISPLAY_HOME`? It changes a constant every built tour sets.
