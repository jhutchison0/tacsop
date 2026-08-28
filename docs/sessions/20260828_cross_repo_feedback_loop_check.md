# Session: Cross-Repo Feedback Loop Check, the Bottom-Up Question Answered

**Date**: 2026-08-28
**Branch**: main
**Tags**: #session #whetstone #harvest #propagation #doctrine #complete

**Documents**: [docs/tasks.md](../tasks.md), [config/project.yaml](../../config/project.yaml)
**Implements**: [conop_whetstone_recursive_doctrine_loop.md](../plans/conop_whetstone_recursive_doctrine_loop.md) (Wave 1 window session 2 of 5; A6 falsifier read on both canaries; first non-author M3 verification, run cross-repo; D10 delta intake from stx-server)
**References**: [20260827_stx_server_lessons_harvest.md](../reviews/20260827_stx_server_lessons_harvest.md), [docs/propagation-protocol.md](../propagation-protocol.md), [docs/doctrine-updates.md](../doctrine-updates.md) (2026-08-27 entry), [traversing-the-knowledge-base/SKILL.md](../../.claude/skills/traversing-the-knowledge-base/SKILL.md), [designing-clear-data-displays/SKILL.md](../../.claude/skills/designing-clear-data-displays/SKILL.md); stx-server `docs/sessions/20260827_field_figure_review_and_capability.md`, `docs/reviews/20260828_plan_alignment_review.md` and `docs/plans/20260828_proposal_weekly_cadence_ui_and_feedback.md` (both untracked in that repo when read); veil-engine `.claude/upstream-lesson.md`
**Follows**: [20260827_figure_style_doctrine_from_stx_server.md](20260827_figure_style_doctrine_from_stx_server.md)

---

## Summary

The user presents on this repo today and asked two things: is stx-server's `designing-clear-data-displays` skill still what we copied, and how has that repo used `traversing-the-knowledge-base`, so that the session record can answer the question the presentation turns on: can doctrine be built from bottom-up feedback across repositories, and is a limited recursive self-learning loop implementable.

The skill is byte-identical to our copy; stx-server has made no commit to it since `307d195`. The traversal skill arrived in stx-server with the template on 2026-08-26 and has been used in every mode the skill describes, but its uptake metric fails there (2 of the last 5 session docs carry a line) for a reason stx-server's own reviewer diagnosed yesterday: no session-close checklist asks for the line, in that repo or in this one. The upward channel holds on the one canary that has had sessions since the seed: veil-engine wrote 6 fleet-scope lessons in two sessions and 6 of 6 reached the channel file. The loop's missing piece is acknowledgment: the hub applied stx-server's three hub-upward items the day after they were filed, and stx-server's task lines are still open because nothing told it.

The answer, in one line each: yes, bottom-up feedback works where the capture point has been shipped, at human cadence; and a limited recursion already exists and produced its first self-referential correction yesterday, when a downstream review measured the hub's traversal instrument, found it failing, and named the fix.

| Metric | Value |
|---|---|
| Skill drift, stx-server vs hub | 0 files, 0 commits since `307d195` |
| stx-server session docs with a `KB-graph:` line | 2 of 9 overall; 2 of 5 most recent (M1 threshold 3 of 5) |
| stx-server traversals recorded outside session docs | 6 in the 2026-08-28 review, 1 in the 2026-08-28 proposal, plus one check-5 run (25 paths, 0 MISSING) |
| M3, non-author verification of stx-server's two lines | 2 of 2 pass (verified by this session, cross-repo) |
| veil-engine A6 | 2 organic sessions since the seed; 6 fleet-marked lessons in the docs, 6 in the channel file |
| tactics-game A6 | 0 sessions since the seed; no data |
| stx-server upward items, filing to hub application | 1 day (tasks.md convention, no channel) |
| veil-engine upward lessons, first write to today | 13 days, captured, unharvested |
| Delta harvest since `307d195` | 8 lessons: 6 OBSERVED, 1 PARKED, 1 NOOP |
| Hub Wave 1 window | session 2 of 5 |
| Em dashes added | 0 |

## Work Completed

### 1. The skill check

`KB-graph: git log 307d195..HEAD -- .claude/skills/designing-clear-data-displays/ in stx-server, then diff -r against the hub's copy → 0 commits, 0 differing files; nothing to re-copy`

stx-server's one session since our copy (`ed87986`, 2026-08-27 afternoon) applied the skill rather than editing it: the REVIEWING pass over twelve field figures found 1 Major (rule 7, no scale on the picture; week 7's list carried no number either) and 3 Minor (rule 4, two labels on their own strokes in week 2). The fix amended the field map plan's D7 override, which had passed two gates on the premise that the list carried every number. That is lesson 1 of the delta harvest in section 4 and it belongs to the skill's `REVIEWING.md`, not to stx-server.

### 2. How stx-server uses the traversal skill

The skill reached stx-server inside the template (bootstrapped 2026-08-26 from `7074f90`, which postdates the skill's merge at `9b12917`). Its `/pcc` check 5 carries the hub's M2 recording rule verbatim. Every use mode the skill names appears in that repo's corpus:

| Mode | Instance | Named an artifact then edited? |
|---|---|---|
| Backlinks before a design move | `20260826_wave3_coach_recommender.md`: backlinks of the hub's `pillars.md` (16 dependents) plus elephant-graveyard's `CONTEXT.md` reading order → `docs/design/pillars.md` created in the sibling's shape, three agents repointed | Yes: the doc narrates the traversal, then "Changed:", then the lead's approval |
| Neighbors before filing a task | `20260826_field_map_wave.md`: neighbors of FR-3, `field_configs`, `geometry` → the task entry rewritten twice before any agent ran (`layout` is a glossary avoid-word; fit is measured at render, not validated at load) | Yes: "changed the entry twice before any agent ran" |
| Backlinks to rule out a design option | `20260828_proposal_weekly_cadence_ui_and_feedback.md`: backlinks of `weekly_rhythm` → `log_form.html:13` reads the same map, so no `sun` key (Design Decision 5) | Yes, within the proposal |
| Lineage, typed edges, blast radius, forward search, amendment trail, check 5 | `20260828_plan_alignment_review.md` Method section: seven bullets, six traversals and one check-5 run | The review is a plan review; its edits are the recommended Status Log entry and the sequencing, not yet made |

`KB-graph: forward search for "KB-graph" across every stx-server .md → 2 session-doc lines, 1 proposal line, 8 review lines, and the review's own uptake note; the counts above, and the tasks.md WHETSTONE line edited from them`

**M1 in stx-server.** Counted by the skill's own grep: `wave3` 1, `field_map_wave` 1, the other seven 0. The five most recent score 2 of 5. stx-server's reviewer measured the same number yesterday (C5) and gave the cause: COMPASS, the Tufte skill session, and the figure session each traversed heavily and recorded nothing, and the session-close checklist never asks. The hub's `.claude/commands/session-end.md` and `docs/session-doc-format.md` do not ask either; the hub's own 1 of 1 so far is author discipline, not the checklist.

**M3, first non-author verification, cross-repo.** Both stx-server lines pass: each traversal precedes the edit in the record's own order and the edit carries the traversal's content (the sibling's pillars shape; the glossary's avoid-word). Verified by reading, not by commit timestamps, since a traversal leaves no commit. This is the first M3 check by someone other than the line's author anywhere in the fleet, and it happened across a repo boundary.

### 3. The upward channels, all three repos

| Repo | Channel | Organic sessions since seed or bootstrap | Fleet lessons written | Captured in channel | Reached the hub | Latency |
|---|---|---|---|---|---|---|
| veil-engine | D10 file, seeded 2026-08-15 | 2 (08-15, 08-21) | 6 marked `(fleet)` in the docs | 6 of 6 | Read today, not yet routed | 13 days and counting |
| tactics-game | D10 file, seeded 2026-08-15 | 0 | 0 | n/a | n/a | no data |
| stx-server | none (bootstrapped after the seeds); three `tasks.md` "Hub upward" lines | 9 | 3 items + 33 harvested lessons | n/a | Applied 2026-08-27 | 1 day |

`KB-graph: veil-engine's two session-doc Lessons sections (fleet-marked entries) against .claude/upstream-lesson.md → 6 of 6 present; A6's kill criterion (two consecutive sessions whose fleet lessons the convention fails to capture) not met; recorded on the WHETSTONE task`

`KB-graph: grep "Hub upward" in stx-server docs/tasks.md, then grep "upward|tasks.md" in the hub's 2026-08-27 entry → three lines still open one day after the hub applied all three; the entry names stx-server six times and never says so; task filed (section 5)`

The one-day latency in the stx-server row is the known-good class in E6, and it is also the failure mode D10 exists to replace: it was fast because the operator was in both repos on consecutive days and carried the items by memory. The 13-day row is the channel working as designed and the hub's harvest cadence being the bottleneck.

### 4. Delta harvest, stx-server since `307d195`

`KB-graph: Follows chain in stx-server from 307d195's session doc to ed87986's, plus the two untracked 2026-08-28 docs → one session doc with five lessons and one review with two; harvested below`

Schema per WHETSTONE D9, provenance per D10. The 2026-08-27 harvest holds lessons 1 to 33; these continue the numbering.

34. `LESSON (OBSERVED): A plan's stated override of a figure rule holds only while its premise does; re-run the rule's test at every gate instead of citing the override | evidence: stx-server field map D7 ("no distances in the picture; the list is the legend") passed two gates, then failed on week 7 whose list carried no number; D7 amended 2026-08-27 | scope: fleet | owner: .claude/skills/designing-clear-data-displays/REVIEWING.md | verdict: UPDATE | origin: stx-server/docs/sessions/20260827_field_figure_review_and_capability.md`
35. `LESSON (OBSERVED): Choose between candidate redraws from a mock rendered in the target medium, not from prose; four options argued in words were decided in one look at the injected page, and the gate rendered the branch the same way | evidence: stx-server mock.py and shot.py kit; the three before/after pairs sent to the lead | scope: fleet | owner: .claude/skills/designing-clear-data-displays/REVIEWING.md (before/after pairs are rendered, not described) | verdict: UPDATE | origin: stx-server/docs/sessions/20260827_field_figure_review_and_capability.md`
36. `LESSON (OBSERVED): A challenge that runs the proposal's own code path beats one that reads the proposal; running the placer over week 11's thirteen items gave the number (six overprints) and the reason (a missing candidate family) | evidence: stx-server/docs/reviews/20260827_field_figure_capability_challenge.md; second independent instance in two days after the hub's 2026-08-27 lesson 3 (the pre-flight that re-ran the hook regex) | scope: fleet | owner: .claude/agents/code-reviewer.md (challenge protocol: execute what the proposal claims) | verdict: UPDATE | origin: stx-server/docs/sessions/20260827_field_figure_review_and_capability.md`
37. `LESSON (PARKED): pkill -f <pattern> matches the shell whose own command line carries the pattern and kills the caller mid-script; kill by pid from ss, and keep state changes and verification in separate calls | evidence: stx-server's merge-then-restart script killed itself after the merge | scope: fleet | owner: none in the hub today; expiry at the Day-1 playbook rewrite, whose deployment section is the home | verdict: PARK | origin: stx-server/docs/sessions/20260827_field_figure_review_and_capability.md`
38. `LESSON (NOOP): A merge that touches a Jinja2 template breaks a running uvicorn until restart | evidence: 500s on every card the morning after the merge | scope: repo (stack-specific; stx-server recorded it as a known issue) | origin: stx-server/docs/sessions/20260827_field_figure_review_and_capability.md`
39. `LESSON (OBSERVED): The traversal skill's uptake metric fails where the session-close checklist never asks for the KB-graph line; three sessions that traversed heavily recorded none, and the hub's own session-end and doc format do not ask either | evidence: stx-server 2 of 5 (review C5); hub .claude/commands/session-end.md and docs/session-doc-format.md grep empty for KB-graph | scope: fleet | owner: .claude/commands/session-end.md, docs/session-doc-format.md, .claude/skills/traversing-the-knowledge-base/SKILL.md (the M1 < 3 escalation rung names /session-start; the evidence says the close checklist is the rung) | verdict: UPDATE | origin: stx-server/docs/reviews/20260828_plan_alignment_review.md`
40. `LESSON (OBSERVED): Every unplanned unit checked itself against the plan's resolutions and none against its calendar; the OPORD's Status Log stopped at Checkpoint 3 while four units shipped and the last wave went unlaunched three days before the season | evidence: stx-server review H1, C4, section 5 (about 4.3M agent tokens outside the plan against 1.4M inside it) | scope: fleet | owner: docs/plans/OPORD-FORMAT.md (a unit shipped outside the waves gets a dated Status Log entry the same session; the first-contact rule gains a calendar check) | verdict: UPDATE | origin: stx-server/docs/reviews/20260828_plan_alignment_review.md`
41. `LESSON (OBSERVED): D10 specifies credit (the entry names the origin) but not acknowledgment (telling the origin its item landed); stx-server's three hub-upward task lines stand open a day after the hub applied all three, and the 2026-08-27 entry names stx-server six times without saying so | evidence: stx-server docs/tasks.md Hub upward lines; grep of the entry for "upward" empty | scope: fleet | owner: docs/propagation-protocol.md and CONOP WHETSTONE D10 (Wave 4's acknowledgment ledger is the downward half; the upward half needs its mirror) | verdict: ADD | origin: this session`

Lesson 39 is the one to show. A downstream repo measured the instrument the hub uses to improve its doctrine, found it under threshold, named the cause, and proposed the fix; the hub's own checklist has the same hole. That is the recursion operating on itself, one hop below the hub, with no mechanism beyond a reviewer reading the skill's success criterion.

### 5. The loop-closure gap

The hub's side of D10 is done for stx-server: the skill, the tools line, and the hook fallback are applied and the entry credits the origin by name. The origin does not know. Its three task lines are open, its latest session doc lists "the hub-upward tasks" as unchanged, and the entry that will land in its `.claude/upstream-update.md` does not tell it to close them. Filed as a P3 task with the cheapest fix named: one acknowledgment line in the entry before it goes live, and a protocol rule that every entry carrying a harvested lesson names the origin's task or channel line it closes.

### 6. The answer

**Can doctrine be built from bottom-up feedback across repositories?** Yes, and the last two days are the evidence: 41 lessons from one downstream repo, three of them already fleet doctrine (the skill, the tools line, the hook fallback), and 6 more waiting in another repo's channel file. The conditions, each observed rather than assumed:

- The capture point must ship with the template. veil-engine had it and captured 6 of 6; stx-server did not and carried its items as task lines a human found by reading.
- Latency is set by the hub's harvest cadence, not by capture. One day when the operator was in both repos; 13 days and counting when nobody ran a hub session.
- The loop needs an acknowledgment leg. Credit exists (D10's incentive half); "your lesson landed, close your line" does not.

**Can a limited recursive self-learning loop be implemented?** A limited form is running now. Its shape: downstream sessions write lessons in a greppable schema; the hub harvests, routes each to an owner artifact, and ships the change back through the propagation channel; the instrument that does the routing (the traversal skill) carries its own falsifiable metric, and yesterday a downstream review scored that metric, found it failing, and named the fix (lesson 39). Every hop is a human running a session, which is the design (WHETSTONE Approach B: convention first, mechanisms behind evidence). What does not exist yet, stated so the claim stays honest: automatic harvest (the hub reads the channel only when a hub session runs), the acknowledgment leg, and any lesson at `LEARNED` (D1 requires verified use plus a human flip; the count today is zero). The presentation's defensible sentence: bottom-up capture works where the capture point has been shipped, the loop closes at human cadence, the first recursive correction has occurred, and nothing is LEARNED yet.

## Key Decisions

| Decision | Rationale |
|---|---|
| Record the delta harvest in this session doc, not a second review doc | Eight lines continue the 2026-08-27 harvest's numbering and stay greppable by `LESSON (`; a second harvest file for one session's delta is a shallow module. |
| Verify stx-server's M3 lines by the record's order, not commit timestamps | A traversal leaves no commit; the doc's narrative order plus the edit carrying the traversal's content is the evidence the skill's standard admits. Stated as the method so the next verifier can disagree. |
| Read veil-engine's channel file for the A6 result; do not harvest it today | The harvest is a filed task with its own routing work; today's question needed the capture rate, which the read gives. |
| File the acknowledgment gap as a task; do not edit the pre-flighted entry silently | The entry passed a pre-flight and a dry run. Adding the line is one edit and the user's call before the live run. |
| Lesson 37 PARKED rather than routed | The hub has no ops runbook; the Day-1 playbook rewrite is open and owns deployment. PARKED with a named expiry is D1's honest state for a lesson with no owner today. |

## Lessons

1. **A downstream reviewer reading the skill's success criterion is the cheapest self-measurement the loop has.** stx-server's C5 cost nothing to produce and gave the hub a metric result plus a cause plus a fix. The hub should ask reviewers to score any doctrine instrument that carries a criterion, as part of the review's Method section. `LESSON (OBSERVED): plan and gate reviews should score any doctrine instrument whose SKILL.md carries a falsifiable criterion, in the Method section | evidence: stx-server review C5; this session's lesson 39 | scope: fleet | owner: .claude/agents/code-reviewer.md | verdict: ADD`.
2. **Cross-repo verification is the M3 check the CONOP asked for and could not get in-repo.** The Wave 1 task says "someone other than its author"; on a one-person hub that meant a later session by the same person. A sibling repo's lines, read by the hub, are a non-author check by construction. Record it as the method at window close.
3. **The two canaries are one canary.** tactics-game has had no session since the seed. A6's evidence base is veil-engine alone; say so at the Wave 1 report rather than counting two.

## Pillar Compliance

- **Shift-Left**: no code changed; the suite ran green at session start (278) and the audit hook had nothing to watch.
- **Simplicity First**: one session doc, three task-line edits, one new task line, the state block; no new file besides this one.
- **Config-Driven**: `project.yaml` state updated to what is true; no semantics changed.

## PCC Results

Session start: 278 passed, 1 expected warning, 3.29s; `main` in sync with `origin/main`; five untracked March docs (the P3 task), unchanged.

Session close, over the working tree:

```
[PASS] No secrets; no .env touched
[PASS] Tests: 278 passed at session start; no source or test file changed since
[PASS] No debug artifacts
[INFO] Branch: main, 0 ahead of origin before this session's commit
[PASS] Reference integrity: 21 paths checked, 0 MISSING (metric M2)
[PASS] Gate separation: no gate surface touched
[PASS] 0 em dashes added; config/project.yaml parses
```

## Commits

- `[doc]` Cross-repo feedback loop check: stx-server skill drift 0, traversal-skill scan, A6 read, delta harvest 34 to 41, acknowledgment gap; task list and state block (this record rides the same commit).

## Next Steps

- [ ] User: the live propagation go is still pending (dry run 16 repos). Before it, decide whether to add the one acknowledgment line to the 2026-08-27 entry so stx-server closes its three lines on receipt.
- [ ] Harvest veil-engine's six lessons (task filed 2026-08-27; captured 6 of 6, unharvested 13 days).
- [ ] Route lessons 34 to 41 at the next doctrine cycles: 34 and 35 to the figure skill's `REVIEWING.md`; 36 and this session's lesson 1 to the code-reviewer; 39 to session-end, the doc format, and the traversal skill's escalation rung; 40 to `OPORD-FORMAT.md`; 41 to the propagation protocol.
- [ ] WHETSTONE Wave 1: session 2 of 5. Five `KB-graph:` lines above; four named artifacts then edited (M3 candidates). The cross-repo M3 method from lesson 2 goes in the window-close amendment.
- [ ] Decide the five March docs; 0.2.0 cut; the rest of the task list unchanged.
