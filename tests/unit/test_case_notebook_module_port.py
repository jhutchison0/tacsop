"""test_case_notebooks.py ports to another repo as it stands, and each of its rules fails alone.

Each test builds a small repo with pytester: one case notebook, one test the case's source
names, and a copy of the hub's test_case_notebooks.py. It runs pytest on that copy in a child
process. The built repo is not a git repository, so the commit check's skip is exercised too.
"""

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

HUB_MODULE = Path(__file__).with_name("test_case_notebooks.py")
SOURCE = "**Source.** Design: `pkg/rule.py`. `test_rule` holds it."
TEXT = (
    "## Case 1. A sum is not a count\n\n**Question.** How many?\n\n**Fixture.** Three numbers.\n\n"
    "**Naive.** Count them.\n\n**The repo's rule.** Sum them.\n\n" + SOURCE
)
CODE = "naive_count = len([1, 2, 3])\nright = sum([1, 2, 3])\nassert naive_count != right"
LIMIT_TEXT = "## Limit. Unknown\n\n**Question.** Why?\n\n**What is not known.** It.\n\n**What would settle it.** A count."


CONFIDENCE = (("markdown", "## Confidence. One doubt, run through"), ("code", "doubt = [1, 2]\nassert len(doubt) == 2"))
OWN_DATA = (("markdown", "## Your own data"), ("code", "MY_DATA = None\nif MY_DATA is not None:\n    seen = open(MY_DATA).read()"))


def module_for_a_built_repo(probes: str = '{"MY_DATA": "pkg/rule.py"}') -> str:
    text, count = re.subn(r"^OWN_DATA_PROBES[^\n]*=.*$", f"OWN_DATA_PROBES = {probes}", HUB_MODULE.read_text(), flags=re.MULTILINE)
    assert count == 1, "test_case_notebooks.py has no single OWN_DATA_PROBES line to set"
    return text


def run(pytester, *cells: tuple[str, str], confidence: bool = True, own_data: tuple = OWN_DATA, probes: str | None = None):
    """Run the hub's module over a case notebook of these (kind, source) cells and return pytest's result.

    A minimal confidence section is appended unless the test is about that section."""
    cells = (*cells, *CONFIDENCE) if confidence else cells
    cells = (*cells, *own_data)
    root = pytester.path
    (root / "pkg").mkdir()
    (root / "pkg" / "rule.py").write_text("RULE = sum\n")
    (root / "notebooks").mkdir()
    built = [{"cell_type": kind, "metadata": {}, "source": text} | ({"outputs": [], "execution_count": None} if kind == "code" else {})
             for kind, text in cells]
    (root / "notebooks" / "cases_counts.ipynb").write_text(json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": built}))
    (root / "tests" / "unit").mkdir(parents=True, exist_ok=True)
    (root / "tests" / "unit" / "test_rule.py").write_text("def test_rule():\n    assert sum([1, 2, 3]) == 6\n")
    (root / "tests" / "unit" / "test_case_notebooks.py").write_text(module_for_a_built_repo(probes) if probes else module_for_a_built_repo())
    return pytester.runpytest_subprocess("-rA", "tests/unit/test_case_notebooks.py")


def failed(result) -> list[str]:
    return re.findall(r"^FAILED tests/unit/test_case_notebooks\.py::(\w+)", result.stdout.str(), flags=re.MULTILINE)


def test_a_whole_case_passes_every_rule(pytester):
    run(pytester, ("markdown", TEXT), ("code", CODE)).assert_outcomes(passed=15)


@pytest.mark.parametrize("part", ["**Question.**", "**Fixture.**", "**Naive.**", "**The repo's rule.**"])
def test_a_case_missing_a_part_fails_the_parts_test_alone(pytester, part):
    result = run(pytester, ("markdown", TEXT.replace(part, part.strip("*"))), ("code", CODE))

    assert failed(result) == ["test_every_section_states_its_parts"], result.stdout.str()


@pytest.mark.parametrize("code", [
    "naive_count = 3\nassert naive_count == naive_count",  # against itself
    "naive_count = 3\nassert naive_count == 3",  # against a constant
    "naive_count = 3\nassert len([naive_count]) == abs(1)",  # against builtins
    "count = 3\nright = 6\nassert count != right",  # no naive name
    "naive_count = len([3])\nright = 6\nprint(naive_count != right)",  # no assert
])
def test_a_case_that_never_sets_naive_beside_the_repos_answer_fails_the_comparison_test_alone(pytester, code):
    result = run(pytester, ("markdown", TEXT), ("code", code))

    assert failed(result) == ["test_every_case_asserts_its_naive_answer_against_the_repos"], result.stdout.str()


@pytest.mark.parametrize("source, test", [
    ("**Source.** `pkg/rule.py`. `test_rule` holds it.", "test_every_source_says_what_kind_it_is"),
    ("**Source.** Design: `pkg/rule.py`. A test holds it.", "test_every_source_names_a_test_that_exists"),
    ("**Source.** Design: `pkg/rule.py`. `test_nobody_wrote` holds it.", "test_every_source_names_a_test_that_exists"),
    ("**Source.** Design: `pkg/gone.py`. `test_rule` holds it.", "test_every_file_a_section_names_exists"),
    
])
def test_a_source_the_repo_cannot_show_fails_its_own_test_alone(pytester, source, test):
    result = run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE))

    assert failed(result) == [test], result.stdout.str()


def test_an_incident_may_name_a_record_file_in_place_of_a_commit(pytester):
    source = '**Source.** Incident: recorded in `pkg/rule.py`, which reads "RULE = sum". `test_rule` holds the fix.'

    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=15)


def test_a_commit_that_cannot_be_checked_is_reported_as_skipped_not_passed(pytester):
    source = '**Source.** Incident: commit `abc1234`, whose message reads "a fix". `test_rule` holds the fix.'

    # two skips, both visible: the commit is not checked, and neither is the quotation from its message
    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=13, skipped=2)


def test_a_limit_with_no_assert_fails_the_limit_test_alone(pytester):
    result = run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", LIMIT_TEXT), ("code", "known = None"))

    assert failed(result) == ["test_every_limit_pins_the_present_state"], result.stdout.str()


def test_a_limit_missing_its_collector_fails_the_parts_test_alone(pytester):
    limit = LIMIT_TEXT.replace("**What would settle it.**", "What would settle it.")
    result = run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", limit), ("code", "assert True"))

    assert failed(result) == ["test_every_section_states_its_parts"], result.stdout.str()


def test_a_notebook_named_for_cases_that_holds_none_fails(pytester):
    result = run(pytester, ("markdown", TEXT.replace("## Case 1.", "## Example 1.")), ("code", CODE))

    assert failed(result) == ["test_it_holds_at_least_one_case", "test_every_heading_is_one_the_module_knows"], result.stdout.str()


@pytest.mark.parametrize("heading", ["## Cas 1. A sum is not a count", "## case 1. A sum is not a count", "## Limits. Unknown"])
def test_a_heading_the_module_does_not_know_fails_and_cannot_hide_a_case(pytester, heading):
    # A misspelled heading once dropped a case from every check: the section closed and nothing read it.
    hidden = TEXT.replace("## Case 1. A sum is not a count", heading).replace("**Source.** Design:", "Design:")
    result = run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", hidden), ("code", "pass"))

    assert failed(result) == ["test_every_heading_is_one_the_module_knows"], result.stdout.str()


def test_numbered_sections_own_data_and_where_next_are_known_headings(pytester):
    cells = [("markdown", "## 1. The passage, once"), ("code", "x = 1"), ("markdown", TEXT), ("code", CODE),
             ("markdown", "## Confidence. What these numbers can bear"), ("code", "assert x == 1"),
             ("markdown", "## Where next\n\n- the tour")]

    run(pytester, *cells).assert_outcomes(passed=15)


@pytest.mark.parametrize("code", [
    "labels = ['a', 'b']\nnaive_name = labels[0]\nright = 'c'\nassert naive_name != right",  # read back, never computed
    "naive_count = 3\nright = 6\nassert naive_count != right",  # a constant
])
def test_a_naive_answer_that_no_rule_computed_fails_the_comparison_test_alone(pytester, code):
    # The pilot's case 2 read its naive answer back from the line that wrote it; nothing naive ever ran.
    result = run(pytester, ("markdown", TEXT), ("code", code))

    assert failed(result) == ["test_every_case_asserts_its_naive_answer_against_the_repos"], result.stdout.str()


def test_a_naive_rule_written_as_a_function_counts_as_computed(pytester):
    code = "def naive_total(xs):\n    return len(xs)\n\nright = sum([1, 2, 3])\nassert naive_total([1, 2, 3]) != right"

    run(pytester, ("markdown", TEXT), ("code", code)).assert_outcomes(passed=15)


GAP_LIMIT = (
    "## Limit. Unknown\n\n**Question.** Why?\n\n**What is not known.** Gap `G6` in `docs/gaps.md`.\n\n"
    "**What would settle it.** A count."
)


def with_gaps(pytester, status: str, *cells):
    (pytester.path / "docs").mkdir()
    (pytester.path / "docs" / "gaps.md").write_text(f"| ID | Gap | Status |\n|---|---|---|\n| G6 | a doubt | {status} |\n")
    return run(pytester, ("markdown", TEXT), ("code", CODE), *cells)


def test_a_limit_that_cites_an_open_gap_passes(pytester):
    with_gaps(pytester, "open", ("markdown", GAP_LIMIT), ("code", "assert True")).assert_outcomes(passed=15)


def test_a_limit_whose_gap_has_closed_fails(pytester):
    # A limit in a register lifts with no code change; the cell's own assert cannot see that.
    result = with_gaps(pytester, "closed 2026-11-16 by a probe", ("markdown", GAP_LIMIT), ("code", "assert True"))

    assert failed(result) == ["test_a_limit_that_cites_a_gap_finds_it_open"], result.stdout.str()


def test_a_limit_that_names_a_missing_file_fails_the_file_test(pytester):
    result = run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", GAP_LIMIT), ("code", "assert True"))

    assert failed(result) == ["test_every_file_a_section_names_exists", "test_a_limit_that_cites_a_gap_finds_it_open"], result.stdout.str()


@pytest.mark.parametrize("code", [
    # a naive function is defined and never called; the answer compared is a constant
    "def naive_total(xs):\n    return len(xs)\n\nnaive_count = 3\nright = sum([1, 2, 3])\nassert naive_count != right",
    # a naive value is computed, and the assert compares a different, constant one
    "naive_seen = len([1, 2, 3])\nnaive_count = 3\nright = sum([1, 2, 3])\nassert naive_count != right",
])
def test_the_naive_answer_in_the_assert_is_one_a_rule_computed(pytester, code):
    # The pilot's fix-up found both: a `def naive_` anywhere satisfied the rule, called or not.
    result = run(pytester, ("markdown", TEXT), ("code", code))

    assert failed(result) == ["test_every_case_asserts_its_naive_answer_against_the_repos"], result.stdout.str()


def test_a_naive_function_called_inside_the_assert_counts(pytester):
    code = "def naive_total(xs):\n    return len(xs)\n\nright = sum([1, 2, 3])\nassert naive_total([1, 2, 3]) != right"

    run(pytester, ("markdown", TEXT), ("code", code)).assert_outcomes(passed=15)


def test_a_source_ends_with_its_cell_and_does_not_read_the_closing_text(pytester):
    # Cells were joined by one newline, so a source that ended its cell absorbed the next cell's paragraph.
    closing = "The naive answer is half the right one. See `test_nobody_wrote` and `pkg/gone.py` for what it is not."

    run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", closing)).assert_outcomes(passed=15)


def test_a_repo_with_a_tour_and_no_case_notebook_fails_and_checks_nothing_else(pytester):
    root = pytester.path
    (root / "notebooks").mkdir()
    (root / "notebooks" / "tour_only.ipynb").write_text(json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": []}))
    (root / "tests" / "unit").mkdir(parents=True)
    (root / "tests" / "unit" / "test_case_notebooks.py").write_text(module_for_a_built_repo())
    result = pytester.runpytest_subprocess("-rA", "tests/unit/test_case_notebooks.py")

    assert failed(result) == ["test_there_is_a_case_notebook_to_hold"], result.stdout.str()
    result.assert_outcomes(failed=1, skipped=14)


def committed_repo(pytester) -> str:
    """Make the built repo a git repository with one commit, and return that commit's short hash."""
    environment = {name: value for name, value in os.environ.items() if not name.startswith("GIT_")}
    identity = ["-c", "user.name=port test", "-c", "user.email=port@test.invalid", "-c", "commit.gpgsign=false"]

    def git(*arguments: str) -> str:
        done = subprocess.run(["git", "-C", str(pytester.path), *identity, *arguments], capture_output=True, text=True, env=environment)
        assert done.returncode == 0, done.stderr
        return done.stdout.strip()

    git("init", "-q")
    (pytester.path / "seed.txt").write_text("seed\n")
    git("add", "seed.txt")
    git("commit", "-q", "-m", "seed")
    return git("rev-parse", "--short=7", "HEAD")


def test_a_commit_in_the_history_passes_the_commit_test(pytester):
    source = f'**Source.** Incident: commit `{committed_repo(pytester)}`, whose message reads "seed". `test_rule` holds the fix.'

    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=15)


def test_a_commit_the_history_does_not_hold_fails_the_commit_test_alone(pytester):
    real = committed_repo(pytester)
    invented = "".join("0123456789abcdef"[(int(c, 16) + 1) % 16] for c in real)
    source = f'**Source.** Incident: commit `{invented}`, whose message reads "seed". `test_rule` holds the fix.'
    result = run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE))

    assert failed(result) == ["test_every_commit_a_source_names_is_in_the_history"], result.stdout.str()


def test_a_case_notebook_with_no_confidence_section_fails(pytester):
    # Three builders deleted the section as a mutant and every test still passed.
    result = run(pytester, ("markdown", TEXT), ("code", CODE), confidence=False)

    assert failed(result) == ["test_it_says_how_sure"], result.stdout.str()


def test_a_confidence_section_that_asserts_nothing_fails(pytester):
    result = run(pytester, ("markdown", TEXT), ("code", CODE), ("markdown", "## Confidence. How sure"), ("code", "print(1)"), confidence=False)

    assert failed(result) == ["test_it_says_how_sure"], result.stdout.str()


@pytest.mark.parametrize("code", [
    # five builders' mutant: one naive answer typed as a literal beside an honest one
    "def naive_total(xs):\n    return len(xs)\n\nnaive_count = 3\nright = sum([1, 2, 3])\nassert naive_total([1, 2, 3]) != right\nassert naive_count != right",
    "naive_seen = len([1, 2, 3])\nnaive_by_order = {'a': 1, 'b': 2}\nright = sum([1, 2, 3])\nassert naive_seen != right",
    "naive_seen = len([1, 2, 3])\nnaive_list = list([1, 2])\nright = sum([1, 2, 3])\nassert naive_seen != right",
])
def test_every_naive_name_is_computed_not_typed(pytester, code):
    result = run(pytester, ("markdown", TEXT), ("code", code))

    assert failed(result) == ["test_every_case_asserts_its_naive_answer_against_the_repos"], result.stdout.str()


def test_a_naive_name_derived_from_another_naive_name_is_computed(pytester):
    code = "naive_order = sorted([3, 1, 2])\nnaive_first = naive_order[0]\nright = sum([1, 2, 3])\nassert naive_first != right"

    run(pytester, ("markdown", TEXT), ("code", code)).assert_outcomes(passed=15)


RECORD = "Verified live: the page reads Declared Run, Achieved Run.\n"


def with_record(pytester, source: str):
    (pytester.path / "docs").mkdir(exist_ok=True)
    (pytester.path / "docs" / "review.md").write_text(RECORD)
    return run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE))


def test_an_incident_that_quotes_its_record_passes(pytester):
    source = '**Source.** Incident: a live probe, "the page reads Declared Run, Achieved Run" (`docs/review.md`). `test_rule` holds the fix.'

    with_record(pytester, source).assert_outcomes(passed=15)


@pytest.mark.parametrize("source", [
    # two of four sources in one review said "no run is on record" beside a file that said "Verified live"
    "**Source.** Incident: a reviewer read it off the code; no run is on record (`docs/review.md`). `test_rule` holds the fix.",
    '**Source.** Incident: the record says "no run showing the wrong page exists" (`docs/review.md`). `test_rule` holds the fix.',
])
def test_an_incident_that_does_not_quote_its_record_or_misquotes_it_fails(pytester, source):
    result = with_record(pytester, source)

    assert failed(result) == ["test_every_incident_quotes_its_record"], result.stdout.str()


def test_an_incident_may_quote_the_message_of_the_commit_it_names(pytester):
    commit = committed_repo(pytester)
    source = f'**Source.** Incident: commit `{commit}`, whose message reads "seed". `test_rule` holds the fix.'

    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=15)


def test_an_incident_with_no_commit_and_no_record_file_fails(pytester):
    source = '**Source.** Incident: it went wrong in March, "badly". `test_rule` holds it.'
    result = run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE))

    assert failed(result) == ["test_every_incident_names_its_record", "test_every_incident_quotes_its_record"], result.stdout.str()


def test_a_repo_that_reserves_the_word_may_head_the_section_how_sure(pytester):
    # One repo's glossary keeps "confidence" for its own output; the kernel's phrase for rule 9 is "say how sure".
    cells = [("markdown", TEXT), ("code", CODE), ("markdown", "## How sure. One doubt, run through"), ("code", "assert 1 + 1 == 2")]

    run(pytester, *cells, confidence=False).assert_outcomes(passed=15)


def test_a_literal_beside_a_call_in_one_tuple_assignment_is_still_typed(pytester):
    # `naive_left, right = [1, 2], compute()` once credited both names with the call on the right.
    code = "naive_count, right = 3, sum([1, 2, 3])\nassert naive_count != right"
    result = run(pytester, ("markdown", TEXT), ("code", code))

    assert failed(result) == ["test_every_case_asserts_its_naive_answer_against_the_repos"], result.stdout.str()


def test_a_computed_naive_answer_in_a_tuple_assignment_counts(pytester):
    code = "naive_count, right = len([1, 2, 3]), sum([1, 2, 3])\nassert naive_count != right"

    run(pytester, ("markdown", TEXT), ("code", code)).assert_outcomes(passed=15)


def test_a_quote_may_cross_a_line_break_in_its_record_and_use_curly_quotes(pytester):
    (pytester.path / "docs").mkdir()
    (pytester.path / "docs" / "review.md").write_text("Verified live: the page\nreads   Declared Run.\n")
    source = "**Source.** Incident: a probe saw “the page reads Declared Run” (`docs/review.md`). `test_rule` holds the fix."

    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=15)


def test_a_limit_that_cites_a_gap_its_register_does_not_hold_fails(pytester):
    limit = GAP_LIMIT.replace("`G6`", "`G77`")
    result = with_gaps(pytester, "open", ("markdown", limit), ("code", "assert True"))

    assert failed(result) == ["test_a_limit_that_cites_a_gap_finds_it_open"], result.stdout.str()


def test_a_literature_source_that_names_a_test_class_passes(pytester):
    (pytester.path / "tests" / "unit").mkdir(parents=True)
    (pytester.path / "tests" / "unit" / "test_held.py").write_text("class TestRule:\n    def test_it(self):\n        assert True\n")
    source = "**Source.** Literature: Saaty 1980 on rank reversal. `TestRule` holds the repo's rule."

    run(pytester, ("markdown", TEXT.replace(SOURCE, source)), ("code", CODE)).assert_outcomes(passed=15)


RUNS_OWN_DATA = "test_the_own_data_branch_runs_over_a_committed_fixture"


def test_an_own_data_branch_that_breaks_on_a_committed_fixture_fails_without_printing_it(pytester):
    # Eight reviews found their Critical in the branch nothing ran: a crash, a wrong label, a number the product withholds.
    marker = "READER-DATA-4d2b"
    broken = (("markdown", "## Your own data"), ("code", f"MY_DATA = None\nif MY_DATA is not None:\n    raise KeyError('{marker} ' + str(MY_DATA))"))
    result = run(pytester, ("markdown", TEXT), ("code", CODE), own_data=broken)

    assert failed(result) == [RUNS_OWN_DATA], result.stdout.str()
    assert marker not in result.stdout.str() + result.stderr.str()


def test_an_own_data_branch_may_not_print_while_it_is_probed(pytester):
    marker = "READER-DATA-77c0"
    chatty = (("markdown", "## Your own data"), ("code", f"MY_DATA = None\nif MY_DATA is not None:\n    print('{marker}', open(MY_DATA).read())"))
    result = run(pytester, ("markdown", TEXT), ("code", CODE), own_data=chatty)

    result.assert_outcomes(passed=15)
    assert marker not in result.stdout.str() + result.stderr.str()


@pytest.mark.parametrize("probes, why", [
    ("{}", "no probe named"),
    ('{"MY_OTHER": "pkg/rule.py"}', "a guard the notebook never sets"),
    ('{"MY_DATA": "pkg/gone.py"}', "a fixture that is not committed"),
])
def test_a_probe_that_reaches_no_branch_fails(pytester, probes, why):
    result = run(pytester, ("markdown", TEXT), ("code", CODE), probes=probes)

    assert failed(result) == [RUNS_OWN_DATA], why + "\n" + result.stdout.str()


def test_a_guard_written_with_an_annotation_is_still_pointed_at_its_fixture(pytester):
    # `MY_DATA: str | None = None` is a plain way to write a guard; the probe must reach it.
    marker = "PROBED-ANNOTATED-91e3"
    annotated = (("markdown", "## Your own data"),
                 ("code", f"MY_DATA: str | None = None\nif MY_DATA is not None:\n    raise KeyError('{marker}')"))
    result = run(pytester, ("markdown", TEXT), ("code", CODE), own_data=annotated)

    assert failed(result) == [RUNS_OWN_DATA], result.stdout.str()  # the branch ran, and raised
    assert "KeyError" in result.stdout.str() and marker not in result.stdout.str() + result.stderr.str()


def test_an_empty_container_filled_later_by_a_rule_is_not_a_typed_in_answer(pytester):
    # `naive_a, repo_a = {}, {}` then a loop that fills each from a call is an accumulator, not a literal answer.
    code = "naive_seen, right = {}, {}\nfor n in (1, 2):\n    naive_seen[n] = len([n])\n    right[n] = sum([n, n])\nnaive_total = sum(naive_seen.values())\nassert naive_total != sum(right.values())"

    run(pytester, ("markdown", TEXT), ("code", code)).assert_outcomes(passed=15)
