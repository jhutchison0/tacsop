---
name: writing-tours-and-case-notebooks
description: House rule for the notebooks that show how a repo works. Two kinds, both run by the test suite over committed fixtures. A tour walks the main path once; a case notebook stops where the obvious rule gives a different answer, runs it beside the repo's, and says how sure the result is. Use when writing or reviewing a notebook under notebooks/, choosing what a repo's next notebook should be, or choosing the display for a notebook section.
version: "0.3.0"
---

# Writing Tours and Case Notebooks

A notebook under `notebooks/` is an example of how the repo works, and the suite runs it like any other example. This skill says which notebooks a repo carries, what each one owes its reader, what the suite holds, and what only a reviewer can. The failure it counters: a notebook that ran once on its author's machine, shows a result and none of the data behind it, and states more than its cells check.

Scope, stated once: `shift-left-testing` governs how code is tested, `designing-clear-data-displays` governs how a figure is drawn, and `verifying-claims` governs what a report may say. This skill governs what a notebook contains and in what order. Where they meet, a figure in a notebook follows the display skill in full, and a sentence in a notebook is a claim.

**Philosophy**: *Show the data at every level, show the wrong answer beside the right one, and say how sure.*

**Status**: 0.3.0, a draft kept out of propagation. The tour rules rest on thirteen reviewed first tours and three doctrine entries (2026-11-14 to 2026-11-16). The case rules rest on a rollout to thirteen repos on 2026-11-16, each notebook built by one agent and reviewed by another. That rollout changed this skill more than it confirmed it: see "What the Suite Cannot See". The test module stands at 0.7.2.

## When to Use

- Writing or reviewing any notebook under `notebooks/`
- Deciding what a repo's second notebook should be
- Looking for a case: reading a repo's fixes, gaps and reviews for rules worth showing
- Writing the section that says how sure a notebook's numbers are (`CONFIDENCE.md`)
- Choosing a display for a notebook section (`DISPLAYS.md`)
- Briefing an agent to build or review a notebook in another repo (`REVIEWING.md`)

## The Kinds

Two questions sort them: who acts, and whether the notebook goes wide or deep.

| | Breadth | Depth |
|---|---|---|
| **The repo shows** | **Tour**: the main path once, from a raw input to a result a person can see. `tour_from_<input>_to_<result>.ipynb` | **Cases**: the places on that path where the obvious rule gives a different answer. `cases_<what_goes_wrong>.ipynb` |
| **The reader does** | Walkthrough: one task, done on the reader's input | Problem set: the reader writes the answer and an assert checks it |

The top row is the standard, because it represents the repo: a tour says what the code does, and a case notebook says why it is written that way and how far its output can be trusted. A repo gets its tour first and its cases second. The bottom row is for a repo whose purpose is teaching; this skill does not yet rule on it, except that a case must not give away what a lesson asks its learner to predict. A demo is a tour with an audience and is not a fifth kind: it keeps every tour rule, the ban on saved output included.

## The Kernel

Nine rules. The sidecars expand them.

1. The suite runs every cell over committed fixtures. No saved output; the reader's own data stays behind a guard committed as `None`.
2. Show the data at three levels: as it arrives, as it is handled, as it is reported. Print one raw record whole.
3. A tour walks the main path once. A case stops where the obvious rule gives a different answer.
4. A case runs the naive rule beside the repo's and asserts the difference between them.
5. Every case names its source, and an incident quotes its record.
6. An assert must fail if the sentence above it were false. A sentence no assert reaches is cut, or cited.
7. A figure comes from the package, never from a cell. Under about twenty numbers, print a table.
8. Write for two readers: the heading and the display carry the argument; the cell, the assert and the source let it be checked.
9. Say how sure. At each level name the doubt, its kind and its size, and run one doubt through to the report.

## Three Levels

Rule 2 is the spine of both kinds. A reader who sees only the report cannot tell what was done to the data, and a reader who sees only the code cannot tell what the data looked like.

| Level | The reader's question | Show | A pipeline | A library |
|---|---|---|---|---|
| **Arrives** | What does the input look like before anything touches it? | One record printed whole, small enough to read | A log record as it was written | The arguments to a call |
| **Handled** | What is done to it, step by step? | The same record after each step, beside the one before | A parsed call, then a stored row | The validated object |
| **Reported** | What does a person downstream see? | The page, table or value the product ships, in every form it ships | The page a person opens | The returned value |

A tour passes through all three once, in order. A case names the level where its two rules part, then follows both answers to the report, because a wrong rule raises no error: it produces a report. Where the report is a short list, following it costs one line.

A library has all three. Do not invent a file format so that something can arrive; where a fixture's format is the notebook's own, the notebook says so, and no sentence credits the product with reading it.

## Three Lenses

A repo with an output to defend has up to three case notebooks. The first is expected; the others exist only where the repo has the material.

| Lens | Question | Example |
|---|---|---|
| **Construction** | Where does the obvious rule give a wrong answer? | Summing every record of a reply counts it twice |
| **Validity** | When is a correct output not to be believed? | A day with no data that reads as a day with no usage; a weight a criterion cannot spend |
| **Scope** | What must the output not be compared with or used for? | A benchmark run read as usage history |

## What Holds Each Rule

| Rule | Held by |
|---|---|
| 1 | `tests/unit/test_notebooks.py`: every cell run, no output, guards off, no reader's value in a failure message. Review, for the host's timezone, the hash seed and the wall clock (`TOURS.md`) |
| 2 | Review |
| 3 | The file name, and review |
| 4 | `tests/unit/test_case_notebooks.py`: a naive answer a rule computed, set beside a second name in an assert. Review, for whether the naive rule is one a person would write and whether the second name is the repo's answer |
| 5 | The same module: the source's kind, a cited test that exists, files and commits that exist, and for an incident a quotation found in its record. Review, for whether the record supports the sentence around the quotation, and whether the cited test fails under the naive rule |
| 6 | Review, with every assert and every conjunct negated one at a time. Negation is a floor |
| 7 | `test_notebooks.py` for the import; the display skill's review for the figure |
| 8 | Review |
| 9 | `test_case_notebooks.py`: the section exists and a cell under it asserts something. Review, for everything inside it (`CONFIDENCE.md`) |
| The own-data cell | `test_case_notebooks.py`: the branch finishes on a committed file. Review, by hand runs, for what it prints (`TOURS.md`) |

## What the Suite Cannot See

This is the rollout's main finding, and the reason `REVIEWING.md` exists.

In every reviewed notebook the mechanical record was clean: all asserts died when negated, and every structural mutant failed its named test. The reviews still found faults in most of them, including Criticals, and each was in a sentence, a label, or the branch the suite never runs.

- **A sentence above a passing assert.** A source said no run had shown the wrong page, beside a record that says "Verified live". A closing sentence said seven items were in no settled order, where most pairs were apart in the cell's own data.
- **An assert that passed by luck.** A claim held on one block of thirty random draws and on two of ten others. A headline held for the committed fixture and for a minority of fresh draws from its generator.
- **A number that belonged to the machine.** A gap between two sources was the host's offset from UTC. One map depended on the hash seed.
- **The own-data branch.** A cell printed a score the product's own report withholds. Another compared counts where the answers differed. A third printed "none" after reading nothing. Through most of the rollout the suite ran none of it; from module 0.7.0 it runs the branch once over a committed file, which proves it finishes and nothing about what it prints.

So a build report leads with what was checked by a second reader, and treats its negation count as a floor.

## What This Skill Is Not

- **Not a place for analysis.** Exploration and one-off analysis live outside `notebooks/`, with their outputs, under whatever rule the repo has for records.
- **Not a second test suite.** A case notebook shows a rule a test already holds, and names the test. A rule no test holds gets its test first.
- **Not a gallery.** A figure appears because a level or a comparison needs it. A notebook that draws nothing is complete if its tables carry the numbers.
- **Not a generator's output.** The `.ipynb` is the source. A script that first wrote it is a session tool and is not kept.
- **Not an assurance.** A notebook runs a product's logic over invented data. It says nothing about whether a real output is right, and where the product advises or decides for a person it says so in its opening cell.

## Sidecar Files

- [TOURS.md](TOURS.md): the shape of a tour, what every notebook owes, what "hermetic" covers, and the own-data cell. Read before writing any notebook.
- [CASES.md](CASES.md): the parts of a case, the naive rule, the three source kinds, the four shapes, where to find cases, and the test module. Read before writing a case notebook.
- [CONFIDENCE.md](CONFIDENCE.md): the section that says how sure: the table, the kinds, choosing the doubt to run, and the faults reviews found in it. Read before writing that section, every time.
- [DISPLAYS.md](DISPLAYS.md): which display suits which level, which comparison and which doubt. Read before a notebook section gets a figure.
- [REVIEWING.md](REVIEWING.md): what a second reader checks that no test can, and how to brief a builder and a reviewer. Read before reviewing a notebook or sending an agent to build one.

## References

- `docs/doctrine-updates.md`: "2026-11-14: A Notebook Tour, Held by the Suite" (adoption steps), "2026-11-16: Notebook Tour Correction" (rules from thirteen reviews), "2026-11-16: Notebook Tour Module" (the two leak channels). The adoption steps and the tour module's commits live there; this skill does not repeat them.
- `notebooks/tour_from_a_model_to_a_ranking.ipynb` and `notebooks/cases_how_a_ranking_goes_wrong.ipynb`: the hub's own pair.
- `tests/unit/test_case_notebook_module_port.py`: each rule of the case module shown failing alone in a built repo.
- The designing-clear-data-displays skill, for every figure; the verifying-claims skill, whose rule 3 is this skill's rule 6 applied to a cell; the maintaining-the-common-operating-picture skill, whose kinds of line are this skill's kinds of doubt.
