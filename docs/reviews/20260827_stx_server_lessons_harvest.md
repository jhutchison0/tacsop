# Harvest: stx-server Lessons, Eight Sessions in Two Days

**Author**: session lead (Claude), harvesting for the hub
**Date**: 2026-08-27
**Type**: Lessons harvest (CONOP WHETSTONE D10 intake, first instance from a non-canary repo)
**Origin repo**: `stx-server` (`~/projects/github/stx-server`), bootstrapped 2026-08-26 from tacsop `7074f90`; 135 commits and 8 session docs by 2026-08-27 10:08
**Method**: the traversal skill's recipes, not keyword search. Started from the skill's backlinks (15 files), walked the 2026-08-27 session doc's typed edges (Implements the proposal; References two challenges and three gates), then the Follows chain back to the bootstrap, then every `## Lessons` section and every line mentioning the hub.

## Verdict

Thirty-three numbered lessons, thirty-two of them fleet-scope, plus four repo-scope notes. Eight are applied in the hub this session (IDENTIFIED: routed and the artifact changed, awaiting the human's endorsement and one verified use before anyone flips them to LEARNED per WHETSTONE D1); twenty-one are routed to a named owner artifact for a later cycle (OBSERVED, verdict UPDATE or ADD); four are NOOP with the reason stated; the repo-scope notes are recorded so the tail is visible (D9: failures and no-lesson dispositions are first-class). The headline export is the skill itself: `designing-clear-data-displays` 1.1.0, copied whole.

stx-server never had the D10 channel (session-end Step 5.5 exists only in the two canaries), so it filed its three hub-upward items as `docs/tasks.md` lines. The hub found them by reading that file one day later. That is not an A6 failure; it is a coverage finding, recorded as a task.

## What the repo is doing

An STX (situational training exercise) trainer: a LAN-only FastAPI app that runs one program, a 14-week FLL SPIKE Prime home practice season for one middle schooler starting 2026-08-31, logs what happens, and recommends a tier each week by rules. Five pillars (Simplicity First, Shift-Left, Config Drives Content, Append-Only History, Kid-First UX), three ADRs, one OPORD (BEACON, four waves, three shipped), one CONOP (COMPASS, Wave A shipped), 269 tests, ruff clean. Every wave ran the same loop: proposer writes, code-reviewer challenges with a prototype, the lead records numbered decisions under the proposal, a builder builds test-first on a topic branch or worktree, the code-reviewer gates with mutation runs and a probe script, the lead fixes or overrules each finding by number, merge, session record. The Tufte skill came out of that loop on the second day, built to settle a filed label-collision task, and was then reviewed by an outside agent and patched to 1.1.0 the same morning.

## The lessons

Schema per WHETSTONE D9 and the D1 status ladder, with D10 provenance. `IDENTIFIED` means routed and the artifact changed this session; `OBSERVED` means routed, not yet applied. Only a human flips a line to `LEARNED`, after the change is verified in use.

### A. Applied in the hub this session

1. `LESSON (IDENTIFIED): Tufte's material belongs in a Level 0 skill of eight one-line rules with sources and tests, the shape of the prose kernel, not in a persona or an agent | evidence: stx-server/.claude/skills/designing-clear-data-displays/, 34 quotations verified by fetch across three reviews | scope: fleet | owner: .claude/skills/designing-clear-data-displays/ (copied whole, 409 lines, byte-identical) | verdict: ADD | origin: stx-server/docs/sessions/20260827_tufte_skill_and_label_placement.md`
2. `LESSON (IDENTIFIED): A tools: line is capability, not project knowledge; Level 0 agents may gain WebSearch and WebFetch without breaching the keep-unchanged rule | evidence: stx-server/docs/reviews/20260827_tufte_skill_proposal_challenge.md C9; the ledger it enabled | scope: fleet | owner: .claude/agents/proposer.md, .claude/agents/code-reviewer.md, .claude/README.md | verdict: ADD | origin: stx-server/docs/tasks.md (hub-upward, 2026-08-27)`
3. `LESSON (IDENTIFIED): Name-only test-partner matching produces noise and noise gets ignored; fall back to an import grep before logging MISSING_TEST | evidence: 27 false MISSING_TEST lines in one wave; stx-server commit 62f20a1 | scope: fleet | owner: .claude/hooks/post-tool-shift-left-audit.sh, .claude/skills/shift-left-testing/ENFORCEMENT.md, tests/unit/test_shift_left_hook.py | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_m1_close_to_m2_merge.md lesson 3`
4. `LESSON (IDENTIFIED): The prose skill and the figure skill need a stated hand-off: a chart that could be a table or a sentence is the figure skill's pre-question, not the prose skill's tokens to cut | evidence: stx-server/docs/plans/20260827_proposal_tufte_skill_feedback_round.md D24 | scope: fleet | owner: .claude/skills/writing-simple-and-direct/SKILL.md (1.0.1) | verdict: UPDATE | origin: stx-server/docs/reviews/20260827_tufte_skill_feedback_round_gate.md C2`
5. `LESSON (IDENTIFIED): The framework's one-sentence description rule contradicts two shipped skills that carry three; the rule was the fiction | evidence: writing-simple-and-direct and designing-clear-data-displays frontmatter | scope: fleet | owner: .claude/skills/SKILLS_FRAMEWORK.md (Description rules) | verdict: UPDATE | origin: stx-server/docs/reviews/20260827_designing_clear_data_displays_gate.md C8`
6. `LESSON (IDENTIFIED): Hub-copied docs carried running-prose em dashes that a downstream repo with a stricter rule could neither keep nor fix without forking doctrine | evidence: stx-server/docs/reviews/20260826_bootstrap_audit.md CONCERN-4; 27 in-sentence dashes in CONOP-FORMAT.md, OPORD-FORMAT.md, session-doc-format.md, .claude/README.md | scope: fleet | owner: those four files | verdict: UPDATE | origin: stx-server/docs/reviews/20260826_bootstrap_audit.md`
7. `LESSON (IDENTIFIED): A Level 0 sidecar that says "in this repo" and names hub scripts reads as a spec downstream | evidence: shift-left-testing/SCRIPTS.md line 3 | scope: fleet | owner: .claude/skills/shift-left-testing/SCRIPTS.md | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_bootstrap_from_tacsop_template.md Next Steps`
8. `LESSON (IDENTIFIED): The hub's own skill inventories drift: .claude/README.md listed six of nine Level 0 skills and SKILLS_FRAMEWORK.md omitted traversing-the-knowledge-base | evidence: this session's blast-radius grep before wiring the new skill | scope: repo | owner: .claude/README.md, .claude/skills/SKILLS_FRAMEWORK.md | verdict: UPDATE | origin: hub, KB-graph traversal 2026-08-27`

### B. Day-1 bootstrap lessons, routed to the playbook rewrite (open P2 task)

9. `LESSON (OBSERVED): git archive import drops the audit hook's executable bit; every fresh clone of the new repo gets a dead hook | evidence: stx-server/docs/reviews/20260826_bootstrap_audit.md HIGH-1 | scope: fleet | owner: docs/design/from_template_to_project.md | verdict: UPDATE | origin: stx-server/docs/reviews/20260826_bootstrap_audit.md`
10. `LESSON (OBSERVED): Pruning a doc at bootstrap leaves dangling references in agents and commands; grep .claude/ for the pruned path before the first review wave | evidence: three pointers to the pruned pillars.md, one in the reviewer's core instruction (HIGH-2) | scope: fleet | owner: docs/design/from_template_to_project.md | verdict: UPDATE | origin: same`
11. `LESSON (OBSERVED): Agent scope lists go stale when modules are pruned (python-prototyper still listed eight utils; one survived) | evidence: bootstrap audit CONCERN-1 | scope: fleet | owner: docs/design/from_template_to_project.md | verdict: UPDATE | origin: same`
12. `LESSON (OBSERVED): Pin the ruff ruleset explicitly; a newer ruff enables far more than the documented defaults, so local and CI disagree by version | evidence: stx-server/docs/sessions/20260826_bootstrap_from_tacsop_template.md Key Decisions | scope: fleet | owner: docs/design/from_template_to_project.md, .claude/skills/shift-left-testing/CI.md | verdict: UPDATE | origin: same`
13. `LESSON (OBSERVED): When doctrine supersedes a decision in the project's own requirements doc (uv over venv, src-layout over flat), state the supersession in the plan; do not diverge silently | evidence: bootstrap audit CONCERN-3 | scope: fleet | owner: docs/design/from_template_to_project.md | verdict: UPDATE | origin: same`

### C. Process lessons, routed to plan formats and skills

14. `LESSON (OBSERVED): Prototype at the challenge: the reviewer builds the proposed approach in a scratch copy and runs the suite before writing a finding, turning the mechanism debate into a measurement | evidence: three sessions (COMPASS lesson 1, field map lesson 1, Tufte lesson 5); 223 passed unmodified on the scratch build | scope: fleet | owner: docs/plans/CONOP-FORMAT.md (In Debate status; review weight) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_compass_wave_a.md`
15. `LESSON (OBSERVED): Print more than you assert, and read all of it: the probe script's full output found every HIGH before the review did; a 300-character excerpt hid the clipped labels | evidence: Wave 3 lesson 1, field map lesson 3, COMPASS lesson 4 | scope: fleet | owner: .claude/skills/shift-left-testing/SCRIPTS.md (a probe-script section) | verdict: ADD | origin: stx-server/docs/sessions/20260826_wave3_coach_recommender.md`
16. `LESSON (OBSERVED): Decisions interact; a brief's decision table needs one probe of each combination, not only of each decision (D5 and D11 were each right and together produced H2) | evidence: Wave 3 lesson 2, field map lesson 2 | scope: fleet | owner: docs/plans/CONOP-FORMAT.md (Lead Decisions) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_wave3_coach_recommender.md`
17. `LESSON (OBSERVED): A negative-only assertion ("X absent") is a four-wave pattern; the builder brief should require the status check and the positive neighbor beside it | evidence: Wave 2 C3, Wave 3 C2, field map C3, COMPASS C3 | scope: fleet | owner: .claude/skills/shift-left-testing/ANTIPATTERNS.md | verdict: ADD | origin: stx-server/docs/sessions/20260826_compass_wave_a.md lesson 3`
18. `LESSON (OBSERVED): A delete-each-rule mutation pass is the honest measure of "one test per rule"; seven named tests satisfied the acceptance on paper and the pass showed which failed for their own rule | evidence: Wave 3 lesson 5, field map lesson 5 (five surviving mutants found the branches no real week exercises) | scope: fleet | owner: .claude/skills/shift-left-testing/PATTERNS.md | verdict: ADD | origin: stx-server/docs/sessions/20260826_wave3_coach_recommender.md`
19. `LESSON (OBSERVED): A filed brief is a claim on features, not only on files; read the open briefs for scope before writing a wave's task table | evidence: COMPASS H2 (two items of the config-authority brief were the wave's work); field map H5 (card.py) | scope: fleet | owner: docs/plans/OPORD-FORMAT.md (wave task table) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_compass_wave_a.md lesson 2`
20. `LESSON (OBSERVED): Vocabulary rules apply to briefs: literals in a decision's own wording ("rough", "great") became code because the builder followed the decision | evidence: Wave 3 lesson 3 | scope: fleet | owner: .claude/skills/maintaining-ubiquitous-language/SKILL.md | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_wave3_coach_recommender.md`
21. `LESSON (OBSERVED): Record lead decisions in the plan at launch, numbered (D1 to Dn) under the proposal, not only in the agent prompt; the scratchpad brief dies with the session and the numbered list is what the gate judges against | evidence: every stx-server wave from Wave 2 on; 26 numbered decisions on the Tufte skill alone | scope: fleet | owner: docs/plans/CONOP-FORMAT.md (Lead Decisions block) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_m1_close_to_m2_merge.md lesson 6`
22. `LESSON (OBSERVED): A fresh-clone smoke test earns its minute every wave (it surfaced the pre-season /demo 200 that became L1) | evidence: M1/M2 lesson 4 | scope: fleet | owner: docs/plans/OPORD-FORMAT.md (checkpoint) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_m1_close_to_m2_merge.md`
23. `LESSON (OBSERVED): Tests that hand-set timestamps hide clock-source bugs; any date that reaches a user-facing calculation comes from one injected clock and its test drives the route | evidence: M1/M2 lesson 2 (L2 invisible to every unit test) | scope: fleet | owner: .claude/skills/shift-left-testing/FIXTURES.md | verdict: ADD | origin: stx-server/docs/sessions/20260826_m1_close_to_m2_merge.md`
24. `LESSON (OBSERVED): A task-condition-standard's literal example can be satisfied by a wrong implementation; each rule test should include an input the neighboring rule would get wrong | evidence: M1/M2 lesson 1 ("best not last" unfalsifiable by the example's order) | scope: fleet | owner: .claude/commands/task.md (TCS guidance) | verdict: UPDATE | origin: stx-server/docs/sessions/20260826_m1_close_to_m2_merge.md`
25. `LESSON (OBSERVED): A worktree changes the shell's ground: a cd into an agent's worktree persisted and three git commands ran there; use git -C and absolute paths whenever an agent holds a worktree | evidence: Tufte lesson 4 | scope: fleet | owner: .claude/skills/using-topic-branches/SKILL.md | verdict: ADD | origin: stx-server/docs/sessions/20260827_tufte_skill_and_label_placement.md`
26. `LESSON (OBSERVED): A source ledger that excludes is worth more than one that fills in: the proposer left two rules out rather than invent wording, and the challenge verified both within the hour | evidence: Tufte lesson 1; 23 then 34 quotations verified | scope: fleet | owner: .claude/agents/proposer.md (a verify-or-exclude line) | verdict: UPDATE | origin: stx-server/docs/sessions/20260827_tufte_skill_and_label_placement.md`
27. `LESSON (OBSERVED): When the spec lacks a value the build needs, the honest form is a provisional value in config with a named confirmation owed, never a builder's guess buried in a test | evidence: field map lesson 4 (five weeks of positions the library never states) | scope: fleet | owner: .claude/skills/configuration-management/SKILL.md | verdict: ADD | origin: stx-server/docs/sessions/20260826_field_map_wave.md`
28. `LESSON (OBSERVED): An outside review of a merged artifact by an agent that did not build it, with every claim re-verified by fetch before acceptance, found the chapter the builders skipped | evidence: stx-server/docs/reviews/20260827_tufte_skill_external_feedback.md; six points, all accepted with changes, two of its attributions corrected | scope: fleet | owner: .claude/teams/code-review.md | verdict: UPDATE | origin: stx-server/docs/sessions/20260827_tufte_skill_and_label_placement.md section 7`
29. `LESSON (OBSERVED): The template does not ship the upward lesson channel; a repo bootstrapped after the canaries were seeded had no Step 5.5 and used tasks.md lines | evidence: stx-server/.claude/commands/session-end.md has no Step 5.5; three hub-upward lines in stx-server/docs/tasks.md | scope: fleet | owner: .claude/commands/session-end.md (template copy, at WHETSTONE Wave 4) | verdict: UPDATE | origin: hub, this harvest`

### D. NOOP, with the reason

30. `LESSON (OBSERVED): Gate surfaces change alone; run the pre-commit check before every push, including lead-only doc commits that touch .claude/ | evidence: M1/M2 lesson 5 (62f20a1 bundled the hook with tasks.md) | scope: fleet | owner: .claude/commands/pcc.md check 6 | verdict: NOOP (the check exists; the lesson is compliance, and the repo's own record already carries it)`
31. `LESSON (OBSERVED): Markup-reading probes miss layout failures; a headless-browser probe at the gate of any change that draws | evidence: the 0 by 0 figure passed two gates and two probes; stx-server tasks.md P3 | scope: fleet | owner: .claude/skills/designing-clear-data-displays/ADOPTION.md step 4 | verdict: NOOP (already in the copied skill)`
32. `LESSON (OBSERVED): Em dashes in code comments and .gitattributes in hub files | evidence: bootstrap audit HIGH-4 (test_logger.py, the hook, .gitattributes) | scope: fleet | owner: .claude/skills/writing-simple-and-direct/RULES.md (rule 8 scope) | verdict: NOOP (prose rule 8 governs running prose; a downstream with a stricter rule edits its project-authored copies, and imported Level 0 sidecars stay unmodified per doctrine)`
33. `LESSON (OBSERVED): Order tasks by the deadline even when the build takes a day | evidence: COMPASS lesson 5 | scope: fleet | owner: docs/plans/OPORD-FORMAT.md | verdict: NOOP (the format's first-contact rule and validate-before-detail already order by risk; deadline is a risk)`

### E. Repo-scope, recorded for the tail

- Soft obstacle tiering on a narrow mat (labels hard, shapes soft); "state the tiering; a builder given 'avoid squares' writes the hard rule." Repo-scope: the mechanism is general, the rule is that repo's. Origin: Tufte lesson 3.
- Rule 4 has two costumes (label over label, label over stroke); the browser caught what the label-only unit test could not. Folded into 31. Origin: Tufte lesson 2.
- A non-nullable column touches every direct constructor; free before the season, a migration after. Origin: Wave 3 lesson 4.
- "Nothing else" is a decision too: a constraint written to keep a wave small produced a figure taller than the screen. Folded into 16. Origin: field map lesson 2.

## Routing summary

| Owner artifact | Lessons | Verdict |
|---|---|---|
| `.claude/skills/designing-clear-data-displays/` | 1, 31 | ADD (done), NOOP |
| `.claude/agents/proposer.md`, `code-reviewer.md`, `.claude/README.md` | 2, 26 | ADD (done), UPDATE |
| Audit hook + `ENFORCEMENT.md` + hook tests | 3 | UPDATE (done) |
| `writing-simple-and-direct/SKILL.md` | 4 | UPDATE (done, 1.0.1) |
| `SKILLS_FRAMEWORK.md`, `.claude/README.md` trees | 5, 8 | UPDATE (done) |
| Four template-copied docs (em dashes) | 6 | UPDATE (done) |
| `shift-left-testing/SCRIPTS.md` | 7, 15 | UPDATE (done), ADD |
| `docs/design/from_template_to_project.md` | 9, 10, 11, 12, 13 | UPDATE (carried by the open P2 task) |
| `shift-left-testing/CI.md` | 12 | UPDATE (the ruff pin, with the playbook) |
| `.claude/commands/pcc.md` check 6 | 30 | NOOP |
| `writing-simple-and-direct/RULES.md` rule 8 scope | 32 | NOOP |
| `docs/plans/CONOP-FORMAT.md` | 14, 16, 21 | UPDATE, next planning-doctrine cycle |
| `docs/plans/OPORD-FORMAT.md` | 19, 22, 33 | UPDATE, UPDATE, NOOP |
| `shift-left-testing/ANTIPATTERNS.md`, `PATTERNS.md`, `FIXTURES.md` | 17, 18, 23 | ADD, next testing-doctrine cycle |
| `maintaining-ubiquitous-language/SKILL.md` | 20 | UPDATE |
| `.claude/commands/task.md` | 24 | UPDATE |
| `using-topic-branches/SKILL.md` | 25 | ADD |
| `configuration-management/SKILL.md` | 27 | ADD |
| `.claude/teams/code-review.md` | 28 | UPDATE |
| `.claude/commands/session-end.md` (template) | 29 | UPDATE at WHETSTONE Wave 4 |

The OBSERVED rows are not tasks yet. Per WHETSTONE, they enter the hub loop at OBSERVED and are dispositioned at the next consolidation session; the two planning-format and testing-sidecar clusters are each one cycle's worth of edits and should ship together, not one line at a time.

## KB-graph evidence lines

- `KB-graph: backlinks of designing-clear-data-displays in stx-server (15 files) → located the proposal, two challenges, three gates, the outside review, and the session doc that carried the skill's lineage; read those instead of the whole corpus`
- `KB-graph: Follows chain 20260827 → compass_wave_a → (six 08-26 sessions) → bootstrap → found the bootstrap audit's CONCERN-4 (em dashes routed upstream) and its Next Steps line on SCRIPTS.md; both edited in the hub this session`
- `KB-graph: backlinks of writing-simple-and-direct/SKILL.md, SKILLS_FRAMEWORK.md, .claude/README.md before editing → found the skills-tree drift (three unlisted skills) and the one-sentence description rule; both fixed`
- `KB-graph: grep for hub-upward across stx-server docs → three filed items in tasks.md plus one in the bootstrap session's Next Steps that never became a task (SCRIPTS.md); the harvest carries all four`

## References

- stx-server: `docs/sessions/20260826_bootstrap_from_tacsop_template.md` through `docs/sessions/20260827_tufte_skill_and_label_placement.md` (eight session docs); `docs/reviews/20260826_bootstrap_audit.md`; `docs/plans/20260827_proposal_tufte_visualization_skill.md` (D1 to D14); `docs/plans/20260827_proposal_tufte_skill_feedback_round.md` (D15 to D26); `docs/reviews/20260827_*` (six review reports on the skill and the placement fix).
- Hub: `docs/plans/conop_whetstone_recursive_doctrine_loop.md` D9, D10, A6; `.claude/skills/traversing-the-knowledge-base/SKILL.md`; `docs/doctrine-updates.md` 2026-08-27 entry (the propagation this harvest feeds).
