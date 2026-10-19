# Proposer review: OVERWATCH kernel wording (Wave 2, task 2d pre-test)

**Date**: 2026-10-01
**Subject**: the six kernel rules in `.claude/skills/verifying-claims/SKILL.md` (lines 27-32), the probe table, and `EXAMPLES.md`, at commits `ef5b488` and `4b11ec3`
**Reviewer**: proposer
**Method**: read SKILL.md, EXAMPLES.md, the shape tests, and the private incident source (not quoted here); ran the read-only probes in this checkout. Incidents are named as shapes only.

## Verdict

SHIP-WITH-FIXES. The kernel's core (state ladder, evidence line, `UNVERIFIED: <blocker>`) is sound and carries D1, D2, and D10. Four wording defects put the 2d pass at risk. First, the ambient six rules never define "claim", so the absence shape (venv called unbuilt) sits outside the text a model sees in CLAUDE.md. Second, rule 2's "this turn" passes evidence taken before a later edit. Third, rule 3 does not say the check must read the outcome the claim names, so a launcher's exit 0 satisfies it. Fourth, rule 5 contradicts the probe table: a push claim is `deployed` in the table, but a dirty tree, which this checkout has right now, voids `deployed` under rule 5. Rule 4 packs three instructions and the fix fits inside the six-rule cap.

## 1. Rule by rule

Reader test: can someone with only the report tell the rule was broken?

| # | Verdict | Reader can tell? | Why |
|---|---|---|---|
| 1 | REWORD | Partly | A missing state label is visible. A wrong label ("tested" on a compile check) takes judgment. |
| 2 | REWORD | No | "This turn" is not visible in a report. A reader sees an `Evidence:` line, not when it ran relative to the last edit. |
| 3 | REWORD | Partly | A reader can judge whether the pasted command targets the claim. "Could prove you wrong" is the author's private test. |
| 4 | REWORD (split) | Yes for the evidence half | A missing `Evidence:` line is greppable. "Check what you can" is not visible. |
| 5 | REWORD | Yes | `git status --porcelain` output is pasteable. But it conflicts with the pushed row (section 6). |
| 6 | CUT as a rule, fold into 3 | Yes, from the command | A write in an `Evidence:` command is visible. It earns the least ambient line (section 9). |

### Rule 1

Current: "Name the state: written, tested, deployed, or observed. Claim only the state your evidence reaches."

Two instructions, but they are one idea (label, then cap). Keep the structure. The defect is that an absence ("never built") has no state, so the model has nothing to name. Replacement:

> Name the state (written, tested, deployed, observed) and claim no higher than your evidence reaches; an absence is a claim too.

### Rule 2

Current: "Evidence comes from this turn. Earlier output is stale: re-run the check, re-measure the number."

Defect A: "this turn" is ambiguous in an agentic session. One user turn spans dozens of tool calls. A `pytest` at call 3, an edit at call 20, and a "tests pass" at call 40 all satisfy "from this turn", and all overclaim. Defect B: read literally it forces a re-run of every check at every report, even when nothing changed. Both vanish if the anchor is the last change to the thing claimed, not the turn. Replacement:

> Evidence postdates your last change to the thing claimed; re-run the check, re-measure the number.

This keeps staleness (shape 6) and closes the same-turn gap. The test in `tests/unit/test_verifying_claims.py` asserts the literal "this turn" in the kernel (`test_kernel_carries_the_decided_terms`); update that assertion to "postdates".

### Rule 3

Current: "Run the check that could prove you wrong, and read its exit status. No error is not evidence."

Defect: the check can be real, fresh, and about the wrong thing. A launcher's exit 0, a `tail` of a log whose crash line was caught and logged, and `pytest | tail` all pass the letter. `echo "exit=$?"` after a pipe reports the last stage's status; I did not run that case, but it follows from POSIX pipe semantics and the table's own `tail <log>` probe sits next to "its exit status" without saying whose. The rule needs to name the object. Folding rule 6 here costs six words:

> Check the outcome the claim names, with a read-only check that could fail; a launcher's exit 0 is not the outcome, and no error is not evidence.

### Rule 4

Current: "Show it: an `Evidence:` line with the command and its output. Mark what you cannot check `UNVERIFIED: <blocker>`; check what you can."

Three instructions (see section 5). Replacement, evidence half only:

> Show it: an `Evidence:` line with the command and its output, under each claim a reader would act on; claims that share a check share the line.

The bound ("a reader would act on", "share the line") is the over-flagging fix (section 3).

### Rule 5 (was 6, see below)

The slot freed by splitting rule 4 takes the `UNVERIFIED` instruction:

> What you cannot check, mark `UNVERIFIED: <blocker>` and paste the blocker's error; a check you skipped is not a blocker, so run it.

"Paste the blocker's error" is what makes the blocker checkable by a reader (pair 5, section 8).

### Rule 6 (was 5)

Current: "Deployed means a clean tree: `git status --porcelain` prints nothing."

Keep as the sixth rule, scoped. As worded it says every `deployed` claim needs a clean tree, and the table puts "pushed" and "merged" under `deployed`. I ran the probes here:

```
$ git status --porcelain
?? docs/decision_audit_20260326.md
?? docs/plans/decision_science_gaps.md
?? docs/review_decision_science_waves_2_3.md
?? docs/reviews/2026-03-26_decision_science_quality_review.md
?? docs/reviews/2026-03-26_decision_science_wave1_review.md
```

A model that wants to comply, in this checkout, must mark "pushed to origin" `UNVERIFIED` or refuse `deployed`, though a push depends on refs and not on the work tree. That is the wholesale-`UNVERIFIED` push the 2d clean turns will trigger on any repo with stray files. Replacement:

> A checkout counts as deployed only if clean: `git status --porcelain` prints nothing.

"A checkout" confines D10 to claims about code that runs from a working tree (the timer-reads-half-finished-code shape). Pushed and merged claims rest on ref SHAs. This carries D10 and needs a one-row edit in the state table (section 7).

### Resulting six

1. Name the state (written, tested, deployed, observed) and claim no higher than your evidence reaches; an absence is a claim too.
2. Evidence postdates your last change to the thing claimed; re-run the check, re-measure the number.
3. Check the outcome the claim names, with a read-only check that could fail; a launcher's exit 0 is not the outcome, and no error is not evidence.
4. Show it: an `Evidence:` line with the command and its output, under each claim a reader would act on; claims that share a check share the line.
5. What you cannot check, mark `UNVERIFIED: <blocker>` and paste the blocker's error; a check you skipped is not a blocker, so run it.
6. A checkout counts as deployed only if clean: `git status --porcelain` prints nothing.

Rule 3 now says "read-only", not "never write". The existing test asserts the substring "never write" in the kernel; change it to "read-only". Rules 3 and 5 are still two clauses each, joined by a semicolon, and each clause states the same idea from both sides (what counts, what does not). That is the house-style limit; I would not cut further.

## 2. Coverage

| Shape | Caught by | Status |
|---|---|---|
| Run called landed, engine crashed | 1 (landed is observed, evidence reached deployed), 3 (read the run's output) | Caught only if rule 3 names the outcome. As worded it is partial. |
| Mirror sync asserted, never checked | 3, 4, 5 | Caught. Strongest shape. |
| Venv called unbuilt | Only 3 ("could prove you wrong") | Weak. See below. |
| Fix claimed, never exercised | 1 ("fixed" is written) | Caught. |
| Validation reported twice, never run | 3, 4, 5, and 2 for the second report | Caught. |
| Stale numbers re-reported | 2 | Caught across user turns. Missed within one turn (see rule 2). |

Round 1's two non-mismatch shapes:

- **Negative claim.** The ambient rules never say "absent". The definition of claim sits in SKILL.md's first paragraph and "When to Use", and CLAUDE.md carries only the six rules (`test_claude_md_carries_the_kernel_verbatim`). Worse, the venv incident happened in working narration ("so I'll create it from scratch"), and SKILL.md's scope sentence lists "final message, status report, commit message, review, and session doc", not mid-task planning. A model reading only CLAUDE.md sees success-claim rules and has no cue. The 2d grader's incident turn for this shape is probably a planning sentence. The "absence is a claim too" clause in rule 1, plus "before you act on" in SKILL.md's scope, closes it. Add to SKILL.md's scope sentence: "and before acting on an absence you have not checked."
- **Staleness.** Caught across turns, missed within one. Fixed by the rule 2 rewrite.

No shape is uncaught outright. Two (landed, venv) depend on the rewrites above.

## 3. The over-flagging failure

Where a compliant model drifts toward `UNVERIFIED` or evidence everywhere:

1. **"Claim" is unbounded.** SKILL.md line 9: "any statement that something works, landed, synced, exists, or is absent". "Works" and "exists" cover most of what an agent says: "the function takes two arguments", "the file has a header". Rule 4 as worded puts an `Evidence:` line under each. There is no exemption for explanations, plans, opinions, or an edit whose diff is in the same message.
2. **Rule 4's "check what you can" and "Not a gate".** SKILL.md line 79: "A claim with no `Evidence:` line is a visible defect." A model that treats absence of the line as a defect adds a line to every sentence.
3. **EXAMPLES.md pair 7 teaches it.** "Small numbers get the same probe as large ones" (line 106) turns a line count into a mandatory `wc -l`. A model reading this will probe every number it mentions.
4. **Rule 6 (old 5) on a dirty tree**, shown above. This is the largest single trigger.
5. **Rule 2 read literally** forces re-runs when nothing changed.

Fixes: the bound in rule 4 ("a reader would act on"; shared checks share a line); a bound sentence in SKILL.md, for example "A claim is a statement a reader will act on or that closes a task; a plan, an opinion, or the content of a file you just displayed is not." Add an anti-pair to EXAMPLES.md: "I renamed `foo` to `bar` in `utils.py` and did not run tests" is a clean turn, state written, the diff is the evidence, no further line. SKILL.md has 95 lines and a cap under 110, so a bound sentence plus a short clean example fits.

"This turn" is not unambiguous (rule 2 above). The fix is the anchor change, not a definition of "turn".

## 4. The under-flagging failure

The test case (real, fresh evidence for the wrong claim) passes the letter of the current rules:

- Rule 1: the model labels the claim `observed` and cites a log tail. Label correct, evidence fresh.
- Rule 3: "the check that could prove you wrong" is the model's own judgment of what could prove it wrong. It picks the launcher's exit.
- Rule 4: the `Evidence:` line is present and truthful.

Result: a clean-looking report on a crashed run. Rewrites that close it: rule 3 ("check the outcome the claim names ... a launcher's exit 0 is not the outcome"), and a probe-table fix for the run row (section 6). A residual gap stays: a model can still choose a weak check and label it honestly. Only a reader or the independent verifier of CONOP Approach C closes that, and the rules cannot. Say so in SKILL.md; do not pretend the kernel is closed. A fabricated `Evidence:` output is also uncatchable by wording. A reader checks it against the transcript.

Two smaller letter-passes: self-labeled state ("tested" for a `py_compile`), and an `Evidence:` line that proves a neighbor claim. Rule 3's "the outcome the claim names" covers the second; the first needs the "Evidence that reaches it" column to name what does not reach (a compile or import is written, not tested).

## 5. Rule 4 packs three instructions

Yes, that is a wording defect under "one idea per sentence". Show-it, mark-the-unverifiable, and check-what-you-can are separate ideas, and the third has no reader-visible failure. It fixes inside the cap:

- Rule 4 keeps show-it (sentence one).
- Mark-the-unverifiable becomes rule 5.
- "Check what you can" is dropped as a stand-alone instruction and folded into rule 5 as "a check you skipped is not a blocker, so run it". That is the only form in which it is checkable: a reader sees a blocker with no error text and knows the check was skipped.
- The slot comes from folding the old rule 6 (read-only) into rule 3.

Net: six rules, none with three instructions, the same D2 and D10 terms present.

## 6. The probe table

Commands run in this checkout; all are read-only.

| Row | Read-only? | Can fail? | Holds-when problem |
|---|---|---|---|
| Run landed | Yes | Yes | "No traceback in the tail" is true for a crash that logged `OperationalError: ...` through a logger with no traceback. "Newer than the launch" needs a launch time no probe supplies. Reword: "the exit status is 0 and the log ends with the run's own completion line". |
| Pushed | Yes | Yes | Ran: `git rev-parse HEAD` printed `4b11ec3bd205...`; `git ls-remote origin main` printed `b1c3e3601a9d... refs/heads/main`. They differ, so it fails correctly for a topic branch. But `git ls-remote origin refs/heads/topic/overwatch-verifying-claims` prints nothing and exits 0. "The two SHAs match" is false-by-absence here, yet a model told in rule 3 to read exit status sees 0. Reword: "one line prints, and its SHA equals `git rev-parse HEAD`". |
| Mirror synced | Yes | Mostly | An unreachable mirror fails loudly (ran `git ls-remote nosuchmirror main`: `fatal: ... exit=128`). A mirror with no such branch and an origin with no such branch both print nothing and "match". Same fix: a line must print. Also name what is compared: mirror equals origin, not mirror equals local HEAD. |
| Tests pass | No | Yes | Running pytest writes `.pytest_cache` (ignored per `.gitignore:37`) and runs arbitrary test code. One incident behind this CONOP is a suite that deleted data. Rule 3 as I reworded it says "read-only"; pytest is not read-only in the strict sense. Say so: "tests are the one write-capable probe; run them where deletes cannot reach real data". More serious: "on the Python that CI runs" has no referent in this repo (`ls .github/workflows` fails; `pyproject.toml:11` says `requires-python = ">=3.11"`). The CI-image incident (tests passed on one Python, failed on 3.11) is the reason for the clause, and a model cannot compare to a version it cannot name. Reword: "on the Python in the CI config (`grep -r python-version .github`), or `requires-python` if none". |
| Venv exists | Yes | Yes, but incompletely | Ran: `cat .venv/pyvenv.cfg` printed `version_info = 3.12`, `.venv/bin/python -V` printed `Python 3.12.13`, both exit 0. "Both print" and "both fail" leave the mixed case undefined, and the mixed case is realistic: a venv whose interpreter path was removed has a readable `pyvenv.cfg` and a failing `python`. That is "exists but broken", and the row calls neither. It also checks one path, so "does not exist" is true only of `.venv`; the incident was a differently named venv on disk. Reword the probe to `ls -d .venv*`, and Holds-when to "cfg prints and python runs: usable; cfg prints and python fails: exists, broken; `ls` finds nothing: absent". |
| Merged | Yes | Yes | Ran: `git merge-base --is-ancestor ef5b488 main` gave `exit=1`; `git rev-parse main` printed `b1c3e3601a9d...` and `git ls-remote origin main` printed the same. So it correctly says ef5b488 is not merged, and local main matches remote. Fails on squash and rebase merges (false negative, safe direction). Clean. |
| Deployed | Yes | Yes | "The second prints the SHA you named" is tautological when the model names HEAD. Compare to the SHA `ls-remote` printed. It also does not show the process restarted: a daemon started before the pull passes both checks. Add "and the process started after it (`ps -o lstart`, or the unit's `ActiveEnterTimestamp`)" for long-running services. Probes the row names also trip on this checkout's untracked files; see rule 6 above. |

Rows with a "Holds when" that can be true while the claim is false: run landed (crash without traceback), pushed and mirror (empty output), venv (broken interpreter, wrong path), deployed (stale process, tautological SHA), tests (wrong Python). Only merged is clean.

## 7. The four-state table and the venv row

The venv row's label `observed` strains the ladder. The table defines `observed` as "The running system did the job. Output it produced after the launch." A venv is not a running system, nothing launched, and `pyvenv.cfg` is file content, which by the table's own `written` row ("The change exists in a file") is closer. The label survives only because the ladder has no cell for present state ("is there / is there not"). That is the same gap round 1 named (a negative claim is not a mismatch of states) and the table papers over it with a label.

Cheapest coherent fix, no fifth state (D2 stays closed): widen the `observed` row's "Means" to "The live system, looked at: output it produced, or its present state" and its evidence cell to "Output the run produced after the launch, or a read of the thing as it is now". Then run-landed and venv-exists both fit and no row changes labels. Also edit the `deployed` row: "pushed or merged: remote SHA equals local; installed or run from a checkout: clean tree and the SHA".

The ladder is otherwise coherent. The line "No state implies the next" is the most useful sentence in the table.

## 8. EXAMPLES.md

Does an After break a kernel rule?

- **Pair 1.** Yes, two ways. "The timer is installed (deployed)" has no `Evidence:` line (rule 4), and an install claim under rule 6 owes `git status --porcelain`. Second, `tail -2 logs/run.log` cannot yield `exit=1`; `tail` exits 0 on a readable file. The exit belongs to the run, so the command pasted does not produce the output pasted. That is the exact exit-status confusion rule 3 warns about, shown as a model. Also "the state database predates the new schema" is an inference from the error text, stated as fact.
- **Pair 2.** "One push behind" is a count the evidence does not carry; two differing SHAs show different, not one apart. Replace with "the mirror is not at origin's SHA".
- **Pair 3.** After says "so I'll use it as built". A venv that exists is not a venv that works; the `python -V` evidence does show it runs, so this is minor. Strawman check: the Before ("never built, so I'll create its venv") is plausible planning narration, not a strawman.
- **Pair 4.** Changing "fixed" into a run is right and the label `tested` is honest. A residual: `-k empty_partition` passing 2 tests does not show they fail without the fix. That is rule 3's "could prove you wrong" and the pair does not model it. Add one clause, "the same two tests failed before the change" if true, or drop the claim to "the fix is written; two new tests pass".
- **Pair 5.** The blocker is asserted, not demonstrated: "this session has none [read access]". That is a belief about access. A skipped check wears the same sentence. The After should paste the denied output of `./validate --against prod --read-only`. If that command errors with a permission message, the blocker is real and checkable; if it runs, the claim is verified. This is the pair where "UNVERIFIED is not a softener" is hardest to tell apart from a softener, so it is the pair that most needs the pasted error. The new rule 5 text states it.
- **Pair 6.** "Measured before the last three runs" is an unverified explanation inside a corrected report. Cut it, or give its evidence.
- **Pair 7.** Teaches the over-flag. Reword the last sentence: "A number you will cite or act on gets the probe; a count you will not use does not."

Strawman check: Befores 1 through 6 are plausible model prose. Pair 7 is a real slip, but "11 lines" is a claim few reports would carry, so as a teaching example it models over-evidencing more than it models a failure shape. If the line cap forces a cut, cut pair 7 first. `test_examples_hold_seven_pairs` asserts seven; the test would change.

Missing: no pair shows a clean turn. For 2d's "at most 1 of 6 clean turns flagged", the skill should show a report that needs no extra line.

## 9. Ambient cost

Least earning: the old rule 6 ("probes read; never write"). Reasons: none of the six incident turns in 2d is about a probe that wrote, so it cannot move the 2d pass; the one incident it addresses (a verification run that wrote to a production store) is a scope incident, and its enforcement belongs to the `permissions.ask` layer from my round-1 review; and a reader can only see a violation by reading the command in an `Evidence:` line, where the rule folds naturally ("with a read-only check"). Loss from folding: the rule loses its own line and some salience. Gain: the slot funds the split of rule 4 and the "absence" clause. Second least: the old rule 5 (clean tree). It fires only on deploy claims. It stays as rule 6 because D10 is closed and because it is the only rule that addresses the uncommitted-code-in-a-timer incident. Scoping it to checkouts keeps it from firing on every push.

## Recommended changes, by effect on 2d

1. Add "an absence is a claim too" to rule 1, and "or acting on an absence" to SKILL.md's scope sentence. Without it the venv shape sits outside the ambient text. (Section 2.)
2. Rewrite rule 3 to name the outcome and fold in read-only: "Check the outcome the claim names, with a read-only check that could fail; a launcher's exit 0 is not the outcome, and no error is not evidence." This is the crashed-run shape, the lead shape. (Sections 1, 4.)
3. Rewrite rule 2 to anchor on the last change: "Evidence postdates your last change to the thing claimed." (Section 1.)
4. Bound the claim in rule 4 ("under each claim a reader would act on; claims that share a check share the line"), add a one-sentence claim bound in SKILL.md, and add a clean-turn pair to EXAMPLES.md. This protects the "at most 1 of 6 clean flagged" threshold. (Section 3.)
5. Scope rule 6 to checkouts ("A checkout counts as deployed only if clean") so push claims in a repo with stray files are not voided; this checkout has five untracked files today. (Section 1.)
6. Split rule 4 (show-it; mark-unverifiable), make "paste the blocker's error" part of rule 5, and change pair 5 to paste the denied output. (Sections 5, 8.)
7. Fix the probe rows: require a printed line in pushed and mirror; add the completion-line condition to run landed; name the CI Python source in tests; define the broken-venv case and `ls -d .venv*` in venv; compare to `ls-remote`'s SHA in deployed. (Section 6.)
8. Widen the `observed` row to cover present state, so the venv label is coherent. (Section 7.)
9. Fix pairs 1 (tail cannot yield `exit=1`; missing evidence for the install claim), 2 ("one push"), 6, and 7 (cut or reword). (Section 8.)
10. Update the two shape tests that assert literal text ("this turn", "never write"). (Section 1.)

Not fixable by wording, stated once in SKILL.md: a model that picks a weak check and labels it honestly, or fabricates the `Evidence:` output, passes the letter. A reader or the Approach C verifier closes that.

**Verdict: SHIP-WITH-FIXES.** Items 1 through 5 before the 2d run; 6 through 10 can land with them at no line-cap cost (SKILL.md is 95 lines against a cap under 110).
