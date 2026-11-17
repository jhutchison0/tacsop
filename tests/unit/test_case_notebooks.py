"""Every case notebook states each case in full and asserts its naive answer against the repo's.

Module version 0.7.2, 2026-11-16. Say this version when you report a copy; the hub's file changes.

A tour walks the main path once. A case notebook stops where the obvious rule gives a
different answer and runs that rule beside the repo's. This module holds what makes a case
a case; `test_notebooks.py` holds what every notebook owes (no saved output, the package
imported, no chart drawn in a cell, every cell run). Copy this module only into a repo
that has a case notebook, and copy `test_notebooks.py` with it.

To carry it to another repo, set NOTEBOOK_DIR to the folder the notebooks are in and TESTS_DIR
to the folder every test a source may name is under. The headings and labels below are the house's; a repo that
changes one changes it here and in `.claude/skills/writing-tours-and-case-notebooks/CASES.md`.
"""

import ast
import builtins
import contextlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

NOTEBOOK_DIR = Path(__file__).resolve().parent.parent.parent / "notebooks"
CASE_NOTEBOOKS = sorted(p for p in NOTEBOOK_DIR.rglob("cases_*.ipynb") if ".ipynb_checkpoints" not in p.parts)
CASE_PARTS = ("**Question.**", "**Fixture.**", "**Naive.**", "**The repo's rule.**", "**Source.**")
LIMIT_PARTS = ("**Question.**", "**What is not known.**", "**What would settle it.**")
SHAPES = {"## Case": CASE_PARTS, "## Limit": LIMIT_PARTS}  # a section heading, and the labels its text carries
HOW_SURE = r"## (Confidence|How sure)\b"  # the section rule 9 asks for; a repo that reserves "confidence" uses the second
OTHER_HEADINGS = r"## (\d+\. |Confidence\b|How sure\b|Your own |Where next)"  # a numbered section, the confidence section, the own-data cell, the closing links
ROOT = NOTEBOOK_DIR.parent
TESTS_DIR = Path(__file__).resolve().parent.parent  # where a test a source names is defined
PATH = r"[\w.-]+(?:/[\w.-]+)+"  # a backticked token with a slash in it is a path from the repo root
COMMIT = r"[0-9a-f]{7,40}"  # a backticked run of hex is a commit
OWN_DATA_PROBES = {"MY_MODEL": "tests/fixtures/tour/depot_model.yaml", "MY_ALTERNATIVES": "tests/fixtures/tour/depot_sites.yaml"}  # each own-data guard, and a committed file to point it at
SOURCE_KINDS = ("Incident:", "Design:", "Literature:")  # the wrong answer happened here; a choice made here; a failure known outside


def shape_of(heading: str) -> str | None:
    """`## Case` or `## Limit` as a whole word, so `## Cases` and `## Limits` are neither."""
    return next((shape for shape in SHAPES if re.match(re.escape(shape) + r"\b", heading)), None)


def sections(path: Path) -> list[tuple[str, str, str, str]]:
    """Each case or limit as (shape, heading, its text, its code), from its heading to the next `## ` line."""
    found: list[list[str]] = []
    open_section = None
    for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
        text = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and text.startswith("## "):
            shape = shape_of(text)
            open_section = [shape, text.splitlines()[0], "", ""] if shape else None
            if open_section:
                found.append(open_section)
        if open_section:
            open_section[2 if cell["cell_type"] == "markdown" else 3] += text + "\n\n"  # a blank line: a source ends with its cell
    return [tuple(section) for section in found]


def names_loaded(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}


CONTAINERS = ("list", "dict", "set", "tuple", "frozenset")  # wrapping a literal in one of these computes nothing


def literal_only(node: ast.AST) -> bool:
    return not any(isinstance(n, (ast.Name, ast.Call)) for n in ast.walk(node))


def assignments(tree: ast.AST):
    """Each assignment as (target, the value assigned to it): `a, b = x, y` yields (a, x) and (b, y), not (a, (x, y))."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
            for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
                paired = isinstance(target, (ast.Tuple, ast.List)) and isinstance(node.value, (ast.Tuple, ast.List)) and len(target.elts) == len(node.value.elts)
                yield from zip(target.elts, node.value.elts, strict=True) if paired else [(target, node.value)]


def calls_one_of(functions: set[str], expression: ast.AST) -> bool:
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in functions for n in ast.walk(expression))


def held(path: Path, shape: str) -> list[tuple[str, str, str]]:
    return [(heading, text, code) for found, heading, text, code in sections(path) if found == shape]


def sources(path: Path) -> list[tuple[str, str]]:
    """Each case's heading and its source: the text from `**Source.**` to the end of that paragraph."""
    found = []
    for heading, text, _ in held(path, "## Case"):
        if "**Source.**" in text:
            found.append((heading, text.split("**Source.**", 1)[1].split("\n\n", 1)[0].strip()))
    return found


def squeeze(text: str) -> str:
    """Whitespace runs to one space, so a phrase matches across a line break."""
    return " ".join(text.split())


def quoted(source: str, pattern: str) -> list[str]:
    """Every backticked token in a source that matches the pattern in full."""
    return [token for token in re.findall(r"`([^`]+)`", source) if re.fullmatch(pattern, token)]


def defined_tests() -> set[str]:
    names: set[str] = set()
    for module in TESTS_DIR.rglob("test_*.py"):
        names.update(re.findall(r"^\s*(?:def|class)\s+(test_\w+|Test\w+)", module.read_text(encoding="utf-8"), re.MULTILINE))
    return names


def git(*arguments: str) -> subprocess.CompletedProcess:
    """git in this repo and no other: an inherited GIT_DIR would answer for another repository."""
    environment = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(ROOT), *arguments], capture_output=True, text=True, env=environment)


def test_there_is_a_case_notebook_to_hold():
    assert CASE_NOTEBOOKS, f"no cases_*.ipynb under {NOTEBOOK_DIR}: the checks below would pass over nothing"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_it_holds_at_least_one_case(path):
    assert held(path, "## Case"), f"{path.name} is named as a case notebook and has no `## Case` section"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_heading_is_one_the_module_knows(path):
    """A heading the module cannot place closes the section before it and is read by nothing: a misspelled case is unchecked."""
    for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
        heading = "".join(cell["source"]).splitlines()[0] if cell["source"] else ""
        if cell["cell_type"] == "markdown" and heading.startswith("## "):
            known = shape_of(heading) or re.match(OTHER_HEADINGS, heading)
            assert known, f"{path.name} {heading!r} is not a case, a limit, a numbered section, the confidence section, the own-data cell or the closing links"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_it_says_how_sure(path):
    """A `## Confidence` section, and under it a cell that asserts something: one doubt run through to the report."""
    code, inside = "", False
    for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
        text = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and text.startswith("## "):
            inside = bool(re.match(HOW_SURE, text))
        elif inside and cell["cell_type"] == "code":
            code += text + "\n"
    asserts = code and any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(code)))
    assert asserts, f"{path.name} has no `## Confidence` (or `## How sure`) section whose cell asserts what survives a doubt and what does not"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_section_states_its_parts(path):
    """A case without its source is an invented example; a limit without its collector is a complaint."""
    for shape, heading, text, _ in sections(path):
        missing = [part for part in SHAPES[shape] if part not in text]
        assert not missing, f"{path.name} {heading!r} lacks {missing}"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_case_asserts_its_naive_answer_against_the_repos(path):
    """The naive answer is computed in the cell, and one assert compares it with a name that is not naive."""
    for heading, _, code in held(path, "## Case"):
        tree = ast.parse(code)
        ran: set[str] = set()  # naive names assigned from an expression that calls something
        derived: list[tuple[set[str], set[str]]] = []  # naive names assigned from other names, and those names
        functions = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("naive")}
        for target, value in assignments(tree):
            named = {n.id for n in ast.walk(target) if isinstance(n, ast.Name) and n.id.startswith("naive")}
            if any(isinstance(n, ast.Call) for n in ast.walk(value)):
                ran.update(named)
            else:
                derived.append((named, names_loaded(value)))
        for _ in derived:  # a naive name read from one a rule computed is computed too, however long the chain
            for named, loaded in derived:
                if loaded & ran:
                    ran.update(named)
        for target, value in assignments(tree):  # no naive name is typed in: each comes from a call, a variable, or another naive name
            typed = sorted(n.id for n in ast.walk(target) if isinstance(n, ast.Name) and n.id.startswith("naive"))
            literal = not any(isinstance(n, ast.Name) for n in ast.walk(value))
            empty = isinstance(value, (ast.Dict, ast.List, ast.Set, ast.Tuple)) and not (value.keys if isinstance(value, ast.Dict) else value.elts)
            wrapped = isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id in CONTAINERS and all(literal_only(a) for a in value.args) and not value.keywords
            assert not (typed and not empty and (literal or wrapped)), f"{path.name} {heading!r} types in {typed} as a literal: a naive answer is computed by the naive rule"
        assert ran or calls_one_of(functions, tree), (
            f"{path.name} {heading!r} computes no naive answer: a constant, a value read back, or a naive function nothing calls is not a rule that ran"
        )
        compared = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                loaded = names_loaded(node.test)
                others = {name for name in loaded if not name.startswith("naive") and not hasattr(builtins, name)}
                compared = compared or (bool(loaded & ran or calls_one_of(functions, node.test)) and bool(others))
        assert compared, f"{path.name} {heading!r} has no assert that sets a naive answer a rule computed beside the repo's"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_limit_pins_the_present_state(path):
    """A limit asserts what is true today, so the cell fails on the day the limit lifts."""
    for heading, _, code in held(path, "## Limit"):
        assert any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(code))), (
            f"{path.name} {heading!r} asserts nothing: a limit that no cell pins is prose"
        )


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_source_says_what_kind_it_is(path):
    """An incident happened here, a design was chosen here, a literature failure is known outside: the reader is told which."""
    for heading, source in sources(path):
        assert source.startswith(SOURCE_KINDS), f"{path.name} {heading!r}: its source begins with none of {SOURCE_KINDS}"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_source_names_a_test_that_exists(path):
    """A case shows a rule some test holds. A source that names no test, or one nobody wrote, is not checked by anything."""
    defined = defined_tests()
    for heading, source in sources(path):
        named = quoted(source, r"test_\w+|Test\w+")
        assert named, f"{path.name} {heading!r}: its source names no test in backticks"
        missing = [name for name in named if name not in defined]
        assert not missing, f"{path.name} {heading!r}: its source names {missing}, defined nowhere under {TESTS_DIR.name}/"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_file_a_section_names_exists(path):
    """A case's source and a limit's text name files in backticks; each is in the repo."""
    named = sources(path) + [(heading, text) for heading, text, _ in held(path, "## Limit")]
    for heading, text in named:
        missing = [name for name in quoted(text, PATH) if not (ROOT / name).exists()]
        assert not missing, f"{path.name} {heading!r} names {missing}, absent from the repo"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_a_limit_that_cites_a_gap_finds_it_open(path):
    """A limit recorded in a gap register lifts when its row closes, with no code change for a cell to see."""
    for heading, text, _ in held(path, "## Limit"):
        gaps = quoted(text, r"[A-Z]{1,3}\d+")
        if not gaps:
            continue
        registers = [ROOT / name for name in quoted(text, PATH) if name.endswith("gaps.md") and (ROOT / name).exists()]
        assert registers, f"{path.name} {heading!r} names gap {gaps} and no gap register that exists"
        rows = [line for register in registers for line in register.read_text(encoding="utf-8").splitlines()]
        for gap in gaps:
            row = next((line for line in rows if re.match(rf"\|\s*{gap}\s*\|", line)), None)
            assert row, f"{path.name} {heading!r} names gap {gap}, which its register does not hold"
            status = row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()
            assert status.startswith("open"), f"{path.name} {heading!r}: gap {gap} is no longer open; rewrite the limit"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_incident_names_its_record(path):
    """An incident is a claim about history: it carries the commit that fixed it, or the file that recorded it."""
    for heading, source in sources(path):
        if source.startswith("Incident:"):
            record = quoted(source, COMMIT) + [n for n in quoted(source, PATH) if "tests/" not in n]
            assert record, f"{path.name} {heading!r}: an incident with no commit and no record file in backticks"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_commit_a_source_names_is_in_the_history(path):
    """Skips, visibly, where the history is not all here: a shallow clone cannot tell an old commit from an invented one."""
    named = [(heading, commit) for heading, source in sources(path) for commit in quoted(source, COMMIT)]
    if not named:
        return
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
        pytest.skip("no git, or a shallow clone: the commits the sources name were not checked")
    for heading, commit in named:
        found = git("cat-file", "-e", f"{commit}^{{commit}}").returncode == 0
        assert found, f"{path.name} {heading!r}: its source names commit {commit}, which this history does not hold"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_every_incident_quotes_its_record(path):
    """An incident says what was seen, in the record's own words: a phrase in double quotes, found in a file or a
    commit message the source names. A source that says "no run is on record" beside a record that says otherwise
    is the commonest fault a review finds, and a quotation is the part of it a test can hold."""
    for heading, source in sources(path):
        if not source.startswith("Incident:"):
            continue
        quotes = [squeeze(q) for q in re.findall(r'["\u201c]([^"\u201c\u201d]+)["\u201d]', source)]
        assert quotes, f"{path.name} {heading!r}: an incident that quotes nothing from its record"
        records = [squeeze((ROOT / name).read_text(encoding="utf-8", errors="replace")) for name in quoted(source, PATH) if (ROOT / name).is_file()]
        messages = [git("log", "-1", "--format=%B", commit) for commit in quoted(source, COMMIT)]
        if any(message.returncode != 0 for message in messages):
            if git("rev-parse", "--is-shallow-repository").stdout.strip() != "false":
                pytest.skip("no git, or a shallow clone: a quotation from a commit message was not checked")
            continue  # the history is all here and the commit is not in it: the commit test's finding
        records += [squeeze(message.stdout) for message in messages]
        missing = [q for q in quotes if not any(q in record for record in records)]
        assert not missing, f"{path.name} {heading!r}: {len(missing)} quoted phrase(s) are in no file or commit message the source names"


@pytest.mark.parametrize("path", CASE_NOTEBOOKS, ids=lambda p: p.name)
def test_the_own_data_branch_runs_over_a_committed_fixture(path, monkeypatch):
    """The suite never ran the reader's branch, and that is where reviews found a crash, a wrong label, and a number
    the product withholds. Here it runs once, each guard pointed at a committed file, with its output discarded
    and a failure named by type only: this proves the branch finishes, not that what it prints is right."""
    assert OWN_DATA_PROBES, f"{path.name}: name a committed fixture for each own-data guard in OWN_DATA_PROBES"
    missing = sorted(probe for probe in OWN_DATA_PROBES.values() if not (ROOT / probe).is_file())
    assert not missing, f"{path.name}: OWN_DATA_PROBES names {missing}, absent from the repo"
    set_by_probe: set[str] = set()

    class PointTheGuards(ast.NodeTransformer):
        def visit_Assign(self, node: ast.Assign) -> ast.Assign:
            names = [t.id for t in node.targets if isinstance(t, ast.Name) and t.id in OWN_DATA_PROBES]
            if names and isinstance(node.value, ast.Constant) and node.value.value is None:
                set_by_probe.update(names)
                node.value = ast.Constant(str(ROOT / OWN_DATA_PROBES[names[0]]))
            return node

        def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:  # `MY_X: str | None = None`
            if isinstance(node.target, ast.Name) and node.target.id in OWN_DATA_PROBES and isinstance(node.value, ast.Constant) and node.value.value is None:
                set_by_probe.add(node.target.id)
                node.value = ast.Constant(str(ROOT / OWN_DATA_PROBES[node.target.id]))
            return node

    monkeypatch.setenv("MPLBACKEND", "Agg")
    monkeypatch.chdir(NOTEBOOK_DIR)
    monkeypatch.syspath_prepend(str(NOTEBOOK_DIR))
    namespace: dict = {"__name__": "__main__"}
    raised = None
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            for number, cell in enumerate(c for c in json.loads(path.read_text(encoding="utf-8"))["cells"] if c["cell_type"] == "code"):
                tree = ast.fix_missing_locations(PointTheGuards().visit(ast.parse("".join(cell["source"]))))
                try:
                    exec(compile(tree, f"{path.name}[cell {number}]", "exec"), namespace)
                except Exception as error:  # the message may carry what the branch read
                    raised = (number, type(error).__name__)
                    break
    finally:
        pyplot = sys.modules.get("matplotlib.pyplot")
        if pyplot is not None:
            pyplot.close("all")
    if raised:  # outside the except block, so no chained error is printed
        pytest.fail(f"{path.name} code cell {raised[0]} raised {raised[1]} with the own-data guards on a committed fixture; message withheld", pytrace=False)
    unset = sorted(set(OWN_DATA_PROBES) - set_by_probe)
    assert not unset, f"{path.name} never sets {unset} to None: OWN_DATA_PROBES names a guard the notebook does not have"
