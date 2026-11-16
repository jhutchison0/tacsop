"""Every notebook under notebooks/ is committed without outputs, draws no chart of its own, and runs over the fixtures.

A notebook is an example of how the repo works, so it is held the way any other example
is: the suite executes every code cell in order, in one namespace, with the working
directory at `notebooks/` as a kernel would have it. Jupyter is not needed for that: an
`.ipynb` is JSON, and a tour's cells are plain Python whose own `assert` lines are its
checks. A saved output fails here because the last section of a tour can point at the
reader's own data, and an output committed from it would publish that data.

To carry this module to another repo, set the three constants below DRAWING_LIBRARIES,
and NOTEBOOK_DIR's count of `.parent` if this file does not sit two folders below the root.
Delete nothing. A repo whose tour draws nothing sets DISPLAY_NEEDS = None, and then the
module never skips the run test; a cell that calls pytest.skip or pytest.xfail fails it.
"""

import ast
import json
import sys
import types
from pathlib import Path

import pytest

NOTEBOOK_DIR = Path(__file__).resolve().parent.parent.parent / "notebooks"
NOTEBOOKS = sorted(p for p in NOTEBOOK_DIR.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)
DRAWING_LIBRARIES = ("matplotlib", "pylab", "plotly", "seaborn", "altair", "bokeh", "plotnine", "holoviews", "hvplot", "pygal")
PACKAGE = "src.myproject.decision_science"  # the package the tour walks, as its cells import it; any figure comes from it
DISPLAY_NEEDS = "matplotlib"  # the optional dependency PACKAGE draws with; None where the tour draws nothing
OWN_DATA_GUARDS = ("MY_MODEL", "MY_ALTERNATIVES")  # the names the own-data cell sets, each committed as None


def cells(path: Path, kind: str) -> list[dict]:
    return [cell for cell in json.loads(path.read_text(encoding="utf-8"))["cells"] if cell["cell_type"] == kind]


def source(cell: dict) -> str:
    return "".join(cell["source"])


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


def test_there_is_a_notebook_to_hold():
    assert NOTEBOOKS, f"no notebook under {NOTEBOOK_DIR}: the checks below would pass over nothing"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_it_is_committed_without_outputs(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    assert "widgets" not in notebook["metadata"], f"{path.name} carries saved widget state"
    for cell in notebook["cells"]:
        assert not cell.get("attachments"), f"{path.name} carries an attachment: a pasted image is a saved output"
    for number, cell in enumerate(cells(path, "code")):
        assert cell["outputs"] == [] and cell["execution_count"] is None, (
            f"{path.name} code cell {number} carries a saved output: clear all outputs before staging"
        )


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_it_imports_the_package(path):
    names = imported(path)
    assert any(name == PACKAGE or name.startswith(PACKAGE + ".") for name in names), (
        f"{path.name} imports nothing from {PACKAGE}"
    )


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_it_imports_no_charting_library(path):
    drawing = sorted(name for name in imported(path) if name.split(".")[0] in DRAWING_LIBRARIES)
    assert not drawing, f"{path.name} imports {drawing}: the notebook draws nothing itself; any figure comes from {PACKAGE}"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_the_own_data_cell_is_committed_switched_off(path):
    """A guard committed with a path makes the suite read the reader's data on every run."""
    values: dict[str, list[ast.expr]] = {}
    for cell in cells(path, "code"):
        try:
            tree = ast.parse(source(cell))
        except SyntaxError:
            continue  # the run test reports a cell that is not plain Python
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                pairs = [(target, node.value) for target in node.targets]
            elif isinstance(node, (ast.AnnAssign, ast.NamedExpr, ast.AugAssign)) and node.value is not None:
                pairs = [(node.target, node if isinstance(node, ast.AugAssign) else node.value)]
            else:
                continue
            for target, value in pairs:
                if isinstance(target, ast.Name) and target.id in OWN_DATA_GUARDS:
                    values.setdefault(target.id, []).append(value)
                for name in ast.walk(target):  # a guard set inside a tuple or list target is never plainly None
                    if name is not target and isinstance(name, ast.Name) and name.id in OWN_DATA_GUARDS:
                        values.setdefault(name.id, []).append(node)
    for name in OWN_DATA_GUARDS:
        assert name in values, f"{path.name} never sets {name}: name the own-data guards in OWN_DATA_GUARDS"
        for value in values[name]:
            assert isinstance(value, ast.Constant) and value.value is None, f"{path.name} commits {name} switched on"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_every_code_cell_runs_in_order_over_the_committed_fixtures(path, monkeypatch):
    if DISPLAY_NEEDS:
        pytest.importorskip(DISPLAY_NEEDS)  # a skip here means no cell ran: keep it installed where the suite runs
        monkeypatch.setenv("MPLBACKEND", "Agg")  # no window, if a cell is the first to import matplotlib
    monkeypatch.chdir(NOTEBOOK_DIR)
    monkeypatch.syspath_prepend(str(NOTEBOOK_DIR))  # restores sys.path after the cells insert the repo root
    namespace: dict = {"__name__": "__main__"}
    try:
        for number, cell in enumerate(cells(path, "code")):
            try:
                exec(compile(source(cell), f"{path.name}[cell {number}]", "exec"), namespace)
            except (Exception, pytest.skip.Exception, pytest.xfail.Exception) as error:  # a cell may not skip itself
                pytest.fail(f"{path.name} code cell {number} raised {type(error).__name__}: {error}")
        held = {v.__name__.split(".")[0] for v in namespace.values() if isinstance(v, types.ModuleType)}
        assert not held & set(DRAWING_LIBRARIES), f"{path.name} holds {sorted(held & set(DRAWING_LIBRARIES))} by a dynamic import"
    finally:
        pyplot = sys.modules.get("matplotlib.pyplot")
        if pyplot is not None:
            pyplot.close("all")
