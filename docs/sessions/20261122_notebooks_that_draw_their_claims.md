# Session: Notebooks That Draw Their Claims

**Date**: 2026-11-22 (Nidhogg, evening into night)
**Branch**: topic/notebook-displays-0-4
**Tags**: #session #doctrine #figures #notebooks #agents #decision-science

**Documents**: [DISPLAYS.md](../../.claude/skills/writing-tours-and-case-notebooks/DISPLAYS.md), [CONFIDENCE.md](../../.claude/skills/writing-tours-and-case-notebooks/CONFIDENCE.md), [REVIEWING.md](../../.claude/skills/writing-tours-and-case-notebooks/REVIEWING.md); the display skill's [SKILL.md](../../.claude/skills/designing-clear-data-displays/SKILL.md), [RULES.md](../../.claude/skills/designing-clear-data-displays/RULES.md), [REVIEWING.md](../../.claude/skills/designing-clear-data-displays/REVIEWING.md), [ADOPTION.md](../../.claude/skills/designing-clear-data-displays/ADOPTION.md)
**References**: [the second review](../reviews/20261122_display_skill_second_review.md); [the doubt audit](../reviews/20261122_display_doubt_audit.md); [the improvement proposal](../plans/20261122_display_skill_improvement_proposal.md); [gaps.md](../gaps.md), rows G18 and G19; [tasks.md](../tasks.md)
**Follows**: [20261117_case_notebook_update_in_detail.md](20261117_case_notebook_update_in_detail.md)

---

## Summary

The notebook skill told builders not to draw, and they did not. The user saw it in a sibling repo's notebooks: good cases, and almost nothing but text and monospace tables. This session reversed the rule, built the first display kit in that repo, drew eight notebooks from it, and had three agents read the figure doctrine a second time.

The user set the aim: a notebook is a tool for telling a reader something, with words, numbers and pictures together, as Galileo set a drawing of Saturn inside a sentence. Show raw, staged and production data, and show results, confidence and uncertainty. Grey is fine; colour where it adds a layer, as flame for a plan that burns.

Nothing is pushed and nothing is merged. Both branches wait for the user's eye on the figures.

| Measure | Value | How measured, 2026-11-22 |
|---|---|---|
| Hub commits on the topic branch | 3 before this doc's commit | `git log --oneline main..HEAD` |
| Hub suite | 693 passed, 1 warning | `.venv/bin/pytest -q` |
| Sibling commits on its topic branch | 12 | `git log --oneline main..HEAD` there |
| Sibling fast suite | 543 passed | `.venv/bin/pytest -q -m "not slow"` there |
| Display kit tests | 146 passed | `.venv/bin/pytest -q tests/unit/test_displays.py` there |
| Notebooks that draw | 8 of 8, 47 display calls | a count of kit calls in each `.ipynb` |
| Notebook lines added and removed | 1,720 and 83 | `git diff main --numstat -- notebooks` there |
| Either branch on a remote | no | `git ls-remote --heads origin` there printed no such branch; the hub branch was never pushed |

---

## Work Completed

### 1. Why the notebooks drew nothing

`DISPLAYS.md` at 0.3.0 held three rules that added up to "print a table". A figure cost a new package function and its tests. The line of twenty numbers was applied to the summary, so twenty thousand simulated nights printed as two means passed as "two numbers". And nothing asked for a picture when the claim was about a shape. The file recorded the result itself: no repo of the thirteen-repo rollout gained a figure.

### 2. The display kit, in a sibling repo

One module of tested displays, so a figure costs a call. It began with five and ended with eight: a unit chart, points on one scale, simulated outcomes counted by group, a region map, lines over an input, a word-sized line set inside a sentence, a payoff table with best replies underlined, and a two-move game tree whose path of play comes from the solver. Colour goes to a name drawn on the figure, and three colours imitate what they mark: flame, water, blood.

The kit was built test-first in slices, with three slips recorded under Pillar Compliance. Its tests hold structure: one mark per datum, one scale, labels that do not overlap by the renderer's own extents. Each round of review added tests for what a render showed and no test had held.

### 3. Eight notebooks

The lead drew the first notebook. Five `python-prototyper` agents drew the other seven in parallel, each confined to its own files, each told to look at every render and to negate each new assert. Two more agents then applied the doubt audit's checklist to those seven and cut prose a figure had replaced. The lead rendered all eight in a real kernel and looked at the sheets after each round.

### 4. Three second readers

The user asked for the roster's agents to read the display skill again: would Tufte approve, are the skills linked, can they improve.

| Reader | Output | What it found |
|---|---|---|
| `proposer` | [the proposal](../plans/20261122_display_skill_improvement_proposal.md) | Citations checked one by one; colour, tables and annotation missing from the skill; "drawn whatever the count" overcorrects |
| `decision-scientist` | [the doubt audit](../reviews/20261122_display_doubt_audit.md) | An interval of the mean printed beside a spread of outcomes and not named, 71 times narrower at 5,000 draws; three doubts that need three marks; a margin given in one input of two |
| `code-reviewer` | [the second review](../reviews/20261122_display_skill_second_review.md) | 0 Critical, 12 Warnings, 7 Notes. The skill kept Tufte's sentence that sends small data to a table and declined the one beside it that asks a graphic to carry a large data set |

Two readers split their reports: findings about the sibling repo's figures went to that repo, and only the doctrine side came here.

### 5. What changed in the skills

**Notebook skill, 0.4.0, still a draft.** `DISPLAYS.md` is rewritten: draw a claim about a shape, with its table beside it; a kit makes a figure cost a call; each level owes one look; the confidence display shows how far the fixture sits from the place where the answer changes; a row of draws states the range that holds 95% of them apart from the interval of the mean; words and pictures sit together; colour names one thing and imitates it. `CONFIDENCE.md` gains the same distinctions. `REVIEWING.md` gains a step for each figure. Kernel rule 7 is reworded.

**Display skill, 1.2.0.** Colour is a distinction under rule 3, with a greyscale test. Every number in a title is on the figure. An annotation touches its mark. A table is a display, sorted by the claim's value. A doubt has a lie factor. "Not a density floor, and not a licence for empty space." The pre-question now counts the numbers behind a claim.

### 6. What the reviews changed in the kit

Each item below was a fault a reviewer or a builder found in a render, and each now has a test.

- A row of draws printed "95% interval" without saying it was the mean's.
- A game tree's note said grey means a reply not chosen, and two refused replies were drawn in colour.
- A map's lines were named "wins above", and 14 of its 81 marks contradicted the names.
- A colour took a grey's place in the ramp and printed as its neighbour's grey.
- Labels lay over marks and over other labels; a tree's annotation floated in a far column.
- Two figures were more than half empty rows.

---

## Claims

Each row was checked after the last change to the thing claimed. Sibling-repo rows were measured in that repo's checkout.

| Claim | State | Evidence |
|---|---|---|
| The hub suite passes with the skill changes | tested | `.venv/bin/pytest -q` printed `693 passed, 1 warning`, after the last skill edit and before this doc's commit |
| The gap register's tests pass with G18 and G19 added | tested | `.venv/bin/pytest -q tests/unit/test_gaps.py tests/unit/test_state_block.py` printed `65 passed` |
| The sibling's fast suite passes with all eight notebooks | tested | `.venv/bin/pytest -q -m "not slow"` printed `543 passed` at `5fbb02e` |
| The kit's own tests pass | tested | `.venv/bin/pytest -q tests/unit/test_displays.py` printed `146 passed` at `5fbb02e` |
| The sibling's lint, format and strict types pass | tested | `ruff check .` printed `All checks passed!`; `mypy` printed `Success: no issues found in 26 source files`, at `5fbb02e` |
| Every notebook runs in a real kernel and yields its figures | observed | An nbclient run of each of the eight wrote 47 PNG and HTML outputs outside the repo, before the last kit sizing change; one notebook was re-run after it |
| No private term is in either branch's unpushed commits | tested | `/pcc` check 7 ran in both repos and printed no FAIL line, before the final commits; the list is at the usual path on this machine |
| Neither branch is on a remote | observed | `git ls-remote --heads origin` in the sibling printed no display branch; no push command was run in either repo this session |
| The sibling's slow suite passes | UNVERIFIED: not run this session; CI has not seen the branch |
| The seven later notebooks read well to a person | UNVERIFIED: gap G18; no person has opened one |
| Tufte's colour passages say what rule 3 attributes | UNVERIFIED: gap G19; the books were not open to any agent |

Overclaims the user caught this session: 0

Overclaims a reviewer caught this session: 6. `DISPLAYS.md` stated a test count that was stale within the hour. It said a kit colour is darker than the grey beside it, which a four-group chart refutes. The kit printed an interval of the mean as "95% interval" beside outcomes. A tree's note called refused replies grey while two were drawn in colour. A map named its lines "wins above" against 14 of its marks. And a commit message of mine, `26a6f67`, says "after three second readers" when the third had not yet reported.

Two corrections were my own and are in neither count. I added a line to the verifying-claims skill and reverted it before committing, since that skill is held until OVERWATCH task 2d. I ran `git stash` and `git stash pop` in the sibling checkout while two agents were editing notebooks there, against the rule I had given them; the pop restored every file and the suite passed afterwards.

---

## Key Decisions

| Decision | By | Rationale |
|---|---|---|
| Reverse the notebook skill's default: draw a claim about a shape | the user, on the lead's recommendation | Thirteen repos drew nothing under the old text |
| Colour where it adds a layer, as flame for burning | the user | Grey is the field; a colour names and imitates one thing |
| Update the other notebooks the same night, and have the roster's agents read the display skill again | the user | "Dig deep" |
| A cap of two colours in a notebook | the lead | The house's own, marked so in the text; the user has not ruled on it |
| Change the ambient pre-question in `CLAUDE.md` and `ADOPTION.md` | the lead, on the second reader's finding | The old sentence is the gate that stopped the drawing, and it loads in every session and every consumer; the user has not seen the new wording |
| Leave the propagated display skill untouched in the sibling repo | the lead | It arrives by a doctrine cycle; only the draft notebook skill was copied by hand |
| Keep sibling-repo findings out of this repo | two reviewers, by the scope matrix | The hub is public and that repo is private |
| No push, no merge | the lead | The user asked to see figures first, and the sibling's rule wants CI and a second reader before a merge |

---

## Pillar Compliance

- **Simplicity First.** The kit is one module of about 1,070 lines, and two of its eight displays import that repo's solvers, so the general displays cannot be ported apart yet. The notebooks gained 1,720 lines and lost 83: the figures were added on top of the prose, and `DISPLAYS.md` says to shorten what a figure replaces.
- **Shift-Left Testing.** Three slips, all the lead's: the region map's first cut, and two small fixes, were written with their tests in one step and not red first. The audit hook never fired for the sibling repo, since the session was rooted here, so that repo holds no audit-log entry for the kit.
- **Config-Driven.** Colours and layout numbers are constants in the kit, and each notebook's assumed grid is an inline list marked as assumed. None is a model input. Whether a palette belongs in config is the user's call.

---

## Next Steps

1. The user runs one notebook in a front end and looks at the figures (gap G18), then rules on the five items in the Focus: the figures, the pre-question's new wording, saved outputs, the kit's home, the colour cap.
2. A `code-reviewer` pass over the seven later notebooks, by `REVIEWING.md` step 10, in the sibling repo. None has had a second reader.
3. The sibling's slow suite and CI, before its branch merges by its own rules.
4. The doctrine entry for display skill 1.2.0, drafted as breaking, before the next cycle.
5. The three citations checked against the books (gap G19).
6. The kit's open items, listed in the task of that name.
