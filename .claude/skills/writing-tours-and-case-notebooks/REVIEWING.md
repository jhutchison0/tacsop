# Reviewing a Notebook, and Briefing an Agent

A notebook is built by one reader and checked by a second. This file is the second reader's protocol, and the brief for anyone sending an agent to build or review a notebook in another repo. It exists because of what the rollout showed: the suite held every notebook, and reviews still found faults in most, including Criticals.

## What Only a Second Reader Finds

| The fault | How a reviewer finds it |
|---|---|
| A sentence the assert under it does not support | For each section: would the assert fail if the sentence were false? |
| A source that misdescribes its record | Open every commit, file and test a source names; compare the source's words with the record's |
| A cited test that does not hold the rule | Swap the naive rule in, in a scratch copy, and run the cited test. It must fail |
| An assert that passed by sample luck | Re-run the cell on a second, disjoint block of draws; sweep a fixture's generator over its seeds |
| A number that belongs to the machine | Two timezones, two hash seeds, a shuffled row order, a faked clock |
| A fault in the own-data branch | Run it by hand on committed fixtures and on one input the product refuses |
| A naive rule nobody would write, or one never run | Read it; ask who wrote it; check it against the code before the fix |
| A defect the builder reported | Reproduce it with a probe that can fail |

## The Protocol

A reviewer writes one file, the report, inside the repo that owns the notebook, and commits it alone. Each step is reported with its command and its output.

1. **State on arrival.** `git status --porcelain` is empty; the head is the one named.
2. **The builder's claims, re-run.** The suite on the clean committed tree. In a repo with network, device or hardware tests, only the tests named in the brief.
3. **Negation.** Every assert, every conjunct of an `a and b` assert, every link of a chained comparison, one at a time, in a scratch copy. Count asserts from the syntax tree. Report survivors, and report the count as a floor.
4. **Hermeticity.** The notebook's tests under `TZ=UTC` and `TZ=Asia/Tokyo`; under `PYTHONHASHSEED=0` and `=1`, with the printed output diffed; with rows shuffled where a store or a set is read; under an inherited `GIT_DIR` where a cell runs `git`. Then twenty runs, as a count.
5. **Each case.** The questions in `CASES.md`. Open every record a source names. Check a restored pre-fix rule against `git show <commit>^`, line by line and by executing both. Swap the naive rule in and run the cited test.
6. **Each sentence.** A word that says how often; "nothing else changed"; a claim about when a slip is invisible; a claim about what an outside party does; a sentence about which settings the notebook survives. Each has a count or an assert, or it is a finding.
7. **The confidence section.** `CONFIDENCE.md`, row by row: is each a real doubt at that level, with an honest kind and a size? Was the repo searched before each `not known`? Does the cell follow the doubt that could change a decision, and name it? Does the result belong to the method or to the fixture? Would a decision scientist accept how the doubt is stated?
8. **The own-data cell.** Could it execute, publish, fetch, or mis-score what a reader gives it? Does it print anything the product's report withholds, or anything from the reader's data that the repo's rules forbid? Run it.
9. **Defects.** Confirm or refute each with a probe that can fail. For a known-defect pin, try one plausible fix and see whether the pin fails.
10. **Readability.** Would a reader new to the repo get each case's point from its heading and its table alone?

Findings are Critical, Warning or Note, each with the cell, the evidence and the fix. A result that differs by machine is a Critical. So is a notebook that fails intermittently, a number the product's report withholds printed by the own-data cell, and a private or real-world term in a public repo. The report ends with a verdict (merge, merge after fixes, do not merge) and a section on where this skill or the test module was wrong, silent or too strict.

## Briefing an Agent

**Where it works.**

- In a worktree outside the tree that propagation discovery scans, on a topic branch, unpushed. Never the owner's checkout.
- In its own scratch directory, named for the repo and the role. Two builders sharing a scratchpad wrote a script to one path, and one's run changed a file in the other's worktree.
- **It mutates a scratch copy, never the worktree**: a local clone, so history is there, with the copy's source first on the path and bytecode writing off. Nothing in the worktree changes, so there is no restore step.
- It removes what it creates. A cleanup that is refused is reported, not worked around.

**What it may run.**

- `--python` takes an absolute path or one starting with `./`; use the repo's own setup interpreter.
- Where the repo has network, device or hardware tests, name the test paths it may run. A marker that claims to exclude them may not.
- No outside lookup of a fixture value, a standard, or how another tool behaves.
- A permission refusal is reported and left. A reviewer may run what a builder could not only after showing from the code that it is safe; nobody routes around a refusal.

**What it must not change.** Product code. A defect is pinned, filed as the repo's rules ask, and put at the top of the report.

**What it reports.** The result (built, or not ready); each command with its last line; the candidate table with what was dropped and why; the cases; defects; the confidence table; the figure it would add; where this skill did not fit; questions for the owner, each answerable in a line. It leads with what a second reader should check, not with its negation count.

**Order of work.** Read the repo's own rules; mine candidates and count them against the gate; take the newest `test_notebooks.py` alone as a first commit; copy `test_case_notebooks.py` and see it fail; write any missing test first; build; run the own-data branch by hand; break it; run the suite after `git add`, since a tripwire may read tracked files; re-copy the test modules before the final run and say their version.

## For the Lead

- The lead re-runs each finished branch itself: the suite or its named tests, two timezones, two hash seeds, a clean tree, no remote, no product file changed.
- A builder's finding is unconfirmed until its review lands. Two confidence findings relayed as results were wrong.
- Per-repo defects go to the repo that owns them, and to a file outside every repo. The public hub holds only lessons that name no private thing.
- **Verify "no network" by counting blocked socket calls.** A rule inherited from an earlier session ("run the unit tests only") was taken as "no network" all through the rollout and was wrong; the lead's last re-run found it.
- **Read before running** in a repo that drives hardware: every construction in the notebook, for the mock setting passed by name.
- **The lead's own running notes are claims too.** The rollout's size was misreported all evening, and clock times were written as if measured.
- The brief grows as reviews return. It reached 135 points and overlapped itself; this skill is its consolidated form, and a builder should need only the skill. Builders re-read it at the end, not only at the start, and say which version of each test module they copied.
