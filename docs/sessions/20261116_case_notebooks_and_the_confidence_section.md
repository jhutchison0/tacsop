# Session: Case Notebooks, the Confidence Section, and What the Suite Cannot See

**Date**: 2026-11-16 (Nidhogg, evening)
**Branch**: main
**Tags**: #session #doctrine #testing #decision-science #agents

**Documents**: [SKILL.md](../../.claude/skills/writing-tours-and-case-notebooks/SKILL.md), the draft skill and its five sidecars; [test_case_notebooks.py](../../tests/unit/test_case_notebooks.py), the case test file; [test_case_notebook_module_port.py](../../tests/unit/test_case_notebook_module_port.py), each of its rules shown failing alone; [cases_how_a_ranking_goes_wrong.ipynb](../../notebooks/cases_how_a_ranking_goes_wrong.ipynb), the hub's own case notebook
**References**: [doctrine-updates.md](../doctrine-updates.md), the three notebook entries of 2026-11-14 and 2026-11-16; [tasks.md](../tasks.md); [gaps.md](../gaps.md), rows G16 and G17
**Follows**: [20261114_notebook_tour_rollout.md](20261114_notebook_tour_rollout.md)
**Cites**: [designing-clear-data-displays](../../.claude/skills/designing-clear-data-displays/SKILL.md), [verifying-claims](../../.claude/skills/verifying-claims/SKILL.md), [maintaining-the-common-operating-picture](../../.claude/skills/maintaining-the-common-operating-picture/SKILL.md)

---

## Summary

The user asked what should follow the breadth tour, having seen a first depth notebook in `assay`: a case notebook, which runs the obvious rule beside the repo's and asserts the difference. The session wrote that practice down as a draft skill, built the hub's own case notebook and two displays, and then, at the user's direction, had the hub's agents build a first case notebook in thirteen sibling repos, each on an unpushed topic branch in a worktree, each reviewed by `code-reviewer` and fixed. Partway through, the user added a requirement: a notebook should say how sure its numbers are, at each level of the data. That became kernel rule 9 and a required section.

The main finding is about checking, not about notebooks. In every reviewed notebook the mechanical record was clean, and ten of thirteen reviews still held a Critical. Each was in a sentence, a label, or the branch the suite never ran.

| Measure | Value | How measured |
|---|---|---|
| Hub suite at session start | 585 passed, 1 warning | `.venv/bin/pytest -q` at `/session-start` |
| Hub suite at this record | 688 passed, 1 warning | `.venv/bin/pytest -q`, 2026-11-16 23:30 CST |
| Repos given a first case notebook | 13 | `ls -d` of the worktrees beside the morning file |
| Built, reviewed, fixed, and re-run by the lead | 9 | the lead's own runs, one per branch (Claims) |
| Reviewed, with a fix-up still running at this record | 4 | the agents' last reports |
| Reviews holding at least one Critical | 10 of 13 | each review's final message |
| Branches on a remote | 0 of 13 | `git branch -r --contains HEAD` in each worktree |
| Skill | 0.1.0 to 0.3.0, 1 to 5 sidecars | the files' frontmatter and `wc -l` |
| Case test file | 0.1 to 0.7.2, 5 to 15 rules | its docstring; its `def test_` lines |

Session start on this box pulled eight commits made on titanx earlier the same day. They have no session doc, though gap G14's closing pointer cites one.

---

## Work Completed

### 1. Reading `assay`'s case notebook

KB-graph: Follows chain and inbound references of `assay`'s case-notebook session doc, on its `home` branch → confirmed the pattern's five parts and its one test rule, and found the rule passed `assert naive == naive`; that became the hub test's first requirement.

The pattern was sound. Three weaknesses carried into the design: the test held little; four of five cases named no origin; one fixture per case said nothing of how often.

### 2. The draft skill

`writing-tours-and-case-notebooks`, in "Level 0 Drafts" in `SKILLS_FRAMEWORK.md`, so `scripts/adopt_doctrine.py` does not copy it. A pin failed when it was first listed in the propagated roster, which is how the Drafts section came to exist.

- **Kinds.** Tour for breadth, cases for depth. Walkthrough and problem set are named and not ruled on.
- **Three levels**, from the user: the data as it arrives, as it is handled, as it is reported. A library has all three: the arguments, the validated object, the returned value.
- **Three lenses**, from `assay`'s three planned notebooks: construction, validity, scope.
- **The source.** A case names where its rule comes from: `Incident:`, `Design:` or `Literature:`. An incident quotes its record.
- **The confidence section**, from the user: a table of doubts by level, each with a kind (measured, measured over an assumed range, estimated, not known, exact) and a size, and one doubt run through to the report.

### 3. The hub's case notebook and two displays

`notebooks/cases_how_a_ranking_goes_wrong.ipynb`: four cases, a limit, a confidence section. Its best case: withdrawing a dominated site changes the naive leader and moves nothing in the package. `passage_chart` and `slope_chart` were driven by failing tests and looked at as rendered. The confidence cell moves one site's flood record three years either way: the leader holds; second and third place swap, across a margin the ranking prints as 0.004.

### 4. The rollout

Builders were `python-prototyper`, reviewers `code-reviewer`. Each repo: build, review, fix-up, then the lead's own re-run of the suite or its named tests, two timezones, a second hash seed, a clean tree, no remote, no product file changed. One shared brief grew from 15 points to 135 as reviews returned.

Per-repo findings, the product defects the notebooks found, and the decisions for the owner are in a file beside the worktrees, outside every repository. They are not in this public repo.

### 5. What the reviews found that the suite did not

- A source said no run had shown a wrong page, beside a record that says "Verified live". Three of four sources in one notebook misdescribed their records.
- A confidence section's headline was the host's offset from UTC. Another's held on one block of thirty draws and on two of ten others.
- A closing sentence said seven items were in no settled order; most pairs were apart in the cell's own data.
- A limit said a state had never been counted; the notebook generated it four cells later.
- An own-data cell printed a score the product's own report withholds. Another printed three all-clears after reading nothing.
- An assert pinned an input the product never builds, and the product's own path did the opposite.
- A cited test passed under the naive rule it was cited as holding.
- One notebook was ruled padded by two cases of five. The gate as first written could not say no to a parser.

### 6. What the test file gained

Fifteen rules, each with a port test that shows it failing alone in a built repo. The ones the reviews forced: a heading the file cannot place fails; a naive answer must be computed, not typed or read back; a limit that cites a gap finds it open; the confidence section exists and asserts; an incident's quotation is found in its record; the own-data branch runs once over a committed file with its output discarded.

The quote rule corrected every source it touched on first use. The own-data rule catches a crash and cannot see a wrong line.

---

## Claims

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes | tested | `.venv/bin/pytest -q` → `688 passed, 1 warning`, 2026-11-16 23:30 CST, working tree of this commit |
| Each rule of the case test file fails alone | tested | `.venv/bin/pytest -q tests/unit/test_case_notebook_module_port.py` → `60 passed`, in the same run |
| Nine branches pass on the lead's own re-run | tested | per branch, the suite or its named tests, then the two notebook test files under `TZ=UTC`, `TZ=Asia/Tokyo` and `PYTHONHASHSEED=1`; last lines in the file beside the worktrees, section 2 |
| Those nine changed no product code | observed | per branch, `git diff <base>..HEAD --stat -- src` printed nothing |
| No branch is on a remote | observed | `git branch -r --contains HEAD` printed nothing in each of 13 worktrees, at the last PCC run |
| No private term is in the hub's uncommitted work | tested | `/pcc` check 7 extended to the changed and untracked paths: 0 files with hits, list present |
| Four branches are finished | not done | their fix-ups were running at this record |
| The whole suite passes in three of the nine (the ones with network, device or three-minute suites) | UNVERIFIED | the lead ran named tests there; the builders' and reviewers' whole-suite counts stand unrepeated |
| The hub's own case notebook and displays are sound | UNVERIFIED | no second reader has reviewed them; every other notebook of the rollout was changed by its review |
| Any case notebook opens correctly in a front end | UNVERIFIED | none was opened |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 2. Both were builders' confidence findings the lead relayed to the user as results before the reviews landed: a 384-minute gap between two sources, which was the host's timezone offset; and "first and second place survive", which held on one block of thirty draws and on two of ten others.

Three of the lead's own statements were wrong and the lead corrected them, so they are in neither count. The rollout's size was reported as twelve repos all evening; it is thirteen. Clock times were written beside the running notes as if measured; they were guesses, and one put the session past midnight when the machine's clock read 23:30. And the first draft of the hub's own case notebook stated two figures its asserts then refuted.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Write the practice down as a skill, reversing the morning's "an entry, not a skill" | the user | Stated in conversation; the rule list had outgrown an entry |
| A pilot in one repo, a pause to update the skill, then the rest | the user | Stated when asking for the rollout |
| Add the confidence section, partway through | the user | Communicating uncertainty is the decision-support work; a notebook is a place to force the question |
| Keep the skill out of propagation as a draft | the lead | Evidence was one author on one day; the pin in `test_adopt_doctrine.py` made the choice explicit |
| The source is a must, with three declared kinds | the lead, agreed by the user | A case without one is an invented example |
| No new figure code in sibling repos; each builder proposes one | the lead | Adding a drawing dependency to a dozen repos overnight is the owner's call |
| No product code changed anywhere; a defect is pinned and filed | the lead | The notebooks were the task; fixes are each owner's |
| A second timezone and hash seed run by hand, not by `test_notebooks.py` | the lead | That file is pinned at `cb7617d` by two sent entries; changing it is a correction entry |
| Hub work committed locally and not pushed | the lead | `/session-end` ran from a hook with the user away; a push publishes |
| Per-repo findings kept outside this repo | the lead | Output goes to the repository that owns the sensitivity of its input |

---

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS, with a flag | The case test file grew from 5 rules to 15 in one evening, each added for a fault a review showed. The brief reached 135 points and overlapped itself; the skill is its consolidated form. |
| **Shift-Left Testing** | PASS, with three exceptions | The displays and every rule of the case test file were driven by a failing test. Not seen failing first: the label-spreading fix, one scorer test, and a set of port tests written after the rules they cover. Source edits made through Bash left no audit entry (gap G2). |
| **Config-Driven** | PASS | The hub notebook's model and alternatives are the tour's YAML fixtures. |

Deviations caused by this session's agents: two builders wrote a script to one path in a shared scratchpad, and one's run changed a file in the other's worktree, which that builder restored from the index. Later agents each had their own scratch directory and mutated a clone.

---

## Next Steps

1. The user reads the morning file beside the worktrees: its opening items first, then the table of thirteen branches, then the decisions.
2. The four fix-ups still running are finished and re-run by the lead, or reported as left.
3. Three finished branches carry an older copy of the case test file, without the quote rule or the own-data rule. Bring them level, or record that they were not.
4. One notebook built from the skill's six files alone, with no brief, and reviewed (gap G16), before the skill is called 1.0.0.
5. `code-reviewer` reviews the hub's own case notebook and displays.
6. The user decides whether the hub is pushed, and whether the two 2026-11-16 doctrine entries go to this box's consumers.

---

## Addendum, 2026-11-17: all thirteen finished, three levelled, and a rule that was wrong

Written after the last agents returned, shortly after midnight. The Summary's table shows the state at 23:30 on 2026-11-16; this section supersedes its rows on branches.

| Measure | Value | How measured |
|---|---|---|
| Hub suite | 688 passed, 1 warning | `.venv/bin/pytest -q`, after the last skill edit |
| Branches built, reviewed, fixed, and re-run by the lead | 13 of 13 | the lead's own runs, one per branch; last lines in the file beside the worktrees |
| Branches clean, on no remote | 13 of 13 | `git status --porcelain` and `git branch -r --contains HEAD` in each worktree, one command over all thirteen |
| Branches on the current test file (0.7.2) | 6 of 13 | `grep 'Module version'` in each; the rest carry 0.6.0 to 0.7.0 |
| Reviews holding a Critical | 10 of 13 | each review's final message |
| Skill | 0.3.0, five sidecars, 674 lines | `wc -l` |

### The levelling pass

The three earliest branches predated the rule that an incident quotes its record. A read-only probe showed that was the only rule of the current test file each would fail, so each got a short pass scoped to it and to the own-data probe. In all three, opening the records corrected at least one sentence the builder had written. In two, the own-data probe failed on first use and found a real fault. The other seven branches on older copies were not levelled: each passed the rules of its day.

### A rule that was wrong

The standing rule for one sibling repo was "run the unit tests only; the integration suite makes live requests". All evening that was read as "no network". The lead's last re-run blocked and counted every socket call and found six existing unit tests looking up a public weather service, untouched by the branch; the suite passes either way because the code swallows the refusal. So the unblocked runs of that folder during the session, by a builder, a reviewer and the lead, very likely sent requests to that service. A second repo's suite does the same from one test, found the same way by its reviewer.

The lead had told the user that the live-request suite was never run. That was true of the integration suite and was not the whole truth. The lesson is in `REVIEWING.md`: verify "no network" by counting blocked socket calls, never by a folder name, a marker, or a passing suite.

### What the last reviews added

- A case asserted the field a fix had made right, while two fields beside it still printed the naive answer. Search the whole output.
- A direction was stated as settled, quoted accurately from a design doc, and was wrong: the same repo's gap register lists the claim as undecided.
- One control on one field became a sentence about a class of input, and it was the sentence telling a reader a defect was small.
- A user's own configuration reached a product through a cell that called it directly.
- An assert on a glob of the working tree failed with a clean tree, where ignored files land.
- In every repo where the quote rule was applied, it changed at least one sentence.

### Claims, at the addendum

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes | tested | `.venv/bin/pytest -q` → `688 passed, 1 warning`, working tree of this commit |
| Thirteen branches are finished and pass the lead's re-run | tested | per branch, the suite or its named tests and the two notebook test files under two timezones and two hash seeds; in the two repos whose suites reach the network, with socket calls blocked and counted |
| Thirteen branches are clean and on no remote | observed | one command over the thirteen worktrees: `dirty=0 remote=0` on every line |
| No product code changed in any of them | observed | per branch, `git diff <base>..HEAD --stat` over its source folders printed nothing |
| No request left this machine during the session | REFUTED | the unblocked unit-test runs in one repo; see "A rule that was wrong" |
| The whole suite passes in every branch | UNVERIFIED | in five the lead ran named tests only; the builders' and reviewers' whole-suite counts stand unrepeated |
| The hub's own case notebook and displays are sound | UNVERIFIED | no second reader |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 2, as above.

The lead's own corrections now number four: the rollout's size, the clock times, the two figures in its own notebook draft, and "the live-request suite was never run", which the lead's own last re-run showed was not the whole truth.

### Next steps, replacing the list above

1. The user reads the morning file beside the worktrees: thirteen opening items, the table, the per-repo entries.
2. The user rules on the thirteen branches, and on the hub's five unpushed commits.
3. One notebook built from the skill's six files alone, with no brief, and reviewed (gap G16).
4. `code-reviewer` reviews the hub's own case notebook and displays.
5. `test_notebooks.py` gains runs under two timezones and two hash seeds, as a correction entry.
6. Seven branches carry an older copy of the case test file. Level them when each is merged, or accept them as they stand.
