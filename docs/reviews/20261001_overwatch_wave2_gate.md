# Review: OVERWATCH Wave 2 Gate, Tasks 2a to 2c

**Author**: code-reviewer
**Date**: 2026-10-01
**Type**: Code review

**Subject**: `topic/overwatch-verifying-claims` at `f100c2b`, against `main` at `b1c3e36`. In scope: `ef5b488`, `4b11ec3`, `d2cdaf8`, `cbd2ef5`, `1edf0d4`, `d1614fc`, `f100c2b`. Out of scope: the WHETSTONE capture-point commits, the merge `2783d6e`, and task 2d. This gate covers 2a to 2c only and cannot close Wave 2.

## Verdict

**GO-WITH-FIXES** for tasks 2a to 2c: 1 Critical, 16 Warning, 15 Suggestion.

All three Standards hold by my own count. The suite passes: 421 with and without `CI=true`. The defects are in what the text tells a model to believe and do:

- One sentence in `SKILL.md` states a safety guarantee that the tripwire's own doc denies (C1).
- The ambient block in `CLAUDE.md` says a plan is not a claim, and the venv incident is a plan (W1).
- Two probe rows hold while the claim is false, reproduced in scratch repos (W2, W3).
- The seven commit messages and the Status Log entry carry 0 `Evidence:` lines for 41 claims (W13). Of those claims, 30 hold, 1 is refuted in part, and 10 cannot be verified.
- The tests kill every mutant the caller named and 25 of 46 overall. They do not pin the parenthesized elements of 2a's Standard (W14).

Fix C1, W1 to W4, W6, W7, and W9 before the 2d replay runs: 2d measures this text. The rest can land before merge.

## What I ran

| Check | Command | Result |
|---|---|---|
| Suite at `f100c2b` | `.venv/bin/pytest -q`; then with `CI=true` | `421 passed, 1 warning`, exit 0, both ways, Python 3.12.13 |
| Suite at `main` | same, on a `git archive main` export in scratch | `403 passed, 1 warning`, exit 0 |
| The 18 doc-pin tests on 3.11 | uv-managed `python3.11 -m pytest`, no conftest, no plugins | `18 passed`, Python 3.11.15 |
| Mutation | 47 mutants on scratch copies, one per run | 25 killed, 22 survived (1 equivalent) |
| Red check | each commit's test file on its parent's tree | 5, 2, 2, 4, 1, 2 failures |
| Probes | every command in the probe table that has an object here | section 2 |
| PCC check 5 | both blocks, verbatim | 0 MISSING, 0 MISSING-DIR |
| D6 | 39 search strings over every in-scope file and message | 0 names |

UNVERIFIED: the full suite on Python 3.11. No 3.11 venv exists (`ls -d .venv*` prints `.venv`), and package-manager commands were outside my rules.

## 1. The Standards, by my own probes

| Standard | Probe | Output | Met |
|---|---|---|---|
| 2a: under 110 lines | `wc -l SKILL.md` | 102 | Yes |
| 2a: at most 6 kernel rules | numbered lines under `## The Kernel` | 6 (`SKILL.md:27-32`) | Yes |
| 2a: one probe per claim type | body rows of the Probes table | 7 (`SKILL.md:51-57`) | Yes |
| 2b: six pairs plus the slip | `## N.` sections in `EXAMPLES.md` | 7, then one clean report | Yes |
| 2b: 11 claimed, 12 measured | `EXAMPLES.md:101`, `:104-105` | present | Yes |
| 2b: no work-system names | section 6 | 0 names in 39 strings | Yes |
| 2c: kernel in `CLAUDE.md` | `diff` of `SKILL.md:27-32` and `CLAUDE.md:65-70` | identical | Yes |
| 2c: Claims table in `/session-end` | `session-end.md:62`, `:66-73` | present | Yes |
| 2c: sequenced after the capture point | reflog: `d565df9` 11:02:25, merge `2783d6e` 12:51:17, `d1614fc` 12:52:25 | in order | Yes |
| 2c: reviewer line, non-author review | `code-reviewer.md:43`; this report | present | Yes |
| 2c: four registrations | `SKILLS_FRAMEWORK.md:211`, `:424`; `.claude/README.md:51`; `CLAUDE.md:61` | present | Yes |
| Sidecar count | `ls .claude/skills/verifying-claims/` | `EXAMPLES.md`, `SKILL.md`: 1 sidecar, as both registries say | Yes |

The elements 2a lists in parentheses are all present in their rows, with two notes. The Tests row lost "This turn's" in `d2cdaf8`; the words now live in rule 2 and in the state table (`SKILL.md:39`). The Standard says "one read-only probe per claim type", and the Tests probe runs code; trap 4 admits it and then overstates the cover (C1).

## Findings

### Critical

**C1. `SKILL.md:64` states a guarantee the tripwire does not give.**
The line reads: "Rule 6 holds for them through the test tripwire". Rule 6 is "they never write to the system they check". `ISOLATION.md:71` lists "Overwrites and moves" under What the Tripwire Cannot See: `open(path, "w")` raises no event. The plan says the same at lines 31 and 103. D10's incident for this rule was a write into a production cache, not a delete. The tripwire is also armed only where a repo registers it: `tests/isolation.py` exists in 0 of the 15 sibling repos I surveyed.
Why it matters: a model told that rule 6 is covered runs a suite against real data and believes writes are stopped. This is the skill's own failure shape, a safety claim with no evidence behind it, in the file that teaches the rule.
Fix, same line count: "**Tests are the one probe that runs code**, so rule 6 does not hold for them. The test tripwire (`shift-left-testing/ISOLATION.md`), where a repo arms it, stops deletes and outbound connections; it does not stop overwrites. Run tests only where their writes cannot reach real data."

### Warning

**W1. `CLAUDE.md:72` exempts the shape of incident 3.**
The closing line says "A plan, an opinion, or a diff shown in the same message is not a claim." `EXAMPLES.md:43` shows the venv incident as a plan ("so I'll create its venv from scratch"), and `EXAMPLES.md:50` says so: "it is a plan resting on a belief nobody checked". `SKILL.md:11` covers it; the ambient text does not. A model that reads only `CLAUDE.md` gets rule 1's "an absence is a claim too" and, eight lines later, an exit for plans. The proposer warned that the 2d turn for this shape "is probably a planning sentence".
Fix: "A plan, an opinion, or a diff shown in the same message is not a claim. The belief a plan rests on is one: check it before you act." Change `SKILL.md:9` to match.

**W2. The Pushed row holds while the work is not pushed (`SKILL.md:52`).**
Refinement 1 took the clean-tree test away from push claims. Nothing replaced it. In a scratch clone with one uncommitted edit:
Evidence: `git rev-parse HEAD` → `2c05845a...`; `git ls-remote origin main` → `2c05845a...	refs/heads/main`; `git status --porcelain` → ` M f.txt`
The row's "Holds when" is true and the edit is on no remote. This is the common push overclaim: a commit that never happened.
A second hole: `git ls-remote origin <branch>` matches by path suffix. With `main` deleted on a scratch remote and `feature/main` present:
Evidence: `git ls-remote origin main` → `afdb468b...	refs/heads/feature/main`; `git rev-parse HEAD` → `afdb468b...`
One line prints and the SHAs match. The same form is in the Mirror, Merged, and Deployed rows.
Fix: write `refs/heads/<branch>` in all four rows. Add to the Pushed row: "and `git status --porcelain` lists no file the claim covers". `git ls-remote --exit-code` exits 2 on no match here, which gives trap 1 a status to read.

**W3. The venv row certifies "absent" from one name pattern (`SKILL.md:55`).**
"`ls` finds nothing: absent" is false for any venv not named `.venv*`. In scratch, with venvs at `venv/` and `envs/gpu/`:
Evidence: `ls -d .venv*` → `ls: cannot access '.venv*': No such file or directory`, `exit=2`; `find . -maxdepth 3 -name pyvenv.cfg` → `./venv/pyvenv.cfg`, `./envs/gpu/pyvenv.cfg`
Absence is the costly direction: the incident was a rebuild of something that existed.
Fix: lead the probe with the `find`, and word the result "none found under this directory", not "absent".

**W4. Four specimens break the table or the kernel they illustrate.**
- `SKILL.md:74` and `EXAMPLES.md:61` show a tests-pass `Evidence:` line with no Python version. The row at `SKILL.md:54` requires one, and 2a's Standard names it.
- `EXAMPLES.md:15-16` claims "(deployed)" on a timer listing and a clean tree. The Deployed row (`SKILL.md:57`) and the state table (`SKILL.md:40`) also require the remote SHA to equal the local one.
- `EXAMPLES.md:32` and `EXAMPLES.md:104` name no state. Rule 1 says to name it.
A model learns the format from the specimens before the table.
Fix: add `.venv/bin/python -V` → `Python 3.12.13` to both lines; add the two SHA probes to pair 1; add "(observed)" to the two claims.

**W5. Pair 7's `Evidence:` line does not reproduce (`EXAMPLES.md:105`).**
The pair is labeled real. Re-run at this HEAD:
Evidence: `wc -l tests/conftest.py` → `16 tests/conftest.py`; `git show 17db809:tests/conftest.py | wc -l` → `12`
The commit message of `4b11ec3` uses the pinned form; the example does not. A reader who re-runs the skill's showcase line gets a different number.
Fix: pin the ref in the example, or date it ("measured 2026-09-30; the file has grown since"). Either one teaches that an `Evidence:` line names the ref or the time it was taken.

**W6. The skill gives two answers on a blocker with no attempt.**
`SKILL.md:66` says a probe that cannot run ("no auth, no network, another machine") is a blocker. `SKILL.md:79` says to "name the machine or the access" when there is no error to paste. `EXAMPLES.md:79` says: "'I have no access', with no attempt, is a skipped check." Rule 4 adds "run it". Read together by a model that wants to comply, the text says to try the production command to prove it is refused. Where the attempt can write, page someone, or meet a permission prompt, that is the wrong push.
Fix: reword `EXAMPLES.md:79`: "'I have no access', with no error and no named credential, is a skipped check." Add to `SKILL.md:66`: "A check the user or the harness declined is a blocker too; do not retry it another way."

**W7. `SKILL.md:83` says a report with no `UNVERIFIED` mark fails.**
"A report that marks every claim `UNVERIFIED` fails the kernel as surely as one that marks none." A fully evidenced report marks none and passes. The sentence sits in the section written to stop over-hedging, and it tells a careful reader to add a mark.
Rewrite: "A report that marks every claim `UNVERIFIED` fails the kernel as surely as one that shows evidence for none."

**W8. `SKILLS_FRAMEWORK.md:217` carries the first-draft kernel.**
Key concepts reads "the check that could prove you wrong" and "deployed means a clean tree". Both were reworded in `d2cdaf8`; the second is the wording refinement 1 exists to remove. It also drops "after your last change". The registry is fleet-read.
Fix: rewrite the line from `SKILL.md:27-32`.

**W9. Rule 4's bound differs across the surfaces.**

| Where | Bound |
|---|---|
| `SKILL.md:9` | "a statement a reader will act on, or one that closes a task" |
| `SKILL.md:30`, `CLAUDE.md:63`, `:68`, `code-reviewer.md:43` | "claim a reader will act on" |
| `session-end.md:68` | "each claim of success the doc makes" |
| `session-doc-format.md:108`, `:208` | "claim of success this doc makes"; "every claim of success" |

The ledger keeps D2's unbounded form, and it says "success", which leaves out absences. The non-claim list also differs: `SKILL.md:9` names four (plan, opinion, explanation of code, diff) and `CLAUDE.md:72` names three.
Fix: pick one bound and one list, and copy them. For the ledger: "one row for each claim a reader will act on".

**W10. The ledger count is defined narrowly, and the measured party writes it (`session-end.md:72`).**
The count is "the number of claims the user had to correct". The plan's Problem says "The user or a review pass caught each one". In the session that ended at `b1c3e36`, reviewers refuted 19 claims; under this definition that session writes 0 unless the user corrected one by hand. The lead incident was found when the user asked a question, not when the user corrected anything. The MOE compares 20 sessions of this count to a baseline from another instrument, so the definition cannot change after adoption.
Fix: say which side each case falls on, before the first ledger line is written: claims a reviewer refuted, and claims retracted after a user's question.

**W11. The Claims table cannot hold its own commit, and rule 2 conflicts with the ledger (`session-end.md:71`).**
- An author can follow "re-run the probe now" for tests. For "pushed" and "merged" the row covers HEAD as it was before the session doc existed. Step 4.5 amends the Step 3 commit after its push (`session-end.md:51`), and the doc itself is committed after Step 5; no step says when. A reader who re-runs the row gets a different SHA.
- Rule 2 says evidence comes from this turn. The ledger re-runs end-state claims only. The text does not say what the Evidence cell holds for a mid-session claim.
Fix: "Name the SHA each row checked. The commit that carries this doc cannot be in its own table; report that push in your final message, with its own `Evidence:` line. A claim about an earlier moment keeps its original output and says when it was taken."

**W12. The reviewer line gives no severity to a refuted claim (`code-reviewer.md:43`).**
A claim with no line is a Warning. A claim the re-run refutes gets "report" and no level, though it is the worse defect. Read per claim, "is a Warning" also turns this gate's 41 unevidenced claims into 41 findings. "The change's report" is undefined: a reviewer often never sees the author's final message. The line does not say what to write for a claim the reviewer cannot re-run.
Fix: "Claims with neither line are one Warning that lists them. A claim your re-run refutes is a Warning, or Critical when a Standard, a gate, or a user decision rests on it; paste the output. A claim you cannot re-run is UNVERIFIABLE, with the reason."
The line is checkable as far as it goes: `grep 'Evidence:'` finds the lines.

**W13. The lead's own messages carry no `Evidence:` line.**
`SKILL.md:11` puts commit messages in scope, and `code-reviewer.md:43` tells me to check them.
Evidence: `for s in <7 SHAs>; do git show -s --format=%B $s; done | grep -c -E '^(> )?(Evidence:|UNVERIFIED:)'` → `0`; the same pattern on plan line 272 → `0`
Section 11 lists 41 claims. Some carry a command and output inline (`4b11ec3`, `ef5b488`); none uses the form. The Status Log's "421 passed" names no Python, and the Tests row asks for one where there is no CI config (`ls .github` fails here).
Why it matters: the commits that ship the rule do not follow it. Either the form is unworkable in commit messages, and `SKILL.md:11` should drop them, or it is workable and the lead should use it.
Fix: decide which. If messages stay in scope, give the Status Log entry its `Evidence:` lines now.

**W14. The tests pin less than the Status Log says.**
"Pins each markable Standard" is refuted in part: these mutants survive with 15 tests green.

| Mutant | Standard element lost |
|---|---|
| M08 | run landed: the output check, "newer than the launch" |
| M09 | venv: `pyvenv.cfg` and `python -V` |
| M10 | deployed: the clean-tree probe |
| M11 | tests pass: CI's Python |
| M12 | pushed: `git ls-remote` |
| M04c | pair 7: 11 claimed, 12 measured |

Each is a substring a test can assert. Four more gaps: the reviewer line's pin checks the path only (M05g deletes the criterion and stays green); the ledger line in `SKILL.md:79` is unpinned (M17); the sidecar count is a string, not a directory listing (M19); the `CLAUDE.md` block's lead and closing sentences are unpinned (M03c).
Fix: one dict of required substrings per claim type; assert `11` and `12` in pair 7; assert the ledger line in all three files; count sidecars from the directory.

**W15. One test fails downstream for a reason that is not drift.**
`test_skill_is_registered` wants "verifying-claims/SKILL.md + 1 sidecar" in `.claude/README.md`. Of 15 sibling repos with a `.claude/` directory, 4 list skills in that form, 9 have a README without it, and 2 have no README there. Three repos carry the hub's hook test today, and one of those has a README with no sidecar tree. `docs/session-doc-format.md` is absent in 3 of 15, and the Step 5 heading in 1.
Fix: say in the entry which files the test expects, or relax the README needle to the skill's name.

**W16. `d1614fc` adds a metric instrument and is tagged `[infra]`.**
WHETSTONE D4 (plan line 108) puts changes to "gate criteria, metrics" in `[gate]` commits. The count line is the instrument for OVERWATCH's MOE. On this branch, `d565df9` and `1ed229c` edited the same two files for WHETSTONE's M1 and carry `[gate]`. PCC check 6 is silent on both, because its path list holds neither file.
Fix: the branch is not on origin (`git ls-remote origin topic/overwatch-verifying-claims` prints nothing), so the tag can still be reworded; or record in the Status Log that `d1614fc` is a D4 change reviewed at this gate.

### Suggestion

**S1. Run landed (`SKILL.md:51`): no probe gives the launch time.** `ls -l` prints minutes. The probe pair 1 teaches has a silent default: `systemctl show no-such-unit-xyz.service -p ExecMainStatus` → `ExecMainStatus=0`, exit 0, for a unit that does not exist. Add `-p ExecMainStartTimestamp`, and say the launch time comes from it or from the log's first line.

**S2. Tests pass (`SKILL.md:54`): "no failures" passes a run that skipped or deselected the tests that matter.** Ask for the skipped and deselected counts. `.venv/bin/pytest` has no Windows form here; plan line 190 gives one.

**S3. Merged (`SKILL.md:56`): the Probe cell lists two commands and "Holds when" needs a third, `git rev-parse main`.** `main` is hardcoded where other rows use `<branch>`. `exit=1` with a stale local `main` does not show "not merged".

**S4. Deployed (`SKILL.md:57`) says "the two SHAs match" without "prints one line".** Trap 1 covers it; the Pushed and Mirror rows say it in the row.

**S5. Trap 3 (`SKILL.md:63`) names the process start and no probe for when the code arrived.** `git reflog -1 --date=iso` prints it (`f100c2b HEAD@{2026-10-01 12:52:51 -0500}` here).

**S6. Three kernel wordings to tighten.** Rule 5's "a checkout that runs code" fits any repo where tests run; "a checkout a timer or service runs from" is the incident. Rule 2's "your last change" leaves out a change by another agent or a timer; the proposer's "to the thing claimed" covers it. Rule 2 still forces a re-run at every report when nothing changed (the proposer's defect B), which works against 2d's clean-turn limit.

**S7. The state "deployed" covers a push, and the seventh claim type is also "Deployed".** "Pushed to origin (deployed)" reads as an overclaim to anyone who has not seen the ladder. Rename the row "Running from a checkout".

**S8. Refinements 1 and 3 change approved decisions.** They are recorded, as the plan's append-only rule requires. The record is the session lead's; no user confirmation is on file. Ask at merge. The tests pin none of the four (M23, M24, M25 survive).

**S9. Prose, all Minor.**
- `SKILL.md:43`: "Tested code may not be pushed" reads as a ban. Rewrite: "Tested code might not be pushed yet, and pushed code might never have run."
- `CLAUDE.md:63`: the clause after the colon hangs off "skill". Rewrite: "Every claim a reader will act on (that something works, landed, synced, exists, or is absent) follows the verifying-claims skill."
- `CLAUDE.md:72`: "that needs no line" has no referent in the ambient text. Rewrite: "that needs no `Evidence:` line."
- `SKILL.md:27`: the semicolon joins the cap and the absence clause with no stated link. Make the absence clause its own sentence.

**S10. `session-end.md:75`, the "Search related sessions" line, now sits inside the Claims subsection.** Move the subsection below it. The no-claims case ("writes the count line alone", `:73`) is missing from the format doc.

**S11. A pipe in a command breaks a markdown table cell.** The Claims table holds commands. Add "escape `|` as `\|`" to the format doc; the plan does this at line 189.

**S12. `d2cdaf8` cites a file that enters the tree one commit later.** `git cat-file -e d2cdaf8:docs/reviews/20261001_overwatch_kernel_wording.md` → exit 128.

**S13. Portability, small.** `EXAMPLES.md:108` leans on "the plan that commissioned this skill", which no downstream repo has. The test docstrings name the hub plan and its decision numbers (`test_verifying_claims.py:5`, `:52`).

**S14. This run did not have the new reviewer line loaded.** The agent definition in my context ends its checklist at the figures line; the caller's brief supplied the claims check. The line takes effect in sessions that start after it lands.

**S15. Three weak spots in the tests.** A seventh rule written as a bullet passes the six-rule cap (M01c). The Level 0 block passes anywhere in the file (M05f). Deleting the state table or the four traps fails nothing (M26, M27).

## 2. The probe table, row by row

Run in this repo unless marked scratch.

| Row | Output here | Can "Holds when" be true while the claim is false? |
|---|---|---|
| Run landed | no run or log exists here | Yes: S1 |
| Pushed | `git rev-parse HEAD` → `f100c2bc...`; `git ls-remote origin topic/overwatch-verifying-claims` → nothing, `exit=0` | Yes: W2 (scratch). Here it fails correctly: the branch is not on origin |
| Mirror synced | one remote (`git remote -v`); no mirror | Suffix match, as W2 |
| Tests pass | `421 passed`, `exit=0`; `Python 3.12.13`; no `.github` | Skips and deselection: S2 |
| Venv | `ls -d .venv*` → `.venv`; cfg prints `version_info = 3.12`; `Python 3.12.13` | Yes, for "absent": W3 (scratch) |
| Merged | `is-ancestor ef5b488 main` → `exit=1`; `d03e66a` → `exit=0`; `ls-remote origin main` → `b1c3e360...`, equal to `git rev-parse main` | No false hold found; S3 |
| Deployed | `git status --porcelain` → 5 untracked files | No; conservative on stray files |

The four traps:

| Trap | Evidence | Verdict |
|---|---|---|
| Empty output is not a match | `git ls-remote origin no-such-branch-xyz; echo "exit=$?"` → no line, `exit=0` | HOLDS |
| Exit status after a pipe | `false \| tail -1; echo "exit=$?"` → `exit=0` | HOLDS |
| Long-running process | `ps -o lstart= -p $$` → `Thu Oct  1 12:54:55 2026` | HOLDS; S5 |
| Tests and the tripwire | `ISOLATION.md:71` | REFUTED: C1 |

## 3. Mutation results

47 mutants, one per run, on `git archive f100c2b` copies in scratch. 25 killed, 22 survived. One survivor is equivalent (M07b, 109 lines), so the score is 25 of 46.

The seven the caller named, 12 variants, all killed:

| Mutant | Killed by |
|---|---|
| M01a, M01b seventh rule (skill only; both files) | `test_kernel_has_at_most_six_rules` |
| M02a probe row deleted | `test_probe_table_has_one_probe_per_claim_type` |
| M03a rule changed in `CLAUDE.md` only | `test_claude_md_carries_the_kernel_verbatim` |
| M04a pair 7 loses its Evidence line | `test_each_example_shows_a_before_and_an_evidenced_after` |
| M05a to M05e each registration removed | `test_skill_is_registered` (4), the drift test (1) |
| M06a Claims table removed from the format doc | `test_session_doc_format_defines_the_claims_table` |
| M07a padded to 110 lines | `test_skill_md_is_under_110_lines` |

Mine, 13 killed: M02b (eighth row), M03b (rule deleted in `CLAUDE.md`), M04d (eighth pair), M04e and M04f (clean report removed; given an Evidence line), M06b (count line reworded in the format doc), M06d (State column dropped), M15 (Claims subsection moved out of Step 5), M16, M18 (session-end strings), M20 (`EXAMPLES.md` deleted), M21 (frontmatter name), M22 (four states cut from rule 1).

Survivors, 21 real:

| Mutant | Change | Finding |
|---|---|---|
| M08 to M12 | a Standard element cut from a probe row | W14 |
| M04c | pair 7 replaced; 11 and 12 gone | W14 |
| M05g | reviewer line keeps the path, loses the criterion | W14 |
| M17 | ledger line reworded in `SKILL.md` | W14 |
| M19 | second sidecar added; registries say 1 | W14 |
| M03c | `CLAUDE.md` lead and closing sentences removed | W14 |
| M13 | Pushed probe becomes `git push` | read-only is unpinned; hard to pin |
| M04b | pair 1 loses one of two Evidence lines | judgment |
| M23, M24, M25 | each refinement reverted in both files | S8 |
| M01c, M05f, M26, M27 | bullet rule; block moved; tables deleted | S15 |
| M06c, M14 | "(Required.)" note; "re-run now" bullet | minor |

Standards no test pins: the parenthesized elements of 2a; "read-only"; 2b's 11 and 12; "no work-system names" (it cannot be pinned without committing the terms).

## 4. The four refinements

| # | Refinement | Reading |
|---|---|---|
| 1 | D10's clean tree scoped to "a checkout that runs code" | Fair, and recorded. It matches the incident. It also removed the only guard on the Pushed row (W2) |
| 2 | "this turn, after your last change" | Fair. It adds a condition and removes none |
| 3 | "every success claim" bounded to "a claim a reader will act on" | A change, not a reading. It narrows D2, and the author is the judge of the bound. Recorded, sound for 2d, applied unevenly (W9). Needs the user's yes (S8) |
| 4 | A clean report after the seven pairs | Fair. The Standard sets a floor; the test pins seven pairs and the report apart |

D10's two rules are both kernel rules: `SKILL.md:31` and `:32`, `CLAUDE.md:69` and `:70`.

Declining the fold of rule 6 into rule 3 is sound on D10's letter: D10 says "Two kernel rules", and a clause is not a rule. The cost is real. "Paste the blocker's error" sits in `SKILL.md:79` and not in the ambient text. Rule 4 is still two sentences, so "one idea now" (`d2cdaf8`) is generous. The lead held D10 to its letter here and refined it in refinement 1; both calls are defensible, and the log should say that the standard differed.

## 5. The proposer's ten

| # | Recommendation | Status | Line |
|---|---|---|---|
| 1 | Absence in rule 1 and in the scope sentence | ADOPTED | `SKILL.md:27`, `:11`, `:18` |
| 2 | Rule 3 names the outcome; fold in read-only | PARTLY | Outcome at `SKILL.md:29`; rule 6 kept at `:32` |
| 3 | Rule 2 anchors on the last change | PARTLY | `SKILL.md:28` keeps "this turn"; drops "to the thing claimed" |
| 4 | Bound in rule 4, bound sentence, clean pair | ADOPTED | `SKILL.md:30`, `:9`; `EXAMPLES.md:112-116`. "Share the line" is at `SKILL.md:70`, not in the rule |
| 5 | Scope the clean-tree rule to checkouts | ADOPTED | `SKILL.md:31` |
| 6 | Split rule 4; blocker's error in the kernel; pair 5 pastes the refusal | PARTLY | No split (`SKILL.md:30`); error text at `:79` only; pair 5 at `EXAMPLES.md:76` |
| 7 | Probe-row fixes | ADOPTED | `SKILL.md:51-57`. The launch-time gap from the same section stays (S1) |
| 8 | Widen `observed` | ADOPTED | `SKILL.md:41` |
| 9 | Fix pairs 1, 2, 6, 7 | ADOPTED | `EXAMPLES.md:14-17`, `:32`, `:91`, `:108` |
| 10 | Update the two literal-text tests | NOT ADOPTED | Moot: "this turn" and "never write" stayed in the kernel (`test_verifying_claims.py:56`, `:60`) |

The unnumbered item, saying what wording cannot fix, is ADOPTED at `SKILL.md:85`.

## 6. D6, no work-system names

I checked 39 search strings: every system, product, dataset, and domain term the held source names, with spelling variants, plus two organization strings and the machine alias, which the source does not name. No term is quoted here.

- In-scope files: 0 system, product, dataset, or organization names.
- `EXAMPLES.md:17` and `docs/reviews/20261001_overwatch_kernel_wording.md:184`: a generic two-word description of a component, the source's wording with the hyphen spelled out. It is a description, not a name. The public plan does not carry it; drop it if in doubt.
- `.claude/README.md:111` and `CLAUDE.md:17`: false positives on lines this branch did not touch, a common English word and a substring of one.
- The seven commit messages: 0 hits.
- Plan line 272: one common word in another sense, the personal machine's alias, and the plan's own phrase for the work machine. No names.
- Out of scope, already on `main`: plan lines 37 and 40 (a dataset format name inside a path), 190 and 267 (a forge CLI name), 192 and 228 (an object-store CLI command).

## 7. Level 0 portability

The skill names no repo and no project. It points at two paths a downstream repo may lack: `docs/session-doc-format.md` (`SKILL.md:79`, `:96`), absent in 3 of 15 sibling repos, and `shift-left-testing/ISOLATION.md` (`:64`, `:95`), which ships in the same held release. Pair 7 is hub history and says so. Tests: W15.

## 8. Wiring

- Kernel: identical in both files (`diff` prints nothing).
- Cross-references: every path on a line this branch added resolves (8 of 8). `EXAMPLES.md`, `ISOLATION.md`, `docs/session-doc-format.md`, and the writing skill's rule 6 exist.
- Sidecar count: 1 in the directory, in `.claude/README.md:51`, and in `SKILLS_FRAMEWORK.md:213`.
- PCC check 5: 0 MISSING and 0 MISSING-DIR; all six surfaces exist. Run over the branch's changed files, as plan line 153 can be read, the same regex prints 17 MISSING and 8 MISSING-DIR. None is on a line this branch added: they are placeholders, retired paths, and URL fragments.
- Stale registry text: W8.

## 9. Gate-surface separation

PCC check 6's logic prints no WARN for any of the seven commits; none touches a path on its list.

`1edf0d4` is acceptable under D4. It holds the agent file and one `parametrize` line that pins the new line. The pin is not work the gate judges, and splitting it would leave an unpinned gate commit or a red one. The capture-point work split its pin into `8c31948`; either form is defensible. The pin itself is weak (M05g). The line: W12. The tag on `d1614fc`: W16.

## 10. The `/session-end` change

- "Required" is stated the same way in `session-end.md:62`, `session-doc-format.md:108`, and `:207`.
- No collision with the capture point: the `KB-graph:` bullet at `:64` is intact, and its 3 pins pass. The layout slip is S10.
- Sequencing: W11.
- The ledger line: `grep -c 'Overclaims the user caught this session: N'` → 1 in each of `session-end.md`, `session-doc-format.md`, and `SKILL.md`, and at plan line 158. One ASCII string matches all four.
- The count's definition: W10.

## 11. The lead's claims

Seven commit messages and the Status Log entry. 41 claims: 30 HOLDS, 1 REFUTED in part, 10 UNVERIFIABLE.

| # | Where | Claim | Verdict | Evidence or reason |
|---|---|---|---|---|
| 1 | `ef5b488` | 95 lines, 5 tests | HOLDS | `wc -l` at that commit → 95; `grep -c '^def test_'` → 5 |
| 2 | `ef5b488` | D10's rules are kernel rules 5 and 6 | HOLDS | read at that commit |
| 3 | `ef5b488` | Three slices, each red first | UNVERIFIABLE | tests and text share the commit |
| 4 | `ef5b488` | Each probe was run in this repo first | UNVERIFIABLE | history. Two rows have nothing to run against here: one remote, no log. The first Pushed row read this branch's own empty output as a match, which the lead later logged as its error |
| 5 | `ef5b488` | `is-ancestor` exits 0 merged, 1 unmerged | HOLDS | `d03e66a` → `exit=0`; `ef5b488` → `exit=1` |
| 6 | `ef5b488` | `cat` on a missing cfg exits 1 | HOLDS | `cat .venv-none/pyvenv.cfg` → `exit=1` |
| 7 | `4b11ec3` | Seven pairs, one per shape, plus the slip | HOLDS | 7 sections; the six shapes match the source's six |
| 8 | `4b11ec3` | `git show 17db809:tests/conftest.py \| wc -l` prints 12 | HOLDS | → `12` |
| 9 | `4b11ec3` | A 16-term grep printed nothing | UNVERIFIABLE | the 16 terms are unrecorded. My 39 strings at `4b11ec3`: 0 names |
| 10 | `4b11ec3` | Two tests, red before the file | UNVERIFIABLE | as 3 |
| 11 | `4b11ec3` | 7 tests | HOLDS | 7 |
| 12 | `d2cdaf8`, log | Five checkable findings all reproduce | HOLDS | the message names none. I re-ran five: `tail` exits 0; empty `ls-remote`; 5 untracked files; no `.github`; the pipe status |
| 13 | `d2cdaf8` | `ls-remote` prints nothing, exits 0 | HOLDS | section 2 |
| 14 | `d2cdaf8` | Old rule 5 voided push claims here | HOLDS | 5 untracked files |
| 15 | `d2cdaf8` | Pair 1 pasted an `exit=1` `tail` cannot print | HOLDS | `4b11ec3` text; `tail -1 /etc/hostname` → `exit=0` |
| 16 | `d2cdaf8` | Pairs 2, 4, 6 unevidenced; pair 5 asserted | HOLDS | `git diff 4b11ec3 d2cdaf8` |
| 17 | `d2cdaf8` | Four traps under the table | HOLDS | `SKILL.md:61-64` |
| 18 | `d2cdaf8` | Two tests red before the edits | UNVERIFIABLE | as 3 |
| 19 | `d2cdaf8` | 102 lines; 8 tests | HOLDS | 102; 8 |
| 20 | `cbd2ef5` | Six rules copied from `SKILL.md` | HOLDS | `diff` → identical |
| 21 | `cbd2ef5` | A drift test compares the lists | HOLDS | M03a, M03b killed |
| 22 | `cbd2ef5` | Four tests red before each edit | UNVERIFIABLE | as 3; `d2cdaf8` and `cbd2ef5` share the second 11:12:30 |
| 23 | `cbd2ef5` | 12 tests | HOLDS | 9 functions and 3 parameters |
| 24 | `1edf0d4` | Ships with only its own pin | HOLDS | 2 files; 1 test line |
| 25 | `1edf0d4` | One test red before the edit | UNVERIFIABLE | as 3 |
| 26 | `1edf0d4` | 13 tests | HOLDS | 13 |
| 27 | `d1614fc` | After the capture point, which edits the same two files | HOLDS | `d565df9` and `1ed229c` touch both; reflog order |
| 28 | `d1614fc` | The table and two best-practice lines | HOLDS | `git show d1614fc` |
| 29 | `d1614fc` | Two tests red before the edits | UNVERIFIABLE | as 3 |
| 30 | `d1614fc` | 15 tests | HOLDS | `15 passed` |
| 31 | log | The tests pin each markable Standard | REFUTED in part | the six listed pins hold; M08 to M12 and M04c survive (W14) |
| 32 | log | Each test was red before its edit | UNVERIFIABLE | below |
| 33 | log | The capture point went first | HOLDS | reflog |
| 34 | log | `git status --porcelain` prints five | HOLDS | 5 lines |
| 35 | log | 2d fails above 1 of 6 clean turns | HOLDS | plan line 206 |
| 36 | log | Two findings were the lead's own errors | HOLDS | `ef5b488` table: "The two SHAs match" |
| 37 | log | One line on weak checks and invented output | HOLDS | `SKILL.md:85` |
| 38 | log | Pair 7's last sentence reworded | HOLDS | `EXAMPLES.md:108` |
| 39 | log | One commit per 2c surface; the reviewer line alone | HOLDS | 3 commits; "alone" means with one pin line |
| 40 | log | 421 with and without `CI=true`; 403, 15, 3 | HOLDS | 421, 421, 403, 15, 3 on Python 3.12.13 |
| 41 | log | The user chose to hold the entries, and Step 5.5 | UNVERIFIABLE | no artifact here records the user's words |

**On "each test was red before its edit"**. Evidence that exists: each commit's test file, run on its parent's tree, fails exactly the new tests (5, 2, 2, 4, 1, 2). So each test can be red, and none passes by accident. Evidence that does not exist: no commit holds a red test alone; test and text land together; two of the commits share one second. The shift-left audit hook logs `src/myproject/` only. Order of writing left no trace. If the claim matters, commit the red test first next time.

## 12. Prose

Reviewed per `REVIEWING.md`, four passes.

- Point: each new section states its point first. No finding.
- Structure: one Major (W7, a sentence that says the reverse of its intent) and one Minor (rule 1's semicolon, S9).
- Words: 0 hits on the 10 banned words and 2 banned phrases, over the 433 added lines, plan line 272, and the 7 messages.
- Punctuation: 1 em dash, in the `EXAMPLES.md:1` heading, which is exempt. 0 in running prose.
- Minor findings with rewrites: S9.

## Reviewer's notes

- I wrote this file and scratch files only. I did not update agent memory: the caller limited my writes to this report.
- Two `.venv/bin/pytest` runs in the repo wrote `.pytest_cache`, `.hypothesis`, and pytest's temp directory under `/tmp`. One scratch run of `main`'s suite omitted `--basetemp` and wrote to that same pytest temp directory, outside my scratch directory. That was my slip. `git status --porcelain` printed the same five lines before and after; HEAD is still `f100c2b`.
- Network: six `git ls-remote` calls against origin. A seventh named a remote that does not exist and failed locally.
- Read-only outside the repo: `ls` and `grep` over sibling repos, reported as counts; `systemctl show` and `list-timers` on names that do not exist.
- I read the held source file. This report quotes none of it.

**Verdict: GO-WITH-FIXES** for tasks 2a to 2c. Apply C1 and the Warnings, then re-run sections 2 and 3 against the fixed branch. Wave 2 stays open until 2d passes.

---

## Round 2

**Date**: 2026-10-01
**Subject**: the same branch at `c97c79e`. New commits: `1b50924` ([gate]), `6bde122`, `c97c79e`. The merge `2e33662` is out of scope except for its one conflict resolution.

### Verdict

**GO** for tasks 2a to 2c.

C1 is closed. Of the 16 Warnings, 14 are closed and 2 are partial (W13, W15). Both partials are record items, not shipped text. The round 1 mutation set now scores 41 of 46, up from 25. I checked 45 new claims by the lead: 41 hold, 2 are refuted in part, 2 cannot be verified. One new Warning (R2-W1) and seven Suggestions follow. None needs another review round: append R2-W1's lines and the W15 surface to the Status Log, and take R2-S1 to R2-S4 with the next edit to the skill.

Wave 2 stays open until 2d passes.

### What I ran

| Check | Command | Result |
|---|---|---|
| Suite at `c97c79e`, 3.12 | `.venv/bin/pytest -q`; then with `CI=true` | `431 passed, 1 warning`, exit 0, both ways; `Python 3.12.13` |
| The two doc-pin files | same, per file | `25 passed`; `3 passed` |
| Suite on 3.11 | `<scratch venv311>/bin/python -m pytest -q -p no:cacheprovider`; then with `CI=true` | `393 passed, 5 skipped, 1 warning`, exit 0, both ways; `Python 3.11.15` |
| `1b50924` with the old test file | `git archive 1b50924` export, `pytest -q -p no:cacheprovider` | `421 passed, 1 warning`, exit 0 |
| New tests on the unfixed tree | `6bde122`'s test file on `2e33662`'s tree; on `1b50924`'s tree | 7 failed, 18 passed; 5 failed, 20 passed |
| Mutation | 70 mutants on a `git archive c97c79e` export | 46 killed, 24 survived (1 equivalent) |
| PCC check 5 | both blocks, verbatim | 0 MISSING, 0 MISSING-DIR |
| D6 | 39 search strings over the changed files, 206 added lines, 4 messages | 0 names |
| Kernel identity | `diff` of `SKILL.md:27-32` and `CLAUDE.md:65-70` | identical |

### 1. Round 1 findings

| # | Status | Evidence at `c97c79e` |
|---|---|---|
| C1 | CLOSED | `SKILL.md:65`: "so rule 6 does not hold for them"; reverting it fails `test_tests_are_not_called_read_only` (N01) |
| W1 | CLOSED | `CLAUDE.md:72`: "The belief a plan rests on is one: check it before you act."; `SKILL.md:9`; `EXAMPLES.md:50` |
| W2 | CLOSED | `SKILL.md:52` reads `git status --porcelain`; `refs/heads/` at `:52`, `:53`, `:56`, `:57`. In scratch the fixed row fails both round 1 cases: status prints ` M f.txt`; `git ls-remote origin refs/heads/main` prints nothing where only `feature/main` exists |
| W3 | CLOSED | `SKILL.md:55`: `find . -maxdepth 3 -name pyvenv.cfg`; none found is "none under this directory", which the row calls less than absent. In scratch it prints `./venv/pyvenv.cfg` and `./envs/gpu/pyvenv.cfg` |
| W4 | CLOSED | Python at `SKILL.md:75` and `EXAMPLES.md:61`; pair 1 claims "scheduled", not deployed (`:15`); states at `:32`, `:104` |
| W5 | CLOSED | `EXAMPLES.md:105`: "at the commit under review on 2026-09-30"; `:108` says why |
| W6 | CLOSED | `SKILL.md:67`: "So is a check the user or the harness declined: do not retry it another way."; `EXAMPLES.md:79` |
| W7 | CLOSED | `SKILL.md:86`: "as one that shows evidence for none" |
| W8 | CLOSED | `SKILLS_FRAMEWORK.md:217` restates the six shipped rules |
| W9 | CLOSED | `grep -n -e 'claim of success' -e 'closes a task'` over the eight files prints nothing; the bound is on all six surfaces; the non-claim lists match (`SKILL.md:9`, `CLAUDE.md:72-73`) |
| W10 | CLOSED | `session-end.md:75-76` defines N and M. M awaits the user; the Status Log says so. A small gap: R2-S2 |
| W11 | CLOSED | `session-end.md:73-74`; `session-doc-format.md:103` ("at `<commit>`") |
| W12 | CLOSED | `code-reviewer.md:43` carries the three severities and UNVERIFIABLE |
| W13 | PARTIAL | The scope decision is recorded. `1b50924` carries 1 `Evidence:` line, `6bde122` carries 3 and 1 `UNVERIFIED:`, the Status Log 2. Four claims still carry none: R2-W1 |
| W14 | CLOSED | M08 to M12, M04c, M05g, M17, M19, and M03c all die now |
| W15 | PARTIAL | The README needle is the skill's name and the sidecar count comes from the directory (`test_verifying_claims.py:202-209`). The Status Log lists five surfaces for the release entry; line 209 reads a sixth, `.claude/README.md`. Two of 15 sibling repos have no such file |
| W16 | CLOSED | `1b50924` is tagged `[gate]`; the Status Log records `d1614fc` as a D4 change reviewed here |

| # | Status | Evidence |
|---|---|---|
| S1 | ADOPTED | `SKILL.md:51` names where the launch time comes from; `:63` is the silent-default trap; pair 1 no longer uses `systemctl show` |
| S2 | PARTLY | Skips and deselection at `SKILL.md:54`; the Windows form is declined, and the log says so |
| S3 | PARTLY | `git rev-parse main` is in the Probe cell (`SKILL.md:56`); `main` is still literal, and the stale-local-`main` case is unsaid |
| S4 | ADOPTED | `SKILL.md:57`: "the third prints one line with the second's SHA"; `--exit-code` at `:61` |
| S5 | ADOPTED | `SKILL.md:64`: `git reflog -1 --date=iso` |
| S6 | PARTLY | Rule 2 and rule 5 reworded (`SKILL.md:28`, `:31`); the re-run at every report stays, as D2 |
| S7 | ADOPTED | `SKILL.md:57`: "Deployed: running from a checkout" |
| S8 | ADOPTED | The Status Log lists three changes for the user; M23 to M25 now die |
| S9 | ADOPTED | `SKILL.md:43`, `:27`; `CLAUDE.md:63`, `:73` |
| S10 | ADOPTED | `session-end.md:66` sits above `:68`; the no-claims case is at `session-doc-format.md:110` |
| S11 | ADOPTED | `session-doc-format.md:110` says to escape a pipe inside a command |
| S12 | NOT ADOPTED | Declined as a record; the log says so |
| S13 | ADOPTED | `EXAMPLES.md:108`: "A plan's first draft"; the test docstrings name no plan |
| S14 | NOT ADOPTED | Nothing to change; a note about session start |
| S15 | PARTLY | M01c, M26, and M27 die; the Level 0 block still passes anywhere in the file (M05f) |

### 2. Mutation, re-run

The export is `git archive c97c79e`. The anchors are updated in a scratch copy of the runner.

Round 1 set, 47 mutants: 41 killed, 6 survived, 1 of them equivalent. Score: 41 of 46, from 25 of 46.

- Round 1 survivors that now die, 16: M01c, M03c, M04c, M05g, M08, M09, M10, M11, M12, M17, M19, M23, M24, M25, M26, M27.
- Still alive, 5: M04b (one of two Evidence lines cut from pair 1), M05f (block moved), M06c (the "(Required.)" note), M13 (a `git push` among the probes), M14 (the "re-run now" bullet). M13 is the read-only gap the docstring names.

Round 2 set, 23 mutants, each reverting one round 1 fix: 5 killed, 18 survived.

- Killed: N01 (C1), N02 (W1 in `CLAUDE.md`), N12 (W9 in `/session-end`), N20 (a state renamed), N21 (the framework's sidecar count).
- Survived: the reverts of W1 in `SKILL.md:9`, W2, W3, W4, W5, W6, W7, W8, W10 (three forms), W11, W12, S1, one of three bound mentions in the format doc, the README count, and a drift in `SKILL.md:82`. See R2-S5.

Both sets: 46 of 69.

### 3. The new text, read for regressions

Probes, run here:

| Probe | Output |
|---|---|
| `git ls-remote origin refs/heads/main` | `b1c3e360...	refs/heads/main`; equal to `git rev-parse main` |
| `git ls-remote --exit-code origin refs/heads/no-such-branch-xyz; echo "exit=$?"` | no line, `exit=2` |
| `find . -maxdepth 3 -name pyvenv.cfg` | `./.venv/pyvenv.cfg` |
| `git reflog -1 --date=iso` | `c97c79e HEAD@{2026-10-01 13:23:47 -0500}: commit: ...` |
| `systemctl list-timers no-such-xyz.timer` | `0 timers listed.` |
| `systemctl show no-such-unit-xyz.service -p ExecMainStatus` | `ExecMainStatus=0`, as trap 3 says |

| New text | Reading |
|---|---|
| Trap 5, `SKILL.md:65` | Sound. It is my wording, and it is pinned |
| Pushed, third probe, `SKILL.md:52` | Checkable when the status output is pasted, as pair 2 does. "No file the claim covers" asks the reader to compare paths; that is a judgment, and a visible one |
| Venv, "less than absent", `SKILL.md:55` | Sound. The probe reaches three levels and the wording says "under this directory": R2-S4 |
| Declined check, `SKILL.md:67` | Consistent with rule 4: declined is not skipped. "The harness declined" could be stretched to cover a timeout; the pasted error shows which it was |
| Rule 5, `SKILL.md:31` | Consistent with the state table (`:40`). The Deployed row (`:57`) asks a clean tree of any checkout that runs, which is stricter than the rule and errs the safe way |
| The M line | `session-end.md:76` and `session-doc-format.md:108` agree on the string. Plan line 158 names N only, and the Status Log says the MOE reads N only. `SKILL.md:82` still says "one count": R2-S2 |
| Reviewer line, `code-reviewer.md:43` | Sound. I applied it in section 4 |
| `CLAUDE.md:72`, the belief under a plan | Closes W1. Every plan rests on several beliefs, so this may raise the flag rate on 2d's clean turns. 2d measures it |

The merge `2e33662`: the resolution kept both sides. Against `d91441f` the format doc differs only by this branch's Claims lines; against `f100c2b`, only by the capture point's two rewordings. No conflict marker remains, and the 3 capture pins pass.

### 4. The lead's new claims

45 claims in `1b50924`, `6bde122`, `c97c79e`, and the new Status Log entry: 41 HOLDS, 2 REFUTED in part, 2 UNVERIFIABLE.

| # | Where | Claim | Verdict | Evidence or reason |
|---|---|---|---|---|
| 1 | `1b50924` | Tagged `[gate]`; holds the three gate surfaces | HOLDS | `git show --name-only`: 3 files |
| 2 | `1b50924` | W9 on the ledger | HOLDS | `session-end.md:70` |
| 3 | `1b50924` | W10: N defined; M added; M not in N | HOLDS | `session-end.md:75-76` |
| 4 | `1b50924` | W11: rows name a commit; the doc's commit goes in the final message | HOLDS | `session-end.md:73-74` |
| 5 | `1b50924` | S10 and S11 | HOLDS | `session-end.md:66`; `session-doc-format.md:110` |
| 6 | `1b50924` | W12: the reviewer line's severities | HOLDS | `code-reviewer.md:43` |
| 7 | `1b50924` | Tests pass on this tree with the old test file: 421 | HOLDS | export of `1b50924` → `421 passed, 1 warning`, exit 0 |
| 8 | `1b50924` | The run was made before the amend | UNVERIFIABLE | order of events. The reflog shows 17 seconds between `4893bd7` and the amend |
| 9 | `6bde122`, log | C1, W2, W3, W5, S1 all reproduce | HOLDS | `ISOLATION.md:71`; ` M f.txt` with equal SHAs; `find` against `ls`; `wc -l tests/conftest.py` → 16; `ExecMainStatus=0`. "Before fixing" is history |
| 10 | `6bde122` | C1 fixed | HOLDS | `SKILL.md:65` |
| 11 | `6bde122` | W1 fixed in both files | HOLDS | `SKILL.md:9`; `CLAUDE.md:72` |
| 12 | `6bde122` | One bound and one non-claim list on every surface | HOLDS | grep for the old forms prints nothing |
| 13 | `6bde122` | S6: rules 2 and 5 | HOLDS | `SKILL.md:28`, `:31` |
| 14 | `6bde122` | W7 fixed | HOLDS | `SKILL.md:86` |
| 15 | `6bde122` | Probe table: every `git ls-remote` names `refs/heads/` | HOLDS | 5 of 5 in the table. One specimen outside it does not: R2-S1 |
| 16 | `6bde122` | The Pushed row reads `git status --porcelain` | HOLDS | `SKILL.md:52` |
| 17 | `6bde122` | W3 fixed | HOLDS | `SKILL.md:55` |
| 18 | `6bde122` | Two more traps | HOLDS | 5 bullets, `SKILL.md:61-65` |
| 19 | `6bde122` | W6 fixed | HOLDS | `SKILL.md:67` |
| 20 | `6bde122` | Every tests-pass line names its Python; pairs 2 and 7 name a state | HOLDS | `SKILL.md:75`; `EXAMPLES.md:61`, `:32`, `:104` |
| 21 | `6bde122` | Pair 1 reads the completion line and claims "scheduled" | HOLDS | `EXAMPLES.md:14-15` |
| 22 | `6bde122` | Pair 7 names its date; the file is 16 lines today | HOLDS | `EXAMPLES.md:105`; `wc -l` → 16 |
| 23 | `6bde122` | W8 fixed | HOLDS | `SKILLS_FRAMEWORK.md:217` |
| 24 | `6bde122` | The five new kinds of pin | HOLDS | M08 to M12, M04c, M17, M18, M19 die. The bound's pin is a presence check: R2-S5 |
| 25 | `6bde122` | Seven of the new pins were red against the unfixed text | HOLDS | 7 failed on `2e33662`'s tree. Against its own parent, 5: `1b50924` had fixed two surfaces |
| 26 | `6bde122` | Two requirements stay unpinned, and the docstring says why | HOLDS | `test_verifying_claims.py:8-10` |
| 27 | `6bde122`, log | 431 both ways: 403, 25, 3; Python 3.12.13; no CI config | HOLDS | 431, 431; 25; 3; `ls .github` fails |
| 28 | `6bde122` | On 3.11.15, the two new files: 28 passed | HOLDS | `28 passed` |
| 29 | `6bde122` | `SKILL.md` is 105 lines | HOLDS | `wc -l` → 105 |
| 30 | `c97c79e` | The entry and the reviewer's report ride here | HOLDS | 2 files: plan +5, report +398 |
| 31 | log | Round 1's counts; all three Standards held | HOLDS | round 1 above |
| 32 | log | `test-runner` matched the lead's suite numbers | UNVERIFIABLE | no artifact in the repo records that run |
| 33 | log | The five lead errors, as described | HOLDS | C1, W1, W2, S1, W5 above |
| 34 | log | 41 claims: 30, 10, 1; six mutants left 15 tests green | HOLDS | round 1, sections 11 and 3 |
| 35 | log | `1b50924` was amended with the tree unchanged | HOLDS | reflog: `4893bd7`, then `commit (amend)` to `1b50924`; both have tree `9076e88f` and parent `2e33662` |
| 36 | log | Three changes wait on the user; the MOE reads N only | HOLDS | plan line 158 names N only |
| 37 | log | The seven commits keep their SHAs, which two reports cite | HOLDS | `git log` unchanged; `grep -l ef5b488 docs/reviews/*.md` → 2 files |
| 38 | log | From `1b50924` on, the messages carry `Evidence:` lines | REFUTED in part | the lines exist; two claims in `6bde122` have none (R2-W1) |
| 39 | log | `d1614fc` is a D4 change, reviewed at this gate | HOLDS | W16 |
| 40 | log | The new tests expect five surfaces | REFUTED in part | a sixth: `grep -n README tests/unit/test_verifying_claims.py` → line 209 |
| 41 | log | Not adopted: the Windows form; S12 | HOLDS | `SKILL.md:54`; `d2cdaf8` unchanged |
| 42 | log | 3.11, dev extras: 393 passed, 5 skipped, both ways; the skips are matplotlib and pandas | HOLDS | same counts here; neither library imports in that venv. R2-S6 |
| 43 | log | The 3.11 run was a skipped check, then run | HOLDS | `6bde122` (13:22:12) says UNVERIFIED; the egg-info is stamped 13:22:24; the log (13:23:47) cites the run |
| 44 | log | The editable install rewrote the gitignored egg-info; no tracked file changed | HOLDS | `.gitignore:6`; `git status --porcelain` → 5 untracked lines |
| 45 | log | The Wave 2 exit is still open | HOLDS | 2d has not run |

The coordinator said I could not see the pre-amend commit. The reflog still holds it, so claim 35 is checked, not taken on trust.

### 5. `1b50924` with the old test file

It passes: the export gives `421 passed, 1 warning`, exit 0, on Python 3.12.13. `git diff --quiet f100c2b 1b50924 -- tests/unit/test_verifying_claims.py` exits 0, so the test file is the old one.

### 6. PCC check 5 and D6

- Check 5: 0 MISSING, 0 MISSING-DIR. All 5 paths on lines added since `f100c2b` resolve.
- Check 6's logic prints no WARN for the three new commits.
- D6: 0 system, product, dataset, or organization names in the changed files, the 206 added lines, and the 4 messages. Three hits, none a name: `EXAMPLES.md:17` (the generic component description from round 1, unchanged), `CLAUDE.md:17` (a substring of a common word, on an old line), and plan line 277 (the plan's own phrase for the work machine).
- Prose on the added lines and the three messages: 0 em dashes, 0 banned words.

### New findings

**R2-W1. Four claims in the new record carry no `Evidence:` line.** This is the reviewer line applied as written: one Warning that lists them.
- `6bde122`: "Seven of the new pins were red against the unfixed text."
- `6bde122` and the log: "The lead re-ran C1, W2, W3, W5, and S1 before fixing; all five reproduce."
- The log: "`test-runner` matched the lead's suite numbers."
The first two hold by my re-run (claims 25 and 9). The third cannot be checked.
Fix: append to the Status Log. For the first: the test file of `6bde122` on `2e33662`'s tree → `7 failed, 18 passed`. For the third: paste the `test-runner` summary line, or cut the sentence.

**R2-S1. `SKILL.md:77` writes the bare branch name that trap 1 forbids.** The specimen reads `git ls-remote mirror main`; `:61` says "so write `refs/heads/<branch>`". Change it to `refs/heads/main`.

**R2-S2. The second count is not on every surface.** `SKILL.md:82` says "with one count below it"; `session-end.md:75-76` and `session-doc-format.md:106-108` write two. `session-end.md:76` says "on the next line" and the template puts a blank line between; without it markdown renders one paragraph. The format doc defines neither N nor M. And M counts a claim refuted "before the user relied" on it, so a claim a reviewer refutes after the user relied on it is in neither count. Settle these when the user rules on M.

**R2-S3. The table's lead-in still calls every probe read-only.** `SKILL.md:47`, the description at `:3`, and `SKILLS_FRAMEWORK.md:215` say "one read-only probe per claim type"; `SKILL.md:65` says one of them is not. Rewrite `:47`: "One probe per claim type, read-only except the test run (see the traps)."

**R2-S4. "None under this directory" says more than `-maxdepth 3` reaches (`SKILL.md:55`).** In scratch, a venv at `./a/b/.venv` is not found. Write "none within three levels of this directory".

**R2-S5. Most round 1 fixes can be reverted with 25 tests green.** 18 of 23 revert mutants survive. Four cheap pins: `git status --porcelain` in the Pushed elements; `refs/heads/` in the Merged and Deployed elements; the `find` in the venv elements; the M line in both files, if the user keeps it. The bound's pin checks presence, so a second, rival bound on the same surface passes (N13).

**R2-S6. "5 skipped" on 3.11 is 38 tests that did not run.** Two of the five skips are whole modules: `pytest --collect-only` counts 35 tests in them on 3.12, and 431 minus 393 is 38. The log explains the skips, as the Tests row asks. It should give the count of tests too. All 28 doc-pin tests did run on 3.11.

**R2-S7. `1b50924` holds two gate surfaces in one commit.** The reviewer line and the ledger changed together; 2c's Condition says one commit per gate surface. D4 is met: the commit is dedicated, tagged, and reviewed here. No action; a record.

### Reviewer's notes, round 2

- I appended this section and wrote scratch files only. Round 1 is as committed. I did not update agent memory, for the same reason as before.
- Every pytest run on an export passed `-p no:cacheprovider` and a `--basetemp` under my scratch directory. The runs in the repo root wrote the gitignored `.pytest_cache` and `.hypothesis` there; `git status --porcelain` printed the same five untracked lines before and after, and HEAD is `c97c79e`.
- Network: three `git ls-remote` calls against origin.
- I rebuilt the private term list in scratch for the D6 check and deleted it afterward. This section quotes none of it.

**Verdict, round 2: GO** for tasks 2a to 2c. Append R2-W1's evidence and the sixth surface for W15 to the Status Log before merge.
