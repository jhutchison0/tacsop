# Review: Notebook Tour Entry, Pre-flight

**Author**: code-reviewer
**Date**: 2026-11-14
**Type**: Code review (doctrine entry, proposal, and the test module the entry ships)

**Verdict: GO-WITH-FIXES.** Do not run the live cycle until Critical 1 and 2 and Warnings 1 to 6 are applied. The four claimed mutants reproduce, but 19 of 30 further mutants pass the module at `a7ab4ca`, and the entry's Rollback deletes notebooks it did not create.

Reviewed: `docs/plans/20261114_notebook_tour_proposal.md` (untracked), the 2026-11-14 entry in `docs/doctrine-updates.md` (lines 7 to 78, uncommitted), and `a7ab4ca` (`tests/unit/test_notebooks.py`, the notebook, two fixtures, the `notebook` extra, the README section).

## What was run

| Check | Result |
|---|---|
| `.venv/bin/pytest -q tests/unit/test_notebooks.py` | `4 passed in 0.50s` |
| `.venv/bin/pytest -q` | `575 passed, 1 warning in 5.88s` |
| `.venv/bin/python scripts/propagate_doctrine.py --dry-run` | 23 repos, 1 entry each (2026-11-14), `github/assay` skipped, no `[warn]` line |
| Entry Detect, command 1 | prints `notebooks/tour_from_a_model_to_a_ranking.ipynb` and `tests/unit/test_notebooks.py` |
| Entry Detect, command 2 | prints nothing, exit 0 |
| `git branch -r --contains a7ab4ca` | prints nothing; `git status -sb` says `main...origin/main [ahead 2]` |
| Private-terms list against the entry, proposal, notebook, test module, fixtures | 0 hit lines in each of 6 files |
| Em dash and en dash search, entry and proposal | 0 matches |
| Military-term search in the entry (protocol's seven terms) | 0 matches |
| `git status --porcelain` after the battery | unchanged: the two modified docs and the untracked proposal |

The mutant battery ran in a `tar` copy of the repo in the session scratchpad (no `.venv`, no `.git`), with the notebook rebuilt from the working tree's copy before each mutant and the baseline scored first (`4 passed`). The working tree's notebook was never written.

Downstream shape, counted read-only across the 23 repos in the dry run: 18 have a `pyproject.toml`; 10 use a true src layout (`where = ["src"]`), 4 use the hub's `include = ["src*"]`; 17 have `tests/unit/`; 3 name matplotlib in `pyproject.toml`; 6 have an `all` extra; 4 have `tests/isolation.py`; 1 tracks a notebook and 1 holds untracked notebooks; none has a `notebooks/` directory or a `topic/notebook-tour` branch yet.

## Evaluation Gate (propagation-protocol.md)

| # | Question | Result |
|---|---|---|
| 1 | What is the change? | PASS. The first paragraph says it in two sentences. |
| 2 | Why is it doctrine? | PASS. Cross-cutting and convention-bearing. The entry says it is optional and rests on two repos and one author; the proposal's four user decisions are still open. |
| 3 | Who is the audience? | PASS, with Suggestion 3. Five of the 23 targets have no `pyproject.toml`. |
| 4 | What action does the maintainer take? | FAIL until Critical 1 and Warnings 3, 4, 5 are fixed. The copy source is unreachable off this machine, and three steps assume the hub's layout. |
| 5 | What is the rollback path? | FAIL until Critical 2 is fixed. |

Batching: Rule 1 PASS (one coherent practice). Rule 2 PASS with a note: row 6 is coupled to row 1 by the module's glob, so a maintainer cannot take the tour and leave existing notebooks alone without editing the module; say so in row 6 (Warning 5). Rule 3 not applicable. Rule 4 PASS: additive, nothing renamed or removed.

Authoring tone: steps are numbered and lead with verbs; no first-person plural; no session context. Two misses: step 2 names no path, and the steps assume `tests/unit/`, a flat layout, and uv.

## Mutants

Against the module at `a7ab4ca`. KILLED means pytest exited non-zero.

| Mutant | Result | Failing test |
|---|---|---|
| C1 saved output (claimed) | KILLED | outputs |
| C2 false assertion (claimed) | KILLED | run |
| C3 `import matplotlib` (claimed) | KILLED | draws |
| C4 raising cell (claimed) | KILLED | run |
| E1 `__import__('matplotlib.pyplot')`, then its own plot | **SURVIVED** | |
| E2 `importlib.import_module('matplotlib.pyplot')` | **SURVIVED** | |
| E3 `import os, matplotlib.pyplot as plt` | **SURVIVED** | |
| E4 `x = 1; import matplotlib.pyplot as plt` | **SURVIVED** | |
| E5 import inside a function body | KILLED | draws |
| E6 drawing on the figure the package returned (`radar.add_axes(...).bar(...)`) | **SURVIVED** | |
| E7 `from pylab import plot` | **SURVIVED** | |
| E8 `if True: import matplotlib.pyplot as plt` | **SURVIVED** | |
| E9 a one-cell notebook: `# src.myproject.decision_science` and `pass` | **SURVIVED** | |
| E11 `exec('import matplotlib.pyplot as plt')` | **SURVIVED** | |
| O1 `execution_count` set, outputs empty | KILLED | outputs |
| O2 image attachment on a markdown cell | **SURVIVED** | |
| O3 widget state in notebook metadata | **SURVIVED** | |
| O4 raw cell holding pasted rows | **SURVIVED** | |
| O5 result table pasted into a markdown cell | **SURVIVED** | |
| R1 `%matplotlib inline` | KILLED (SyntaxError) | run |
| R2 top-level `await` | KILLED (SyntaxError) | run |
| R3 `display(results)` | KILLED (NameError) | run |
| R4 `!ls` | KILLED (SyntaxError) | run |
| R5 `sys.exit(0)` before a false assert | KILLED | run |
| R6 false assert inside `try/except Exception: pass` | **SURVIVED** | |
| R7 a socket connect in a cell | KILLED at the hub by `tests/isolation.py`; **SURVIVED** with `-o addopts=` (`4 passed`) | |
| R8 a cell reads `ANTHROPIC_API_KEY` from the environment | **SURVIVED** | |
| R9 every `assert` line deleted | **SURVIVED** | |
| R10 own-data guard switched on, paths outside `notebooks/` | **SURVIVED** | |
| R11 a cell sets `os.environ` and leaks it to later tests | **SURVIVED** | |
| S1 a notebook with outputs, a matplotlib import and a raising cell in `notebooks/drafts/` | **SURVIVED** (never collected) | |
| S2 the same notebook at the repo root | **SURVIVED** (never collected) | |
| S3 the same notebook in `notebooks/` (control) | KILLED | all three |
| S4 `notebooks/` emptied (control) | KILLED: `1 failed, 3 skipped` | there-is-a-notebook |
| matplotlib absent, clean notebook | `3 passed, 1 skipped`, exit 0 | |
| matplotlib absent, raising cell (C4) | **SURVIVED**: `3 passed, 1 skipped`, exit 0 | |

Two false alarms, the other direction: `from src.myproject import decision_science` with no dotted form fails the draws test, and a printed string with a line that starts `import matplotlib` fails it too.

With the patch in Warning 1 applied to the scratch copy, the baseline still passes and E1, E2, E3, E4, E7, E8, E9, E11, O2, O3 and S1 are killed; both false alarms pass. E6, O4, O5, R6, R8, R9, R10, R11, S2 and the two matplotlib-absent cases still survive; those are for review or for the entry's wording.

## Critical

### C1. The entry's sources are not reachable off this machine
`docs/doctrine-updates.md:58` (row 1), `:20` (the proposal pointer).

Row 1 says "Copy it from the hub at `a7ab4ca`". `a7ab4ca` is on no remote branch (`main` is ahead of `origin/main` by 2), the proposal the entry cites is untracked, and the entry itself is uncommitted. A consumer on the work terminal, or anyone reading the public repo, cannot fetch the module the whole entry rests on. The row also gives no command.

Fix, in order:
1. Apply the fixes below, commit the module change, the proposal and the entry, and push `main` before the live run.
2. Replace the first sentence of row 1 with the command and the final commit (`<sha>` is the commit that holds the fixed module, not `a7ab4ca`, if Warning 1 is applied):

   > Copy it from the hub at `<sha>`: `git -C <hub-path> show <sha>:tests/unit/test_notebooks.py > tests/unit/test_notebooks.py`, or fetch `https://raw.githubusercontent.com/jhutchison0/tacsop/<sha>/tests/unit/test_notebooks.py`.

### C2. Rollback deletes notebooks the entry did not create
`docs/doctrine-updates.md:75-76`.

"Delete `notebooks/`" is safe only where the tour is the only notebook. Row 6 addresses repos that already have notebooks, and an agent following Rollback there deletes all of them. Untracked notebooks are not in git and do not come back. One downstream repo holds untracked notebooks today. Row 6 also clears outputs and moves files, and Rollback does not reverse either.

Fix. Replace the Rollback body with:

> Delete the tour notebook (`notebooks/tour_*.ipynb`), the test module you copied, and the tour's fixtures; remove the `notebook` extra and the README section. Delete `notebooks/` only if the tour created it. If you did row 6, revert that commit (`git revert <commit>`) to bring back the outputs and the old paths. Nothing else depends on these files.

And add to row 6: "Commit row 6 on its own, so it can be reverted alone. Do not clear the outputs of a notebook that is not tracked by git until you have a copy; the outputs may be the only record of the run."

## Warnings

### W1. Rule 3 is satisfied by a comment and evaded by seven one-line imports
`tests/unit/test_notebooks.py:21-22, 50-53`.

Line 53 checks that the string `DISPLAY_HOME` appears anywhere in the code, so a comment satisfies "imports the repo's package" (E9). In a src-layout repo `DISPLAY_HOME` is a bare name such as `urd`, which any longer word containing it also satisfies. Line 52 matches `import` only at the start of a line, so E3, E4 and E8 pass, as do the dynamic forms E1, E2, E11 and the unlisted `pylab` (E7). The same regex raises two false alarms. Line 21's `glob` is not recursive, so a notebook in a subfolder of `notebooks/` is held by nothing (S1). Consumers copy this file tonight; a fix after the run needs a correction entry to 23 repos.

Fix: read imports from the syntax tree, check module objects left in the namespace after the run, and glob recursively. The tested patch is at `/tmp/claude-1000/-home-jhutchison-projects-github-tacsop/067af0da-f5e1-47af-859e-e596d79ba31d/scratchpad/test_notebooks_recommended.diff`. Its parts:

```python
import ast
import types

NOTEBOOKS = sorted(p for p in NOTEBOOK_DIR.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)
DRAWING_LIBRARIES = ("matplotlib", "pylab", "plotly", "seaborn", "altair", "bokeh", "plotnine", "holoviews", "hvplot", "pygal")


def imported(path: Path) -> set[str]:
    """Every dotted name a code cell imports, read from the syntax tree, not the text."""
    names: set[str] = set()
    for cell in cells(path, "code"):
        try:
            tree = ast.parse(source(cell))
        except SyntaxError:
            continue  # the run test reports a cell that is not plain Python
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
                names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names
```

In the draws test, replace the body with:

```python
    names = imported(path)
    drawing = sorted(name for name in names if name.split(".")[0] in DRAWING_LIBRARIES)
    assert not drawing, f"{path.name} imports {drawing}: a figure comes from {DISPLAY_HOME}"
    assert any(name == DISPLAY_HOME or name.startswith(DISPLAY_HOME + ".") for name in names), (
        f"{path.name} imports nothing from {DISPLAY_HOME}"
    )
```

In the run test, after the `for` loop and inside the outer `try`:

```python
        held = {v.__name__.split(".")[0] for v in namespace.values() if isinstance(v, types.ModuleType)}
        assert not held & set(DRAWING_LIBRARIES), f"{path.name} holds {sorted(held & set(DRAWING_LIBRARIES))} by a dynamic import"
```

Drive each part with its mutant first (E9, E3, E1, S1), per the repo's shift-left rule. After the patch a plain `import matplotlib` fails two tests, so "each failed exactly one test" in the entry and the proposal becomes "each failed". E6 (drawing on a returned figure) stays with review; say so in rule 3's "Held by" cell.

### W2. Rule 2 misses attachments and widget state
`tests/unit/test_notebooks.py:40-45`.

The test reads `outputs` and `execution_count` on code cells only. A pasted image lives in a markdown cell's `attachments`, and widget output lives in `metadata.widgets`; both publish data and both pass (O2, O3).

Fix, in the outputs test (in the patch file above):

```python
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    assert "widgets" not in notebook["metadata"], f"{path.name} carries saved widget state"
    for cell in notebook["cells"]:
        assert not cell.get("attachments"), f"{path.name} carries an attachment: a pasted image is a saved output"
```

Text pasted into a markdown or raw cell (O4, O5) cannot be told from prose; add it to rule 6's review line.

### W3. A missing optional dependency skips rule 1 and the suite stays green
`tests/unit/test_notebooks.py:58`; `docs/doctrine-updates.md:9-11, 69`; proposal line 12.

With matplotlib absent, a notebook whose cell raises gives `3 passed, 1 skipped`, exit 0. The hub's documented setup installs `.[dev]`, which has no matplotlib, so a fresh hub checkout does not run the tour. "The test suite runs every cell of that notebook, so it cannot drift" holds only where `DISPLAY_NEEDS` is installed. Only 3 of 18 downstream `pyproject.toml` files name matplotlib.

Fix, entry step 3: "Write the tour until the module reports `4 passed` and no `skipped`. A skip means no cell ran: install the `DISPLAY_NEEDS` dependency in the environment the suite runs in (your `dev` extra or your CI install line)." Add to row 1: "Most repos draw nothing: then delete the `pytest.importorskip(DISPLAY_NEEDS)` line and the constant, and the run test can never skip." At the hub, add `matplotlib>=3.5` to `dev` or state the skip in the README section.

### W4. Rule 1 claims more than the module holds
`docs/doctrine-updates.md:35`; proposal line 30.

"No network, no secrets" is listed as held by the test module. The module has no such check: a socket connect passes with the hub's isolation plugin off, and a cell reading an API key passes anywhere. At the hub `tests/isolation.py` holds the network half; 4 of 23 downstream repos have that file. "Over committed fixtures" is not held either: the guard switched on and pointed outside `notebooks/` passes (R10), and the module reads the disk, not the index.

Fix: split the row in both tables.

> | 1 | The suite runs every code cell, in order, in one namespace, with the working directory at `notebooks/`. No kernel. | the test module |
> | 1a | The cells read only committed fixtures. No network, no secrets. | review (and the isolation tripwire, in a repo that has `tests/isolation.py`) |

Update "The first three are held by one test module" in the proposal (line 26) to match.

### W5. Three hub-specific assumptions in the steps
`docs/doctrine-updates.md:58-59, 63, 67`.

1. **Src layout (10 of 23 repos).** Row 2 tells every repo to write "an opening cell that puts the repo root on `sys.path`". In a true src layout the root holds no importable package; the package is installed in the venv, or lives under `src/`. Rewrite: "an opening cell that names the fixtures and, only if the package is not installed in the venv, puts its parent directory on `sys.path` (the repo root at the hub, where the import is `src.myproject`; `ROOT / "src"` in a src layout)". In row 1 add: "`DISPLAY_HOME` is the dotted name as the notebook imports it: `pkg` or `pkg.report`, not `src.pkg`, in a src layout."
2. **Plain Python only.** The module runs cells with `exec`, so `%` magics, `!` commands, top-level `await` and `display()` each fail the run test (R1 to R4). The module's docstring says so; the entry does not. Add to rows 2 and 6: "Cells must be plain Python: no `%` magics, no `!` commands, no top-level `await`, no `display()`; use `print`."
3. **Step 1's red.** In a repo that already has notebooks, `test_there_is_a_notebook_to_hold` passes at step 1 and the other three fail on the old notebooks. Rewrite step 1: "Copy the test module (row 1), set its constants, and run it. With no notebook yet, see `test_there_is_a_notebook_to_hold` fail and three tests skip. With existing notebooks, see them fail and do row 6 first."

Row 6 gives no way to clear outputs, and the `notebook` extra carries no `nbconvert`. Add a command that needs nothing installed:

```bash
python3 -c "
import json, sys
for f in sys.argv[1:]:
    nb = json.load(open(f, encoding='utf-8'))
    for c in nb['cells']:
        if c['cell_type'] == 'code': c['outputs'], c['execution_count'] = [], None
    json.dump(nb, open(f, 'w', encoding='utf-8'), indent=1); print('cleared', f)" notebooks/<name>.ipynb
```

Row 6 also sends unrunnable notebooks out of `notebooks/`, where nothing checks their outputs (S2). Add: "A notebook moved out keeps its outputs in git: clear them, or keep the file untracked."

### W6. Step 4 mutates the only copy of the tour
`docs/doctrine-updates.md:70`.

Step 3 says to clear outputs "before staging", so at step 4 the notebook is neither staged nor committed, and "then restore the file" has nothing to restore from. An agent that saves a mutant over the tour and cannot undo it ships the mutant or loses the tour. The step also skips rule 3.

Fix: "4. Stage the notebook (`git add notebooks/<tour>.ipynb`). Break the working copy three times, one at a time: save an output, falsify one assert, add `import matplotlib`. Confirm each fails, and run `git restore notebooks/<tour>.ipynb` after each. Finish with `git diff --quiet notebooks/` and a passing run."

### W7. Detect breaks on a notebook name with a space and misses a stale `execution_count`
`docs/doctrine-updates.md:45-50`.

`for f in $(git ls-files '*.ipynb')` splits `Untitled 1.ipynb` into two paths and prints tracebacks. `c.get('outputs')` passes a cell with `execution_count` set, which the module refuses (O1), so Detect and the test disagree. The first command prints file names and leaves the reader to infer what "the suite does not run" means; it prints nothing for a module placed outside `tests/unit/`.

Fix (run at the hub: prints nothing, exit 0):

```bash
# Every tracked notebook, then the test module that holds notebooks/ (no second line: nothing holds them):
git ls-files '*.ipynb'; git ls-files '*test_notebooks.py'
# Tracked notebooks with saved outputs or execution counts (prints each):
git ls-files -z '*.ipynb' | python3 -c "
import json, sys
for f in filter(None, sys.stdin.read().split('\0')):
    nb = json.load(open(f, encoding='utf-8'))
    if any(c.get('outputs') or c.get('execution_count') for c in nb.get('cells', []) if c['cell_type'] == 'code'): print(f)"
# A first tour already built for you (prints the branch if it exists):
git branch --list topic/notebook-tour
```

### W8. Claims without an `Evidence:` line, and three the re-run does not support
Proposal lines 6, 16, 40, 60-63; entry lines 14-19; commit `a7ab4ca`.

None of these carries `Evidence:` or `UNVERIFIED:`.

| Claim | Re-run |
|---|---|
| Four mutants each failed exactly one test (proposal 60, entry 17-18, commit) | VERIFIED: C1 to C4 above, `1 failed, 3 passed` each |
| "The test module is 70 lines" (proposal 40) | REFUTED: `wc -l` prints 71 |
| "ports by changing two constants" (proposal 40; module docstring line 10) | REFUTED by the entry's own row 1, which also changes `NOTEBOOK_DIR` and deletes the `importorskip` line |
| "the test suite should run that notebook on every run" / "cannot drift" (proposal 12, entry 10-11) | REFUTED where `DISPLAY_NEEDS` is absent: `3 passed, 1 skipped` (W3) |
| `exponential()` crash and silent wrong answer, `acdab6e` (proposal 61, entry 16-17) | VERIFIED as written: the commit exists and its body states both faults |
| "All three hub figures come from the package" (proposal 63) | VERIFIED: the notebook calls `radar_chart`, `tornado_plot`, `rank_stability_heatmap` and the draws test passes |
| The March gap analysis proposed `direction: minimize` (proposal 62) | VERIFIED as present: `docs/plans/decision_science_gaps.md` holds the string |
| First render showed `radar_chart` text was wrong (proposal 61) | UNVERIFIABLE: the first render was not kept |
| "Written first and seen red" (commit `a7ab4ca`) | UNVERIFIABLE: no red run is recorded |
| "The AI CoP lanes showed that a notebook with a hands-on section teaches faster than either" (proposal 16) | UNVERIFIABLE: no measurement is cited |

Fix: put an `Evidence:` line under the mutant claim (the four `1 failed, 3 passed` lines), correct 70 to the real count after the patch, change "two constants" to "two constants and, where tests are not in `tests/unit/`, one path", and rewrite the lane sentence as what was seen: "Lane 01 of the AI CoP used a notebook with a hands-on section; no comparison was measured."

## Suggestions

1. **`plt.show()` can hang the suite.** `tests/unit/test_notebooks.py:57-59`. A consumer's display function that calls `plt.show()` blocks under a GUI backend on a desktop. Add `monkeypatch.setenv("MPLBACKEND", "Agg")` before the loop, and to row 2: "a display function returns its figure and never calls `show()`".
2. **Cells leak state into the suite.** A cell that sets `os.environ`, a random seed, or logging config changes later tests (R11). Add to row 2: "cells set no environment variables and no global state".
3. **Audience.** `docs/doctrine-updates.md:23-24`. Rewrite the second sentence: "A repo with no importable Python package (documents, CAD, configuration) has nothing to tour; delete this notice."
4. **Row 4.** Six of 18 downstream `pyproject.toml` files have an `all` extra. Write: "Do not add it to `all`, if you have one. A repo with no `pyproject.toml` lists `ipykernel` wherever it lists optional tools."
5. **Rule 7 and the README row.** `ipykernel` alone opens the notebook in an editor that hosts kernels (VS Code); it does not install Jupyter. Say which in row 5.
6. **The suite goes red when the tour is used.** Running the tour in Jupyter saves outputs to disk, and the module reads the disk, so the reader's next `pytest` fails until outputs are cleared. The notebook's section 8 says so; the README section and row 5 should too.
7. **Action step paths.** Step 2 names no path; write "under `tests/fixtures/tour/` (or your fixture directory)". Rollback and step 1 name `tests/unit/test_notebooks.py` while row 1 allows another place.
8. **`docs/tasks.md` line 26.** The P3 "Evaluate the notebook tour as doctrine" still says the hub has no notebooks, cites three rules and 60 lines, and asks whether this is doctrine. The entry answers it. Close it or rewrite it to point at the proposal's four decisions.
9. **Proposal status.** [Minor] Rule 2 (Claim Style): "Status: Proposed" sits beside "directed a first rollout the same night". Rewrite: "Status: Proposed; rollout directed by the user on 2026-11-14, four decisions open (below)."
10. **Prose.** Both documents state their point first and carry no em dash and no banned word. One packed sentence, entry lines 14-16 ("The practice came from ... and three figures."): split at the colon into two sentences.

## Gaps in this review

- No consumer repo was built end to end from the entry; the src-layout and no-matplotlib findings come from reading the module and counting downstream layouts, not from a trial adoption.
- The battery ran on Python in the hub's `.venv` only, on this machine.
- `ipykernel` was not installed and the notebook was not opened in a kernel; the working directory a kernel gives it was not observed.
