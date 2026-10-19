# Review: CONOP SEXTANT, proposer, debate round 1

**Date**: 2026-10-05
**Subject**: `docs/plans/conop_sextant_doctrine_evaluation_repository.md` (Draft), with the OVERWATCH Status Log entry of 2026-10-05 and gaps G8, G9.
**Verdict**: **SHIP-WITH-FIXES.** The direction is right: measurements leave the hub's prose, and the transcripts are saved first. Finding 1 is a defect in the one step with a deadline. Findings 2 to 5 change the plan's shape.

## Findings, most important first

### 1. Task 0a's stopgap value is rejected by the installed Claude Code (Critical)

The plan sets `cleanupPeriodDays: 0` (plan line 164, line 129; gap G8 in `docs/gaps.md:16`) on the reading that 0 turns deletion off. Public issue reports say otherwise. In an old release 0 silently stopped transcripts from being written; since v2.1.89 the minimum is 1 and 0 fails validation, so a "never clean up" setting needs a large value such as 36500 (sources below, via web search; I could not open the settings reference's detailed entry, the fetch returned only the table row).

Evidence: `claude --version` on this box prints `2.1.289 (Claude Code)`, which is past 2.1.89. The plan's own Standard ("fist's oldest transcript still dated 2026-09-15 after the next session start") would catch a failure only after the fact, and a validation error may reject the whole settings file, not only the key.
UNVERIFIED: the behavior on 2.1.289 itself. I did not edit `~/.claude/settings.json`; the lead should test the value in a scratch settings file with `claude --settings`, or read the entry's text, before the user is asked to say yes.

Fix: write the value as a large positive integer (the plan can name 3650 days), and make the Standard "the key is accepted and the oldest transcript survives a session start".

### 2. Wave 0 is gated on the wrong things, and the copy needs neither the repo nor the NAS (High)

The deadline is 2026-10-15. Last-modified dates of fist's 10 top-level transcripts: 2026-09-15, 09-19 (2), 09-25 (4), 10-01, 10-04 (2) (`find ... -printf '%TY-%Tm-%Td'`, 2026-10-05). The first two go within days of 10-15, and four more within 10 days after.

- Task 1b (the copy) waits on 1a (the repo) and 0b (the topology doc). Neither is needed to stop the loss. `cp -an` of fist's directory to a local directory outside every checkout is additive (D5), takes a minute, and fits A4's own fallback ("keep copies local until the store answers"). Do it first, today, and move it to home storage when 0b lands.
- Task 0c (debate and approval) heads Wave 0 but gates nothing about a non-destructive local copy. Approval should gate the repository, not the rescue.
- The 1b Standard "a second run copies 0 files" is wrong for a live store. A session's transcript grows while the session runs and when it resumes. `--ignore-existing` semantics freeze a partial copy; "copy when size or mtime differs" overwrites a prior version, which D5 and HOME-STORAGE rule 2 call out. Choose one and test it: copy to a name that carries the source's size and mtime, never overwrite a name, and let the collector read the newest.

### 3. A new repository is not yet earned; sequence it behind a throwaway spike (High)

Approach B may be the right end state, and I would not reject it. I would not build it first, because the plan's only scored, hard measure (Wave 2) is the one whose viability is unknown (A1, A2), and the Wave 1 measure is a `jq` pipeline.

Strongest alternatives the draft did not list:

- **Approach E: copy first, repo on evidence.** Waves 0 and a retention copy (a `SessionEnd` hook or a 20-line script on a timer, written once, outside git or in the user's dotfiles) preserve inputs. The A4 counts are `jq` over the copy, one command per pattern, with the command printed beside the number so it re-runs. Run the Wave 2 spike (rubric, A2, A1) in scratch. Create the repository only if A1 and A2 pass, because the repository is justified only if a tested estimator exists. This costs the repo's tests for 1c and delays the "one home for all plans' measures", which has no consumer until a second measure is ready (D8 already concedes this).
- **Approach F: use the existing trainer.** `stx-server` is on this box and already has a log-and-recommend loop (`~/projects/github/stx-server` has `app/`, `docs/`, no evaluation code). I would not merge them, since its subject is a different domain, but the plan should say in one sentence why shape-borrowing beats reuse.
- **Approach G: a directory in the hub with the scope declared per directory.** Rejected on the plan's own reasoning (the hub is work-scoped by default, `HOME-STORAGE.md:20-22`). It stays rejected, and the draft's Approach A already covers it.

What I would cut from the draft: Approaches C and D as written (C is rejected by quoting OVERWATCH's own text, D is the user's earlier option and the plan answers it in two lines); D9 and O3 to O5 until a second measure exists; Wave 3's list. What I would keep: D1 to D8, since D3 (one instrument for both windows) and D5 (additive copies) are the plan's strongest content.

### 4. The exclusion is a deny-list, so it fails open on every project not yet named (High)

D4 and task 1a stop a collector from reading `assay` by an exclusion list. The directory holds 21 or more project subdirectories under `~/.claude/projects`: top level counts are fist 10, tacsop 9, stx-server 8, propter 6, daily-weather 6, assay 6, cad-dnd-minis 4, veil-engine 3, schelling-point 2, and more with fewer (`find` per directory, 2026-10-05). A project outside the list, such as `-home-jhutchison-projects-sony`, has no scope the collector can read from the directory name, and the path encoding replaces `/` with `-`, which makes a name ambiguous.

Fix: an allowlist. The collector copies a named set (`fist`, then `propter`, then hub sessions for A2) and reads each project's `scope` from its checkout's `config/project.yaml`, stopping when the file is absent. The fail-closed test then reads: a new, unlisted project directory is never opened. The current "sentinel in an excluded fixture" test only proves the one named case.

Also: the plan quotes `assay` at 5 transcripts (line 34, "last modified 2026-10-03 and 10-04"). The count is now 6 and the file times include today, a day after the draft. That is the drift the plan sets out to catch, so the cure is to name the universe (top-level or including subagent files) and the stamp in each count. The totals show the problem: 287 `.jsonl` files exist now, and 232 of them are under `subagents/` (`find . -name '*.jsonl' -path '*subagents*'`). The plan's "173 versus 285" known-bad reference does not say which universe it counted, and the current count is 287, not 285.

### 5. A2 is not a valid calibration of a "user caught it" scorer (High)

The 29 is verified as a sum: the three session docs' Appendix A tables list 16, 5, and 8 refuted claims (`docs/sessions/20261001_overwatch_wave2_verifying_claims.md:172`, `20261004_common_operating_picture_at_the_hub.md:246`; the 10-02 doc's table reports 5 at line 35). The use is the problem.

- **Different event class.** The ledger separates M (a reviewer's re-run refuted it) from N (the user caught it) on purpose (Status Log entry `447a459`, 2026-10-01). MOE 1 reads N only. A2 calibrates an N scorer on M events. A scorer that flags a claim "the user later challenged" will find few of these, since the doc says the user did not act on items 1 and 2 of the 10-04 list. It would fail A2 for the wrong reason, or pass by flagging any wrong-looking claim, which is a different instrument.
- **Written artifacts, not conversation.** Of the 16 in the 10-01 table, the "Where" column lists commits, the Status Log, `SKILL.md`, and `docs/tasks.md` for most rows. The scorer reads a transcript; those claims sit in Write and Edit tool inputs and a commit message, a reachable but different surface from "claims made to the user".
- **Selection and hindsight.** The author of the sessions wrote the lists, and the rubric writer reads them first. A rubric tuned on a known answer key passes A2 by construction; the plan has no held-out set.
- **No negative set.** "More than 1 in 10 held claims flagged" needs a labelled population of held claims. The Claims tables exist in some docs, but the plan names no source or count.
- **Thresholds.** 20 of 29 on a population where 16 come from one session has an interval wide enough to pass or fail a rubric by luck (binomial 95% interval on 20 of 29 is roughly 0.49 to 0.84). State the pass as a lower bound or a split by session.

Fix: keep A2 as a smoke test of the claim detector (does it find claim-like statements that a reviewer refuted), rename it, and calibrate the N-scorer on what N actually is: user turns that contest an earlier assistant statement. fist's 10 transcripts hold 799 array-shaped and 81 string-shaped user messages (`jq`, 2026-10-05), so a deterministic "user correction candidate" pre-pass (user message directly after an assistant statement, hand-labelled once by the user) gives a labelled set from the real population. This also supplies the cheaper first instrument: the number of user-contest turns per session, counted without a model.

### 6. A1's design and bar need two changes (Medium)

- **Unit of agreement.** Cohen's kappa "on per-claim labels" needs both scorers to agree first on what the claims are. Segmenting free text into claims is where the plan's own Enemy Forces says scorers misfire. Pre-segment: label candidate turns (the user-contest turns from finding 5), then kappa is defined on a fixed list.
- **Prevalence.** If most of the 10 sessions hold zero or one caught claims, kappa is unstable (high agreement with low prevalence can still give a low kappa). Report raw agreement and the positive-label counts beside kappa, and set the sample as claims, not sessions.
- **Scorer independence.** "One agent run" as the second scorer shares a model family with the author of the kernel under test. The plan leaves the choice to Wave 2 detail. Decide now: the user labels the A1 set (about 10 sessions is an evening's work with candidate turns pre-listed), and an agent labels it blind; then the agent is validated against the user, which is the only calibration with a human ground truth.
- **Baseline size.** fist has 10 transcripts and 15 session docs, so a pre-kernel window of at most 10 sessions exists, and the after-window needs 20 (OVERWATCH MOE). That is a comparison of rates on 10 versus 20 sessions, with an interval the plan promises but does not size. State the smallest drop the design can detect, and say now that a failure to detect is the likely result.

### 7. What the plan details too early, and too late (Medium)

- **Too early**: Wave 1's task 1c names OVERWATCH task 1e's seven patterns and "the lead decides which patterns ship", while falsifier A4 depends on them. Wave 3's list and O5 are speculation. The Terrain's per-project counts will be stale in a week; drop them from the plan and let the first render carry them.
- **Too late**: the privacy handling of the copy (transcripts include tool results, so a copy can hold secrets a session cat-ed) appears only as "no transcript text in git". It also needs a mode and an owner on the share, and a statement of who can read the store. And 0b, the topology doc, is a P3 task that the plan promotes to a blocker with no owner date earlier than 10-14. Move the A4 check ("a listing returns without error") to day 1, since an unreachable store changes Wave 1 entirely.
- **Gate order**: the exit criterion of Wave 1 says OVERWATCH's Status Log cites rendered lines "by stamp", but OVERWATCH's own date is 2026-10-16 and the plan's mission is 10-23. State which date moves.

### 8. Smaller points (Low)

- Terrain says the hub's checkout has no `project.scope` (`config/project.yaml:9` shows only a comment describing the key). That matches the plan.
- The stx-server citation (`docs/reviews/20260827_stx_server_lessons_harvest.md`) was not re-run; UNVERIFIED because I did not read it. I did check that fist reads `HOME_CORPUS_ROOT` (`~/projects/github/fist/CONTEXT.md:35`, `.env.example:13`): confirmed.
- "No em dash" style and the claim lines are in good order; the plan's own claims that I re-ran hold: fist session docs 15, fist transcripts 10, fist oldest 2026-09-15, `cleanupPeriodDays` absent from `~/.claude/settings.json` (grep prints nothing; the project-local settings file does not exist on this box).

## Falsification runs (2026-10-05)

| Plan claim | Run | Result |
|---|---|---|
| fist has 10 top-level transcripts, oldest 09-15 | `find` with `-printf` on the fist directory | holds |
| `assay` has 5 transcripts | `find` count in its directory | 6, refuted (drift within a day) |
| 285 `.jsonl` files on 10-05 | `find ~/.claude/projects -name '*.jsonl'` | 287; 232 of them under `subagents/` |
| 29 refuted claims in three hub sessions | Appendix A tables | 16 + 5 + 8 = 29, holds, but 4 of the 16 are from a cleanup review in the same session, not the Wave 2 work |
| `cleanupPeriodDays` is set nowhere on this box | `grep` over user settings | holds |
| 0 turns deletion off | version check plus public issue reports | refuted for 2.1.89 and later; UNVERIFIED on 2.1.289 itself |

## Sources

- https://github.com/anthropics/claude-code/issues/23710 (0 disabled transcript persistence)
- https://github.com/anthropics/claude-code/issues/41800 (settings reference versus validation behavior)

## Order of work I would run

1. Verify the retention value in a scratch settings file; set a large positive integer with the user's yes (finding 1).
2. Copy fist, then propter, to a local directory outside git, by allowlist, with versioned names (findings 2 and 4).
3. Run the Wave 2 spike in scratch: user-contest candidate turns, the user's labels, an agent's blind labels, kappa with prevalence (findings 5 and 6).
4. Create the repository when step 3 reports, and put the A4 `jq` counts in it as its first tested collector (finding 3).
