# Review: Notebook Test Module, Port by Constants (Correction Items 2 and 3)

**Author**: code-reviewer
**Date**: 2026-11-16
**Type**: Code review (test module that consumers copy, and its new port test)

**Verdict: APPROVE WITH FIXES.** No Critical findings. The module refuses every tour it refused before, failure for failure, and a repo that draws nothing now ports it by setting three constants and deleting nothing. Fix Warning 1 before committing: it is one assert, and without it the port test cannot tell a run test that executes cells from one that executes none. Decide Warning 2 in the same commit, because every module change costs a re-copy in 23 repos.

Reviewed: the uncommitted diff to `tests/unit/test_notebooks.py` and the new `tests/unit/test_notebook_module_port.py`, against `docs/plans/20261115_notebook_tour_correction_entry_draft.md` items 2 and 3, the delivered `## 2026-11-14` entry in `docs/doctrine-updates.md`, and the evasions in `docs/sessions/20261114_notebook_tour_rollout.md` sections 3 and 5 (itemized in `docs/reviews/20261114_notebook_tour_preflight.md`, Mutants).

## What was run

| Check | Result |
|---|---|
| `.venv/bin/pytest -q -rA tests/unit/test_notebook_module_port.py tests/unit/test_notebooks.py` | `9 passed in 1.28s` |
| `.venv/bin/pytest -q` | `578 passed, 3 skipped, 1 warning in 6.75s` |
| `CI=true .venv/bin/pytest -q` | `578 passed, 3 skipped, 1 warning in 8.54s` |
| Tour mutant battery, HEAD module against new module, hub configuration (T0 to T10 below) | 11 of 11 refused the same way by both modules; T10 escapes both |
| Same tours in a repo configured to draw nothing, through the port test's own helper (N0 to N6) | refused as expected; N4 escapes |
| Module mutants against the port test (P0 to P6) | P1 and P6 survive all three port tests |
| Em and en dash search, both files | 0 matches |
| `git status --porcelain` after the battery | the lead's entries plus this report. `docs/doctrine-updates.md` became modified during the review (file time 10:30, a new correction entry); this review did not write it |

All mutants ran in a `git archive HEAD` copy under `/tmp`, with the working tree's two test files copied in. The copy was removed afterwards. Nothing in the working tree was written except this report.

## The three questions

**Does `if DISPLAY_NEEDS:` open a new evasion?** No. In the hub's configuration the run test's code path is unchanged, and the split's two tests refuse exactly the union of the old combined test's two asserts. In a repo that draws nothing, `DISPLAY_NEEDS = None` behaves like the old instruction to delete three lines. A drawing repo that sets `None` by mistake fails where its library is absent; it does not skip. That fails closed.

Evidence (hub configuration; failing tests named; HEAD's combined test abbreviated `draws`):

| Mutant | HEAD | New |
|---|---|---|
| T0 baseline | `5 passed` | `6 passed` |
| T1 `import os, matplotlib.pyplot as plt` (E3) | `draws`, run | charting, run |
| T2 `from pylab import plot` (E7) | `draws` | charting |
| T3 `plt = __import__('matplotlib.pyplot').pyplot` (E1) | run | run |
| T4 `x = 1; import matplotlib.pyplot as plt` (E4) | `draws`, run | charting, run |
| T5 package import deleted | `draws`, run | package, run |
| T6 package named in a comment, loaded by `importlib` (E9) | `draws` | package |
| T7 `MY_MODEL` switched on | guard | guard |
| T8 saved output | outputs | outputs |
| T9 false assert | run | run |
| T10 a cell calls `pytest.skip()` | `4 passed, 1 skipped` | `5 passed, 1 skipped` |

No-draw configuration (`PACKAGE = "pkg"`, `DISPLAY_NEEDS = None`, matplotlib blocked): N1 dynamic import fails run; N2 comment plus `importlib` fails package alone; N3 guard on fails guard alone; N5 false assert fails run; N6 port test 3's tour fails charting and run; N4 `pytest.skip()` gives `5 passed, 1 skipped`.

**Does the module still refuse what it refused before?** Yes. Evidence: the table above. The subfolder glob (S1) and the guard forms from `97b3c42` are in code this diff does not touch.

**Is anything left that a no-draw repo must delete or edit?** No. The child repo in N0 sets three constant lines (`configure` asserts exactly one match each) and leaves the `finally` block and `import sys` in place; it passes with matplotlib blocked. Evidence: N0 → `outcomes={'passed': 6}`. One line still misleads such a repo without breaking it: Suggestion 3.

## Critical

None.

## Warnings

### W1. The port tests pass when the run test executes no cell

`tests/unit/test_notebook_module_port.py:44-49, 62-66`.

Test 1's name claims "every cell runs", but nothing in the file can fail if the run test executes nothing or swallows a raising cell. Test 1 checks that the run test passed, which an empty loop also achieves. Test 3 checks the charting test only. This is the first automated test of the module's run test, so its vacuity matters: today only hand-run mutants hold the run test.

Evidence (module mutants, run against the port test file in the scratch copy):

```
P1 run test iterates cells(path, "raw")     test 1 PASSED  test 2 PASSED  test 3 PASSED  strict 3 FAILED
P6 run test's except clause becomes `pass`  test 1 PASSED  test 2 PASSED  test 3 PASSED  strict 3 FAILED
P0 new module                               test 1 PASSED  test 2 PASSED  test 3 PASSED  strict 3 PASSED
```

Fix: in test 3, pin the exact failures, as test 2 does. In this repo the run test can fail on that tour only by executing the import cell, so the assert proves the cells ran and were not skipped:

```python
def test_a_charting_import_fails_the_charting_test_and_the_run_test_and_not_the_package_test(pytester):
    result = repo_that_draws_nothing(pytester, *TOUR[:2], "import matplotlib.pyplot as plt", *TOUR[2:])

    assert failed(result) == [
        "test_it_imports_no_charting_library",
        "test_every_code_cell_runs_in_order_over_the_committed_fixtures",
    ], result.stdout.str()
```

"strict 3" above is this assert. It passes on the new module and kills P1 and P6.

### W2. "The run test can never skip" is false: a cell can skip or xfail it, exit 0

`tests/unit/test_notebooks.py:12-13` (docstring) and `:126-129` (the cell loop).

The cell loop catches `Exception`. pytest's skip and xfail outcomes derive from `BaseException`, so a cell that calls `pytest.skip()` or `pytest.xfail()` ends the run test as skipped or xfailed, and the remaining cells never run. HEAD has the same escape (T10), so this diff did not open it. But the diff rewrites the sentence that rules it out, and port test 1 asserts it.

Evidence: N4 → `outcomes={'passed': 5, 'skipped': 1}`; xfail probe → `ret=0`, `5 passed, 1 xfailed`; `pytest.exit('done', returncode=0)` from a cell is already refused (`ret=1`, `1 failed, 5 passed`).

Fix, one line (verified in the scratch copy: the skip and xfail probes then fail the run test, `ret=1`; the port test and the hub module still pass, `12 passed` across those files and probes):

```python
            except (Exception, pytest.skip.Exception, pytest.xfail.Exception) as error:
```

The correction entry being written into `docs/doctrine-updates.md` during this review repeats the claim in its `MODULE_COMMIT` row: "and the run test then never skips". That entry is uncommitted and was not reviewed here.

Or, if the module should change no further in this correction, narrow the sentence: "A repo whose tour draws nothing sets DISPLAY_NEEDS = None, and then the run test never skips for want of a library." Then add the skip and xfail forms to the draft's "Known limit" line beside `globals()`. The one-line fix is cheaper overall: consumers re-copy the file once either way.

## Suggestions

### S1. The port test cites the delivered entry for a setting only the draft proposes

`tests/unit/test_notebook_module_port.py:3-5`. "with its constants set the way the doctrine entry tells a repo to set them". The delivered entry names `DISPLAY_HOME` and tells a no-draw repo to delete `DISPLAY_NEEDS` and two lines (`docs/doctrine-updates.md:67`). A reader who checks the entry finds the opposite instruction.

Rewrite: "with its three constants set for a repo whose tour draws nothing (`DISPLAY_NEEDS = None`)".

### S2. The helper's docstring misdescribes test 2's tour and hides that it runs pytest

`tests/unit/test_notebook_module_port.py:30-31`. "A repo with no charting library installed, whose tour imports `pkg`." Test 2's tour does not import `pkg`. The function also runs the child pytest and returns its result, which its noun name does not say. (The "no charting library" half holds: of `DRAWING_LIBRARIES`, the venv has only `matplotlib` and `pylab`, which ships with it.)

Rewrite: rename it `run_in_a_repo_that_draws_nothing` and use the docstring "Build a repo around a tour of these cells, configured to draw nothing and with matplotlib blocked; run the copied module in a child pytest and return the result."

### S3. The charting test's message keeps the misnomer the rename removed

`tests/unit/test_notebooks.py:85`. `f"{path.name} imports {drawing}: a figure comes from {PACKAGE}"`. In 12 of 13 repos `PACKAGE` draws nothing, so this sends the author looking for a figure function that does not exist. That is the same fault that retired `DISPLAY_HOME`.

Rewrite: `f"{path.name} imports {drawing}: a tour draws no chart of its own; any figure comes from {PACKAGE}"`.

### S4. Test 1's two checks can be one stronger line

`tests/unit/test_notebook_module_port.py:47-49`. `result.assert_outcomes(passed=6)` holds on the baseline (verified). It also requires zero failed, errors, skipped, xfailed and xpassed, so it covers the xfail form in W2. It pins the six-test count the correction entry will state. The `parseoutcomes` line and the `fnmatch_lines` line can then go.

### S5. `PATH_SETUP` carries no load in the port test

`tests/unit/test_notebook_module_port.py:14-15`. A tour without it passes the same (`outcomes={'passed': 6}`). `python -m pytest` and the root `conftest.py` already put the pytester directory on the child's `sys.path`. Drop it, or add a comment that it mirrors a real tour's first cell (row 2) and is not what makes `import pkg` resolve.

### S6. Two numbers in the correction draft go stale when this lands

`docs/plans/20261115_notebook_tour_correction_entry_draft.md:25, 78`. Item 1 says "five tests", and Step 1 says "one failure and four skips". After the split the module has six tests, and with no notebook it reports one failure and five skips. Evidence: baseline `6 passed`; empty `notebooks/` → `outcomes={'failed': 1, 'skipped': 5}`. Step 4's mutant counts still hold: a charting import fails two tests (T1), a false assert one (T9). The entry being written into `docs/doctrine-updates.md` already says `6 passed`.

## Claims checked

| Claim (the lead's) | Result |
|---|---|
| Full suite 578 passed, 3 skipped, with and without `CI=true` | VERIFIED: `578 passed, 3 skipped, 1 warning` both runs; `.venv/bin/python` is 3.12.13, pytest 9.1.1 |
| Each port test was seen failing for its own reason before the change | UNVERIFIABLE as history. Reconstructed: with HEAD plus the rename only (P4), all three fail. Test 1 fails on `TypeError: compile() arg 1 must be a string` from `importorskip(None)`. Test 2 fails on `['test_it_dra...ted_fixtures'] == ['test_it_imp..._the_package']`. Test 3 fails because the charting test name is absent. With the rename and the guard but no split (P5), tests 2 and 3 fail and test 1 passes |
| A `matplotlib` import and the package imports removed each failed the intended half plus the run test | VERIFIED: T1 → charting, run; T5 → package, run |
| A no-draw repo used to delete the constant, the `importorskip` line and the `MPLBACKEND` line | VERIFIED: `docs/doctrine-updates.md:67` |
| Twelve of thirteen tours draw nothing | Not re-checked: the tours live in thirteen other repos. Source: the session doc's Key Decisions table |

Committing this to `main` changes nothing for consumers: the delivered entry pins `8c3b69a` (`docs/doctrine-updates.md:67`). Sending it is the user's call: decisions 2 and 3 in the draft.

## What this review did not do

- It did not run any other repo's tests or read the thirteen built tours.
- It did not check formatting at 88 columns (draft item 4, not in this change). No lint config exists in `pyproject.toml`.
- pytester's temporary directories under `/tmp/pytest-of-<user>` are pytest's own (it keeps the last three runs) and predate this review; they were left in place.
