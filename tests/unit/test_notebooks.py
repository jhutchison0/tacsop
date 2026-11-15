"""Every notebook under notebooks/ is committed without outputs, draws no chart of its own, and runs over the fixtures.

A notebook is an example of how the repo works, so it is held the way any other example
is: the suite executes every code cell in order, in one namespace, with the working
directory at `notebooks/` as a kernel would have it. Jupyter is not needed for that: an
`.ipynb` is JSON, and a tour's cells are plain Python whose own `assert` lines are its
checks. A saved output fails here because the last section of a tour can point at the
reader's own data, and an output committed from it would publish that data.

To carry this module to another repo, change the two constants below DRAWING_LIBRARIES.
"""

import json
import re
import sys
from pathlib import Path

import pytest

NOTEBOOK_DIR = Path(__file__).resolve().parent.parent.parent / "notebooks"
NOTEBOOKS = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
DRAWING_LIBRARIES = ("matplotlib", "plotly", "seaborn", "altair", "bokeh")
DISPLAY_HOME = "src.myproject.decision_science"  # the one package a notebook's figures come from
DISPLAY_NEEDS = "matplotlib"  # the optional dependency the display home draws with


def cells(path: Path, kind: str) -> list[dict]:
    return [cell for cell in json.loads(path.read_text(encoding="utf-8"))["cells"] if cell["cell_type"] == kind]


def source(cell: dict) -> str:
    return "".join(cell["source"])


def test_there_is_a_notebook_to_hold():
    assert NOTEBOOKS, f"no notebook under {NOTEBOOK_DIR}: the checks below would pass over nothing"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_it_is_committed_without_outputs(path):
    assert json.loads(path.read_text(encoding="utf-8"))["nbformat"] == 4
    for number, cell in enumerate(cells(path, "code")):
        assert cell["outputs"] == [] and cell["execution_count"] is None, (
            f"{path.name} code cell {number} carries a saved output: clear all outputs before staging"
        )


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_it_draws_nothing_of_its_own_and_shows_a_display_from_the_display_home(path):
    code = "\n".join(source(cell) for cell in cells(path, "code"))
    for library in DRAWING_LIBRARIES:
        assert not re.search(rf"^\s*(import|from)\s+{library}\b", code, re.MULTILINE), (path.name, library)
    assert DISPLAY_HOME in code, f"{path.name} shows no display from {DISPLAY_HOME}"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_every_code_cell_runs_in_order_over_the_committed_fixtures(path, monkeypatch):
    pytest.importorskip(DISPLAY_NEEDS)
    monkeypatch.chdir(NOTEBOOK_DIR)
    monkeypatch.syspath_prepend(str(NOTEBOOK_DIR))  # restores sys.path after the cells insert the repo root
    namespace: dict = {"__name__": "__main__"}
    try:
        for number, cell in enumerate(cells(path, "code")):
            try:
                exec(compile(source(cell), f"{path.name}[cell {number}]", "exec"), namespace)
            except Exception as error:
                pytest.fail(f"{path.name} code cell {number} raised {type(error).__name__}: {error}")
    finally:
        pyplot = sys.modules.get("matplotlib.pyplot")
        if pyplot is not None:
            pyplot.close("all")
