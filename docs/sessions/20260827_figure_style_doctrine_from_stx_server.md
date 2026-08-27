# Session: Figure Style Doctrine, Harvested from stx-server

**Date**: 2026-08-27
**Branch**: main
**Tags**: #session #doctrine #skills #propagation #whetstone #harvest #complete

**Documents**: [CLAUDE.md](../../CLAUDE.md) (Figure Style section), [.claude/skills/SKILLS_FRAMEWORK.md](../../.claude/skills/SKILLS_FRAMEWORK.md), [docs/doctrine-updates.md](../doctrine-updates.md) (2026-08-27 entry), [docs/tasks.md](../tasks.md), [CHANGELOG.md](../../CHANGELOG.md)
**Implements**: [conop_whetstone_recursive_doctrine_loop.md](../plans/conop_whetstone_recursive_doctrine_loop.md) (D9 lesson schema, D10 upward harvest; Wave 1 window session 1 of 5)
**References**: [20260827_stx_server_lessons_harvest.md](../reviews/20260827_stx_server_lessons_harvest.md), [20260827_figure_style_doctrine_preflight.md](../reviews/20260827_figure_style_doctrine_preflight.md), [docs/propagation-protocol.md](../propagation-protocol.md), [designing-clear-data-displays/SKILL.md](../../.claude/skills/designing-clear-data-displays/SKILL.md), [traversing-the-knowledge-base/SKILL.md](../../.claude/skills/traversing-the-knowledge-base/SKILL.md); stx-server `docs/sessions/20260827_tufte_skill_and_label_placement.md` and `docs/reviews/20260826_bootstrap_audit.md`
**Follows**: [20260803_uv_environment_doctrine.md](20260803_uv_environment_doctrine.md) (the 2026-08-13 to 08-15 kb-graph and WHETSTONE sessions wrote no session doc; their record is the CONOP Status Log and `docs/reviews/2026081[34]_*`)
**Cites**: Edward R. Tufte, through the copied skill's `RULES.md` source ledger (34 quotations verified by fetch in stx-server)

---

## Summary

The user took Tufte's course and asked for three things: copy stx-server's new `designing-clear-data-displays` skill into the hub whole, study what that repo is doing and rebuild the lessons worth sharing, and build the doctrine update that ships the skill. All three landed. The skill (five files, 409 lines, no repo names) is byte-identical to stx-server at `307d195` and wired per its own `ADOPTION.md`; the harvest holds 33 lessons in WHETSTONE's D9 line schema with D10 provenance, the first intake from a repo that never had the upward channel; the 2026-08-27 doctrine entry passed the code-reviewer's pre-flight (GO-WITH-FIXES 0/2/6, all twelve findings applied) and dry-runs to 16 repos. Live propagation is the one thing not done: it writes into 16 working trees and waits for the user's go.

Along the way the hub absorbed stx-server's two other hub-upward items (research tools on the two reasoning agents; the audit hook's import-grep fallback, built test-first) and fixed what its bootstrap audit could not fix downstream without forking: 27 running-prose em dashes in four template-copied docs, a Level 0 sidecar that said "in this repo" about hub scripts, and skills inventories that listed six of nine skills.

| Metric | Value |
|---|---|
| Skill copied | 5 files, 409 lines, `diff -r` identical, 0 repo names |
| Hub files changed | 19 modified, 4 new (skill dir, harvest, pre-flight, hook tests) |
| Tests | 269 at open; 278 at close (9 hook tests, the first written failing) |
| Lessons harvested | 33 (32 fleet-scope): 8 IDENTIFIED, 21 OBSERVED, 4 NOOP |
| Pre-flight | GO-WITH-FIXES 0/2/6 + 4 Minor; 12 of 12 applied |
| Dry run | 16 repos: 13 append, 3 new (stx-server, tactics-game, veil-engine) |
| Em dashes added by this session | 0 (27 removed) |
| Check 5 (M2) | run twice, 0 MISSING over 26 paths |

## Work Completed

### 1. Session start, three findings that changed the day

The five "verified absent" March decision-science docs are present on this box, dated 2026-03-26; the 08-13 check ran on `topic/kb-graph-traversal` in a worktree, and untracked files do not follow a worktree. The task line is corrected and actionable. `veil-engine/.claude/upstream-lesson.md` holds six fleet-scope lessons pending since 08-15 and 08-21, the first organic A6 canary fire; harvested next session, task filed. The uncommitted roster line from yesterday named `stx-server`, bootstrapped 2026-08-26 from `7074f90`, with a Tufte skill proposal dated today.

### 2. The traversal, then the copy

`KB-graph: backlinks of designing-clear-data-displays in stx-server (15 files) → located the proposal, two challenges, three gates, the outside review, and the session doc that carried the skill's lineage; read those instead of the whole corpus`

`KB-graph: Follows chain 20260827 → compass_wave_a → six 08-26 sessions → bootstrap → found the bootstrap audit's CONCERN-4 (em dashes routed upstream) and its Next Steps line on SCRIPTS.md; both edited in the hub this session`

The skill was copied with `cp -r` and verified with `diff -r`. Wired per `ADOPTION.md` steps 1 to 3: Figure Style section in `CLAUDE.md` beside Prose Style (the ambient block without stx-server's Kid-First override, which is that repo's); the reviewer's checklist line beside the prose line; the framework entry; both skills trees. `writing-simple-and-direct` 1.0.1 carries the receiver side of the pre-question hand-off that stx-server's D24 drafted for the hub.

`KB-graph: backlinks of writing-simple-and-direct/SKILL.md, SKILLS_FRAMEWORK.md, .claude/README.md before editing → found the skills-tree drift (three unlisted skills) and the one-sentence description rule; both fixed`

### 3. The two other hub-upward items, applied

`proposer` and `code-reviewer` gained `WebSearch, WebFetch`; `.claude/README.md` now states that a `tools:` line is capability, not the project knowledge the Level 0 rule guards. The audit hook's import-grep fallback was ported from stx-server `62f20a1` test-first: `tests/unit/test_shift_left_hook.py` drives the bash hook with a JSON payload in a throwaway git repo; the first test failed with `MISSING_TEST`, the patch made it pass, two characterization tests followed. The pre-flight then found that the `from pkg import mod` form matched only through a GNU grep quirk (`(x|^)` mid-pattern; BSD grep and Python `re` reject it), that `${file_path#*/src/}` strips at the first `/src/` on the box rather than the project's, and that unescaped dots let `myprojectXwidgets` match `myproject.widgets`. All three fixed; the tests are parametrized over four import forms and four near-miss names (9 tests). `ENFORCEMENT.md` step 4 and its limitations describe the two-stage lookup.

### 4. The harvest

`KB-graph: grep for hub-upward across stx-server docs → three filed items in tasks.md plus one in the bootstrap session's Next Steps that never became a task (SCRIPTS.md); the harvest carries all four`

[20260827_stx_server_lessons_harvest.md](../reviews/20260827_stx_server_lessons_harvest.md): every `## Lessons` section of eight session docs, the bootstrap audit, and every line naming the hub, rendered as D9 lines with origin provenance and routed to owner artifacts. Eight applied this session and labeled IDENTIFIED (the pre-flight's HIGH-2: D1 reserves LEARNED for a human flip after verified use); five Day-1 lessons onto the open playbook task; sixteen process lessons routed to the plan formats and testing sidecars for their next cycles; four NOOP with reasons; four repo-scope notes kept so the tail is visible. One coverage finding: the template does not ship the D10 channel, so a repo bootstrapped after the canaries carried its upward items as `tasks.md` lines, found by the hub one day later. Filed as a task, not an A6 failure.

### 5. The doctrine entry and its pre-flight

Three parts per the 2026-07-20 precedent, each with its own adoption-mode table: the skill bundle (TEMPLATE-COPY plus four PATCH steps), the research tools (PATCH, with a stated opt-out), the hook fallback (TEMPLATE-COPY then re-glob, or PATCH one block; the hub's tests marked HUB-ONLY because they assume `src/myproject/`). Civilian vocabulary throughout ("execution-phase", not wave). The code-reviewer's pre-flight ([report](../reviews/20260827_figure_style_doctrine_preflight.md)) verified all 34 named paths, the byte-identical copy, the hook on four probe paths, and every harvest citation, then found: the dash count was 27 not 26 (HIGH-1); LEARNED misused (HIGH-2); the grep quirk (C1); the `/src/` strip (C2); two lessons missing from the routing table (C3); the framework's inventory sections still listing seven of ten (C4); three replacements that read wrong (C5); the audience never named (C6); and four Minor. All applied and re-verified: 278 tests, 0 dashes added, check 5 clean, dry run 16.

### 6. Side fixes the traversal surfaced

27 running-prose em dashes replaced in `CONOP-FORMAT.md`, `OPORD-FORMAT.md`, `session-doc-format.md`, and `.claude/README.md` (headings, table cells, list-label separators, and the header specimen untouched per rule 8's scope). `SCRIPTS.md` line 3 no longer says "in this repo". `SKILLS_FRAMEWORK.md` gained inventory sections for `using-topic-branches`, `writing-simple-and-direct`, and `traversing-the-knowledge-base`; both trees list all ten skills. The description rule reads "one to three sentences".

## Key Decisions

| Decision | Rationale |
|---|---|
| Copy the skill verbatim; no hub edits | Level 0 by design (no repo names); the hub's ambient block omits only stx-server's Kid-First override sentence, which is that repo's UX rule. Any future fix goes to the skill and propagates. |
| One entry, three parts | Batching Rule 1 (one cycle, one entry) with Rule 2 honored by per-part tables, the 2026-07-20 precedent. The em-dash sweep and `SCRIPTS.md` ride as trivial bumps (Rule 3). |
| Apply the hub-upward items now, not just cite them | Each is small, verified, and the entry can then say what the hub did rather than what it intends. |
| IDENTIFIED, not LEARNED, for the eight applied lessons | WHETSTONE D1: LEARNED needs verified use and a human flip. This harvest sets the precedent for the greppable state machine, so the first data point must be honest. |
| Hold live propagation for the user | It writes into 16 working trees; the protocol's pre-flight is done and the dry run is recorded, so the go is one command. |
| Not fixing em dashes in hub code comments | Prose rule 8 governs running prose; stx-server's stricter N5 is its own rule, applied to its project-authored copies. |

## Lessons

1. **Cross-repo path mentions trip check 5.** Two new task lines named `stx-server/docs/reviews/...` and `veil-engine/.claude/upstream-lesson.md`; the check's regex has no notion of a repo prefix and reported both MISSING. Reworded rather than allowlisted (a gate surface would have had to change in the same commit). The check needs a prefix rule when the D10 harvest becomes routine, since every harvest line names another repo's paths. `LESSON (OBSERVED): check 5 reads cross-repo path mentions as local | evidence: this session's first check-5 run, 2 false MISSING | scope: repo | owner: .claude/commands/pcc.md | verdict: UPDATE`.
2. **A worktree check can falsify presence.** The 08-13 "verified absent" verdict on the March docs was run in a worktree; untracked files stay in the main checkout. Verify presence on the branch the files were reported from, or `git worktree list` first.
3. **The reviewer earned its run on a bash regex.** The `(x|^)` quirk would have shipped to every macOS downstream as a silent regression of the very form the entry documents. A pre-flight that re-runs the commands, not just reads the prose, is the protocol's step 2 done right.
4. **The upward channel needs to ship with the template.** A repo bootstrapped after the canaries had no Step 5.5, wrote three hub-upward `tasks.md` lines, and was found by a human reading its task file. The convention worked as operator memory, which is what D10 exists to replace.

## Pillar Compliance

- **Shift-Left**: the hook fallback was driven by a failing test written first (`MISSING_TEST` observed, then the patch, then `OK_TEST_EXISTS`); the audit hook does not watch `.claude/hooks/`, so the commit history is the evidence.
- **Simplicity First**: the skill was copied, not adapted; the hook patch is one `if` block; every other change is a sentence, a line, or a table row.
- **Config-Driven**: `project.yaml` state updated to what is true; no config semantics changed.

## PCC Results

Session close, over the working tree (nothing staged until the commits below):

```
[PASS] No secrets (the .env.example hit is the placeholder DB_PASSWORD line, unchanged)
[PASS] Tests pass (278 tests in 3.3s)
[PASS] No debug artifacts
[INFO] Branch: main, ahead of origin by 1 before this session's commits
[PASS] Reference integrity: 26 paths checked, 0 MISSING (metric M2); first run had 2 false MISSING from cross-repo mentions, reworded
[WARN] Gate separation: the hook is in the working tree with everything else; committed alone as [gate] below
[PASS] 0 em dashes added; config/project.yaml parses; no large files
```

## Commits

- `[gate]` Audit hook: import-grep fallback for feature-named test partners (hook only)
- `[doctrine]` Figure Style doctrine: designing-clear-data-displays copied from stx-server; research tools; hook tests; 33-lesson harvest; 2026-08-27 entry pre-flighted; em-dash sweep; skills inventories; session record

## Next Steps

- [ ] User: say go, and the hub runs `scripts/propagate_doctrine.py` (dry run recorded: 16 repos, 13 append, 3 new). Log the cycle in the next session doc per the protocol.
- [ ] Harvest veil-engine's six pending upward lessons (task filed); clear the file after intake.
- [ ] WHETSTONE Wave 1: this is window session 1 of 5; four `KB-graph:` lines above, two naming artifacts then edited (M3 candidates for non-author verification at window close).
- [ ] Next planning-doctrine cycle: the three CONOP-FORMAT and two OPORD-FORMAT lessons in the harvest's routing table; next testing-doctrine cycle: the three shift-left sidecar additions.
- [ ] Decide the five March docs (present here, untracked since March).
- [ ] Push the 08-15 canary commit with this session's commits.
