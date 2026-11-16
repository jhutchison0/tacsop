"""test_notebooks.py ports to another repo by setting its constants; nothing in it is deleted.

Each test builds a small repo with pytester: a package, one tour, and a copy of the hub's
test_notebooks.py with its constants set the way the 2026-11-16 correction entry tells a
repo to set them. It then runs pytest on that copy in a child process, so the child's
missing charting library cannot leak into this suite.
"""

import json
import re
from pathlib import Path

import pytest

HUB_MODULE = Path(__file__).with_name("test_notebooks.py")
RUN_TEST = "test_every_code_cell_runs_in_order_over_the_committed_fixtures"
TOUR = ("import pkg", 'assert pkg.greet() == "hi"', "MY_DATA = None")


def configure(text: str, **constants: str) -> str:
    for name, value in constants.items():
        text, count = re.subn(rf"^{name} = .*$", f"{name} = {value}", text, flags=re.MULTILINE)
        assert count == 1, f"test_notebooks.py has no single {name} line to set"
    return text


def notebook(*sources: str) -> str:
    code = [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s} for s in sources]
    return json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": code})


def run_in_a_repo_that_draws_nothing(pytester, *sources: str):
    """Run the configured module over a tour of these cells, in a repo with package `pkg`
    and no charting library installed, and return pytest's result."""
    root = pytester.path
    (root / "pkg").mkdir()
    (root / "pkg" / "__init__.py").write_text('def greet():\n    return "hi"\n')
    (root / "notebooks").mkdir()
    (root / "notebooks" / "tour.ipynb").write_text(notebook(*sources))
    (root / "tests" / "unit").mkdir(parents=True)
    module = configure(HUB_MODULE.read_text(), PACKAGE='"pkg"', DISPLAY_NEEDS="None", OWN_DATA_GUARDS='("MY_DATA",)')
    (root / "tests" / "unit" / "test_notebooks.py").write_text(module)
    (root / "conftest.py").write_text('import sys\n\nsys.modules["matplotlib"] = None  # not installed here\n')
    return pytester.runpytest_subprocess("-rA", "tests/unit/test_notebooks.py")


def failed(result) -> list[str]:
    return re.findall(r"^FAILED tests/unit/test_notebooks\.py::(\w+)", result.stdout.str(), flags=re.MULTILINE)


def test_a_repo_that_draws_nothing_sets_its_constants_and_every_test_passes(pytester):
    run_in_a_repo_that_draws_nothing(pytester, *TOUR).assert_outcomes(passed=6)


def test_a_tour_that_never_imports_the_package_fails_the_package_test_alone(pytester):
    result = run_in_a_repo_that_draws_nothing(pytester, "total = 1 + 1", "assert total == 2", "MY_DATA = None")

    assert failed(result) == ["test_it_imports_the_package"], result.stdout.str()


@pytest.mark.parametrize("escape", ["pytest.skip('mutant')", "pytest.xfail('mutant')"])
def test_a_cell_that_tries_to_skip_fails_the_run_test(pytester, escape):
    result = run_in_a_repo_that_draws_nothing(pytester, *TOUR, f"import pytest\n{escape}")

    assert failed(result) == [RUN_TEST], result.stdout.str()


def test_a_charting_import_fails_the_charting_test_and_the_run_test(pytester):
    result = run_in_a_repo_that_draws_nothing(pytester, TOUR[0], "import matplotlib.pyplot as plt", *TOUR[1:])

    assert failed(result) == ["test_it_imports_no_charting_library", RUN_TEST], result.stdout.str()
