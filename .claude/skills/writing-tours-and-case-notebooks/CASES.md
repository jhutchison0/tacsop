# Case Notebooks

A case notebook is the depth notebook. It takes the rules that shape a repo's output and, for each, runs the rule a reasonable person would write first beside the rule the repo uses, with an assert stating how far apart they land. The third step is what a tour lacks: the reader runs the obvious code, sees the wrong answer, and then sees the repo's.

A case notebook keeps every rule in `TOURS.md`. This file adds what makes a case a case. `CONFIDENCE.md` holds the section every case notebook ends on.

## When a Repo Is Ready

- It has a tour. The cases link back to it and assume its path.
- It has rules whose obvious alternative changes what the product ships, on a committed fixture. A different internal value is not enough. Where the product ships more than one output (a report and an export), the case's heading and text say which one differs.
- A candidate counts when its naive rule is on record (a fix, a review finding, a probe that found a defect), or when it survives a reading of the repo's own format and design docs. If the repo's own doc states the rule in its first lines, the naive rule is one nobody who read it would write.
- A test that already holds the rule counts. A characterization test written for the notebook lets a case be built; it does not make a weak candidate count.

Three such cases make a notebook. **Two and a limit make a short notebook, and that is an honest result; so is "not ready".** Three is not the price of building, and five is a cap, not a target. A repo with no such rules has no case notebook, and that is a finding about the repo, not a gap in its documentation.

Count findings, not fix commits: one commit fixed three findings from a review. In the rollout no repo of thirteen came back "not ready", and one review ruled a five-case notebook padded by two: every regular expression in a parser has a wrong alternative and can take a test, so the gate as first written could not say no. The wording above is the repair.

## The Parts of a Case

Each case is a text cell under a `## Case` heading, then one code cell, then one short closing text cell.

| Part | Label | Says |
|---|---|---|
| Heading | `## Case N.` | The finding, as a sentence: "A raw number is not a utility". A reader who stops at the heading has the point. A known defect says "known defect" here |
| Question | `**Question.**` | One sentence a user of the output would ask |
| Fixture | `**Fixture.**` | The committed data the case runs over, small enough to print whole. The cell prints it before anything is computed |
| Naive | `**Naive.**` | The obvious rule, and why a reasonable person writes it |
| The repo's rule | `**The repo's rule.**` | The rule, and the function that applies it |
| Assert | in the code | A name beginning `naive`, computed by running the naive rule, and an assert that sets it beside the repo's answer |
| Source | `**Source.**` | Its kind, where the rule comes from, and the test that holds it |
| Closing | the cell after | How big the difference is, on the fixture and on the tour's own run; whether the wrong answer raises an error; which way the naive rule errs |

Most wrong answers raise no error, and saying so is the point of the case.

## The Naive Rule

**It is one a competent person would write**, named for what it is: `splitlines()`, a spreadsheet's `SUMPRODUCT`, min-max scaling, the textbook formula. A rule nobody would write proves nothing. Where two wrong rules come to mind, run both.

The best evidence that a person writes it is that one did. In order of strength:

1. A fix that needed a second fix: a recommended fix shipped and was replaced eleven minutes later.
2. The repo's own code before a fix.
3. The same rule still written elsewhere in the repo, in client code or a study script. Search every tracked file for the naive expression, other languages included, before a source says nobody wrote it. Two sources said so and were wrong.
4. A mutant that once survived. A mutant is a slip, not a belief: the text says why a person would write it.

**The cell runs it.** A naive answer typed as a constant, or read back from the line that wrote it, is a description of a wrong answer and not one. The test module refuses both.

| Where the naive rule lives | How to run it |
|---|---|
| A method the product calls | Restore the old line in a small subclass inside the cell |
| Inside a long function | Pass in the input the old line produced |
| A module-level helper called by name | A patch in a `with` block inside the cell |
| Code that cannot be recovered | Call today's code at the earlier moment or with the old input, and say in the source what the stand-in stands for |
| Another language | It cannot run here. The case says the rule is on record and latent, and asserts where it is written |

Keep a restored rule's expression order, and compare it with the old source by executing both over more inputs than the fixture: three maps agreed where half of five hundred differed in the last bit. A private name is allowed where the fix lives in it or the input arrives through it; the text says it is private, and the case still reaches the report through a public call.

Two cautions. Where a naive rule depends on the order rows come back in, fix the order with a small in-memory reader and say so. Where it reads the wall clock or the host's zone, set both clocks and assert the hours at which the two rules agree.

Where the repo gives a criterion and leaves the decision to the reader, the cell assembles the repo's answer from it. Say so.

## The Source

A case without a source is an invented example: it shows that an input can be built where two rules differ, which is true of almost any two rules. The source is a must. It opens with one of three kinds, so the reader knows how much weight the case bears.

| Kind | Means | Must carry |
|---|---|---|
| `Incident:` | The wrong rule is on record in this repo | A quotation from the record, in double quotes, saying what was seen and by what: a run, a reviewer's probe, a sentence of prose. The file or commit the quotation is in. The test that holds the fix |
| `Design:` | The repo chose its rule, and no wrong rule is on record | The code that applies the rule, the test that holds it, and the pinning commit where there is one |
| `Literature:` | The failure is known outside the repo | The reference, by author and year, and the test that holds the repo's rule |

**An incident quotes its record.** Open the record, read it, and quote what it says. Never characterise a record you have not opened. In one notebook three of four sources misdescribed their records while every assert passed: two said no run was on record beside a review that says "Verified live", and one said a page was shown to a person no record says opened it. The test module now finds each quotation in the file or commit message the source names. On first use the rule corrected every source it touched.

What the quotation cannot do: it proves the phrase is in the record, not that it supports the sentence around it. Say what the record does not establish as "not recorded", never as "did not happen". A quotation takes double quotes; backticks are for paths, commits, tests and code. A finding id is cited from the file it is in.

**Which kind, at the edges.**

| The case | Kind |
|---|---|
| A mutation table or a review pinned the rule before anyone got it wrong | `Design:`, citing the pinning commit |
| A review marked the rule for repair and a later decision deferred it | `Incident:` and a known defect |
| The wrong rule was a sentence of prose that gave the right answer on its input | `Incident:`, saying so |
| The wrong rule happened in a predecessor repo and this one holds the record | `Incident:`, saying it is recorded here and not re-run |
| The builder found the defect on this build | `Incident:`, quoting the task row the builder filed. This is circular and the source says so |

**Every kind names a test, and the test fails under the naive rule.** Swap the naive rule in, in a scratch copy, and run the cited test. One cited test existed and passed under the pre-fix code; it did not hold the rule. A rule no test holds gets its test first; a test that pins present behaviour and passes on first run is a characterization test, and the report says so.

A figure the cell cannot recompute names the file that recorded it, says what it counted, and is labelled "from the record, not re-run here".

Most cases in most repos are `Design:`. That is an honest label, and it tells the reviewer where to press.

## Four Shapes

| Shape | Heading | Use when | Held by |
|---|---|---|---|
| **Case** | `## Case` | An obvious rule gives a different answer | The test module |
| **Known defect** | `## Case`, the repo as the naive side | The repo's own rule is the wrong one today | The test module, and a filed task |
| **Limit** | `## Limit` | The repo cannot answer the question, and can say why | The test module |
| **Tradeoff** | a numbered section | No rule is wrong; the answer moves with a parameter | Review |

A **known defect** computes the repo's present answer under a `naive` name and the intended answer beside it; the text says outright that the naive side is the repo. Its pin asserts at the reported level, through the path the product takes: try one plausible fix in a scratch copy and report which pins failed, since a pin that still passes pinned something else. Fixing the defect fails the cell. Do not fix it; file the task the repo's rules ask for and put it at the top of the report. These are also known defects:

- Two rules where one was meant, even when the intended one is not chosen. The cell shows the candidates beside the present behaviour.
- A rule kept only by a notebook cell. If the product does nothing and a notebook compensates, the product has the gap.
- A case whose asserted difference passes through a defect reported elsewhere. The cell names it and marks the assert.

A **limit** carries `**Question.**`, `**What is not known.**` and `**What would settle it.**`, the two fields of a gap register row. Its cell asserts the present state, so it fails on the day the code changes. A limit recorded in a gap register can lift with no code change, so it names the gap and the register in backticks, and the test module fails the notebook once that row is not open. A sentence that a thing has not been counted, or cannot occur, needs the count wherever the cell can make it: one limit said a state had never been counted, and the notebook's own data held four. A limit on data nobody has asserts only what illustrates it.

A **tradeoff** shows the output across the parameter's range, as a table or small multiples on one scale, and asserts where the answer changes. It names who owns the choice. One builder probed for a tradeoff, found the output did not move past its standard error, and built none: a shape that is absent is reported as absent.

## Where to Find Cases

Cases are mined, not invented. Read these before proposing any, and list at least five candidates with the lens, the level, the kind and the test for each.

```bash
git log --oneline --grep='^\[fix\]'              # each fix is a rule the code once got wrong; read each body
git log --oneline -i --grep='^fix'
ls docs/reviews/                                 # findings, counted one by one; a fix that needed a second fix
grep -rln -i 'mutant' docs/reviews/              # a mutant that survived is a rule the suite could not tell from a slip
grep -n 'open' docs/gaps.md                      # each open gap is a candidate limit
grep -rn 'warnings.warn\|quarantine\|deprecated' src/   # the code marks its own doubtful outputs
```

Then sort by lens and by the level where the rules part. A first case notebook takes the construction lens and orders its cases along the tour's path.

- A fix log undercounts and can mislead. In a repo that is mostly another language it points away from the Python, and every case came from review files.
- Before dropping an incident because its test is in another language, look for its twin on this side.
- A crash is a bug report, not a case. Prefer a wrong answer that raised no error.
- Where a fixture has a generator, sweep its seeds and report how often the case's headline holds. A fixture tuned until it shows an effect says so, and the case claims what holds across draws.
- Ask the owner which wrong answer they have had to explain more than once. That case goes first.

## The Test Module

`tests/unit/test_case_notebooks.py`, version 0.7.2, holds fifteen things.  Set `OWN_DATA_PROBES` to map each own-data guard to a committed file. Copy it only into a repo that has a case notebook, beside `test_notebooks.py`; set `NOTEBOOK_DIR` and `TESTS_DIR` by meaning; say its version in any report. `tests/unit/test_case_notebook_module_port.py` shows each rule failing alone.

| Test | Fails when |
|---|---|
| `test_there_is_a_case_notebook_to_hold` | No `cases_*.ipynb` exists, so the checks would pass over nothing |
| `test_it_holds_at_least_one_case` | A file named for cases has no `## Case` section |
| `test_every_heading_is_one_the_module_knows` | A `## ` heading is not a case, a limit, a numbered section, the confidence section, the own-data cell or the closing links. A misspelled heading once hid a whole case |
| `test_it_says_how_sure` | No `## Confidence` or `## How sure` section, or no cell under it asserts anything |
| `test_every_section_states_its_parts` | A case or limit lacks one of its labels |
| `test_every_case_asserts_its_naive_answer_against_the_repos` | A naive name is typed in as a literal; no naive rule ran; or no assert sets a computed naive answer beside a second name |
| `test_every_limit_pins_the_present_state` | A limit's cell has no assert |
| `test_every_source_says_what_kind_it_is` | A source opens with none of the three kinds |
| `test_every_source_names_a_test_that_exists` | A source names no test, or one defined nowhere under `TESTS_DIR` |
| `test_every_file_a_section_names_exists` | A source or a limit names a path the repo does not hold |
| `test_a_limit_that_cites_a_gap_finds_it_open` | A limit names a gap whose register row is missing or not open |
| `test_every_incident_names_its_record` | An incident names no commit and no record file |
| `test_every_incident_quotes_its_record` | An incident quotes nothing, or a quotation is in no file or commit message it names |
| `test_every_commit_a_source_names_is_in_the_history` | A source names a commit this history does not hold |

| `test_the_own_data_branch_runs_over_a_committed_fixture` | No probe is named, a probe names a file the repo lacks or a guard the notebook lacks, or the branch raises on its fixture. Output is discarded and a failure is named by type only |

The two tests above that read git history skip, visibly, where it is missing or shallow. A scratch copy made for mutation is therefore a local clone, not an archive.

What it cannot hold, each left to review: whether the naive rule is plausible; whether the second name in the assert is the repo's answer; whether an assert rewritten to compare naive with naive hides beside an honest one; whether the cited test and the quotation are about this rule; anything inside the confidence section beyond one assert; what the own-data branch prints, since it proves only that the branch finishes on one committed file; a path named outside a source or a limit; a control character in a code cell.

## Review Questions

The full protocol is `REVIEWING.md`. The questions a builder should ask of each case before handing it over:

1. Would a competent person write this naive rule, and has anyone?
2. Did the naive rule run, and is the second name in the assert the repo's answer?
3. Does the cited test fail under the naive rule?
4. Does the record say what the source says it says?
5. Does the heading state the finding, and does the cell print its fixture and both answers as labelled rows?
6. Does the closing text say whether an error is raised, how big the difference is on the tour's own run, and which way the naive rule errs?
7. Does any sentence say how often, or claim what an outside party does, with nothing in the cell to check it?
