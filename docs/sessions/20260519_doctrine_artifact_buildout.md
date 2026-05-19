# Session: Doctrine Artifact Buildout

**Date**: 2026-05-19
**Branch**: main
**Tags**: #session #doctrine #agents #infra #skills #framework #complete

**Documents**: [CLAUDE.md](../../CLAUDE.md) — Project conventions touched by every artifact
**Documents**: [.claude/README.md](../../.claude/README.md) — Skills tree refreshed in both commits
**Documents**: [.claude/skills/SKILLS_FRAMEWORK.md](../../.claude/skills/SKILLS_FRAMEWORK.md) — v2 update + Wave 2 inventory refresh
**References**: [docs/design/hold/plan1.md](../design/hold/plan1.md) — Source memo that triggered the sprint (gitignored)
**References**: [docs/reviews/20260519_plan1_proposer_grill.md](../reviews/20260519_plan1_proposer_grill.md)
**References**: [docs/reviews/20260519_plan1_audit.md](../reviews/20260519_plan1_audit.md)
**References**: [docs/reviews/20260519_plan1_maut.md](../reviews/20260519_plan1_maut.md)
**References**: [docs/reviews/20260519_pass2_audit.md](../reviews/20260519_pass2_audit.md)
**Follows**: [20260421_docs_reviews_convention_and_python311.md](20260421_docs_reviews_convention_and_python311.md) — Previous session
**Completes**: Doctrine artifact buildout (LANGUAGE.md + CONTEXT.md + ADRs + propagation protocol) and Wave 2 skill refactor (3 legacy skills → directory form)
**Cites**: Matt Pocock's `mattpocock/skills` — pattern source for CONTEXT-FORMAT, ADR-FORMAT, tracer-bullet TDD; adapted, not adopted

---

## Summary

Two coordinated sprints in one session driven by a 31KB strategic memo (`plan1.md`, attached to `docs/design/hold/`). A three-agent Pass 1 review converged on a sharper-than-the-memo scope; Pass 2 built the agreed doctrine artifacts; Pass 3 audited and verified. Mid-session the user observed that the new directory-form skills were ~100 lines while existing single-file skills ran 600–1500 lines — the rule we'd just codified ("migrate at >500 lines") was already violated by our own legacy. Wave 2 honored that rule by refactoring all three legacy skills to directory form with topical sidecar files. Two clean commits, no test regressions, no propagation to downstream yet (user requested fresh-eyes review in next session before propagating).

## Work Completed

### Wave 0 — Housekeeping

- Added `docs/design/hold/` to `.gitignore` as per-repo scratch workspace; `plan1.md` lives there but is not tracked.
- Renamed `.claude/settings.local.json` → `.claude/settings.json` per Anthropic convention; `settings.local.json` now gitignored for any future per-user content.

### Pass 1 — Three-Agent Analysis of plan1.md

Launched proposer, code-reviewer, and decision-scientist in parallel. Each produced an independent review in `docs/reviews/20260519_*`.

| Agent | Headline finding |
|---|---|
| **proposer** | Plan's sequencing is inverted (should be LANGUAGE → CONTEXT → ADR, not the reverse); its biggest gap is the missing propagation protocol; Pocock's LANGUAGE.md vocabulary solves a problem we don't have (TypeScript overloads) and ignores the one we do (decision-science + agent-framework + escalation-ladder terms) |
| **code-reviewer** | 0 FAILs / 14 CONCERNs across 16 numbered recommendations; flagged 2 plan self-contradictions (session-end "migration" is a no-op per Anthropic's own docs the plan quotes; grill-master agent is dismissed as covered elsewhere then recommended); surfaced a pre-existing duplication of session-end as both skill and command |
| **decision-scientist** | MAUT-ranked 16+ alternatives; broadly endorsed lead scope but flipped LANGUAGE.md (D4) out of P1 because it was the only item that changes how 11 downstream repos *talk*; finding survived sensitivity |

Lead synthesis converged with the user on: build CONTEXT.md, LANGUAGE.md, ADR system, propagation protocol, and a TDD upgrade. Build OUR LANGUAGE.md, not Pocock's verbatim. Defer all new agents. Defer all command→skill migrations. Resolve session-end duplication.

### Pass 2 — Doctrine Artifacts

Twelve new artifacts plus one rename and one deletion:

| Artifact | Author | Notes |
|---|---|---|
| `LANGUAGE.md` (repo root) | lead | Project-specific glossary: decision-science, agent framework, escalation ladder, governance, workflow. Civilian/military crosswalk. Anti-glossary section. |
| `CONTEXT.md` (repo root) | lead | Project identity, mission, current state, constraints, key relationships, reading order, adjacent-artifact distinguisher |
| `docs/propagation-protocol.md` | lead | Formalized: what counts as doctrine, the 5-question evaluation gate, batching rules, cycle anatomy, downstream discovery, append mode, rollback, civilian/military substitution |
| `docs/session-doc-format.md` | lead | Reference content demoted from the deleted session-end skill |
| `docs/adr/ADR-FORMAT.md` + `.gitkeep` | python-prototyper (took over by lead) | Pocock's triple-filter gate adopted verbatim |
| `.claude/skills/maintaining-ubiquitous-language/SKILL.md` | python-prototyper (took over by lead) | Directory form |
| `.claude/skills/maintaining-project-context/SKILL.md` | python-prototyper (took over by lead) | Directory form |
| `.claude/skills/recording-architecture-decisions/SKILL.md` | python-prototyper (took over by lead) | Directory form |
| `.claude/skills/SKILLS_FRAMEWORK.md` v2 | python-prototyper (took over by lead) | Anthropic Dec 18 open standard: YAML frontmatter spec, directory form, progressive disclosure rule, civilian/military vocabulary crosswalk |
| `.claude/skills/shift-left-testing.md` v1.1 | python-prototyper (took over by lead) | Added Vertical Slicing (tracer-bullet) section from Pocock's tdd skill |
| `.claude/commands/session-end.md` | lead | Step 5 slimmed to reference new `docs/session-doc-format.md` |
| `.claude/skills/session-end.md` | lead | **Deleted** — reference content moved to docs |

The python-prototyper hit a tool-permission block in its isolated subprocess; lead took over its work with full briefing context intact.

### Pass 3 — Audit and Pre-Commit Fixes

Launched code-reviewer (Pass 2 audit) and test-runner (regression check) in parallel.

- **test-runner**: 189 passed / 5 skipped / 1 baseline warning / 0.90s — no regression.
- **code-reviewer**: 0 FAILs / 14 CONCERNs; flagged stale `.claude/README.md` skills tree, a `configuration-management.md` listed twice in `SKILLS_FRAMEWORK.md`, missing version bump on `shift-left-testing.md`, an 11-vs-18 downstream-repo count discrepancy, and incorrectly flagged the `PROJECTS_DIR` resolution in `propagation-protocol.md` (verified manually — the doc was correct, the reviewer was wrong).
- All pre-commit CONCERNs resolved before commit.

### Commit 1: `cf946b5` — Doctrine artifact buildout (22 files, +2934 / −400)

### Wave 2 — Legacy Skill Refactor

Mid-session observation: new directory-form skills were ~100 lines while the three existing single-file skills ran 623–1533 lines. The progressive-disclosure rule codified in Pass 2's SKILLS_FRAMEWORK v2 said "migrate at >500 lines" — and all three legacy skills violated it.

Decision: refactor all three to directory form with topical sidecars. Leave commands (<160 lines each, user-readable workflows), agents, and team templates as single-file (all already concise).

| Skill | Before | After | Sidecars |
|---|---|---|---|
| `shift-left-testing` | 1242 lines | 8 files (SKILL.md 102) | TIERS, PATTERNS, MOCKS, FIXTURES, VERTICAL-SLICING, CI, ANTIPATTERNS |
| `configuration-management` | 1533 lines | 6 files (SKILL.md 88) | STRUCTURE-AND-FILES, LOADER, SECRETS, VALIDATION, TESTING-AND-PATTERNS |
| `python-venv-management` | 623 lines | 3 files (SKILL.md 105) | SETUP, TROUBLESHOOTING |

Every SKILL.md <110 lines. Every sidecar <400 lines. Total content largely re-organized; modest growth (~7%) from added cross-reference scaffolding (See Also footers, sidecar indices, philosophy/quick-reference sections in each SKILL.md). All 6 new directory-form skills picked up correctly by Claude Code's skill discovery during the session.

Post-refactor: updated `.claude/skills/SKILLS_FRAMEWORK.md` (inventory, Level 0 section, retired-skills list) and `.claude/README.md` (skills tree) to reflect the new layout. Tests re-verified green.

### Commit 2: `54c0022` — Wave 2 skill refactor (23 files, +3690 / −3433)

## Key Decisions

| Decision | Rationale |
|---|---|
| Build our own LANGUAGE.md, not Pocock's verbatim | Pocock's vocabulary disambiguates TypeScript-ecosystem overloads; ours need to disambiguate decision-science + agent-framework + escalation-ladder + governance terms. The pattern transfers; the words do not. |
| Sequence LANGUAGE → CONTEXT → ADR (not the reverse) | Proposer's correction. CONTEXT.md cites LANGUAGE terms; ADRs cite both. Building in the original order would have forced a retcon pass. |
| Reject command → skill migrations | Anthropic's own docs (quoted in the source plan) say a command and skill with the same name are equivalent — the migration is a no-op. More importantly, session-end and pcc have side effects; auto-triggering skills with side effects is wrong by construction. |
| Defer all new agents | Existing roster of 5 hasn't been demonstrably saturated yet. Adding agents speculatively is over-investment. |
| Demote session-end skill rather than delete | The skill's reference content (knowledge-graph relationship types, diagram guidelines, body template) was valuable. Moved to `docs/session-doc-format.md`; command references it. Zero content lost. |
| Refactor Wave 2 mid-session, not next sprint | The user observed the inconsistency; honoring our own freshly-written rule immediately was cleaner than tracking a follow-up debt item. Two commits keep the history bisectable. |
| Leave commands, agents, teams as single-file | All under 160 lines; progressive disclosure exists for Claude's context budget, not user readability. User-invoked workflows load whole regardless. |
| Hold off on propagation to 11 downstream repos | User requested fresh-eyes agent review in next session before propagating. Two commits sit on local main; not pushed at end of session... actually pushed at end of session per user direction. |

## Pillar Compliance

| Pillar | Status | Notes |
|---|---|---|
| **Simplicity First** | PASS | Sprint scope was disciplined down from a 16+ recommendation memo to 6 core artifacts + a TDD upgrade. Wave 2 was pure reorganization, no new abstractions. Rejected speculation (interface-designer with parallel subagents, mattpocock bulk install, command→skill migrations). |
| **Shift-Left Testing** | PASS | shift-left-testing skill got a vertical-slicing upgrade in Pass 2 AND a structural refactor in Wave 2. Tests verified green twice. Code-reviewer ran mid-Pass-2, not at the end. |
| **Config-Driven** | PASS | LANGUAGE.md and CONTEXT.md are the narrative companions to `config/project.yaml`'s structured state. Propagation protocol formalized a process that was previously implicit in a script. |

## Pass 1 Agent Disagreements (Surfaced for the Record)

- **D4 (Pocock's LANGUAGE.md)**: MAUT said "defer from P1"; reviewer said "ADOPT skill, skip pillar"; proposer said "build ours, not his." Resolution: build ours. All three were partly right.
- **D6 (`diagnosing-defects` skill)**: MAUT considered adding (utility 0.728); reviewer said "defer, `bug-fix.md` team template already does it." Reviewer won on evidence; D6 deferred to a future re-evaluation triggered by team-template usage data.
- **Reviewer error on propagation-protocol PROJECTS_DIR**: reviewer claimed the doc was wrong; verified manually that the doc was correct and the reviewer mis-counted `.parent` calls in the script. Trust but verify.

## Commits

| Hash | Subject | Files | Lines |
|---|---|---|---|
| `cf946b5` | [infra] Doctrine artifact buildout: LANGUAGE, CONTEXT, ADRs, skills, propagation protocol | 22 | +2934 / −400 |
| `54c0022` | [infra] Wave 2: refactor 3 legacy skills to directory form with sidecars | 23 | +3690 / −3433 |

Plus this session doc as the third commit.

## Next Steps

- [ ] **Next session — fresh-eyes agent review.** User explicitly requested a Pass 4 review by the agents with fresh context, before propagation. Likely roster: code-reviewer (re-audit doctrine artifacts), decision-scientist (re-rank the now-built artifacts against actual usefulness criteria), proposer (find what we missed).
- [ ] **Sixth doctrine propagation cycle.** Bundles: Python 3.11 minimum bump (pending since 2026-04-21), LANGUAGE.md skill, CONTEXT.md skill, ADR system, SKILLS_FRAMEWORK v2, shift-left-testing TDD upgrade, session-end skill/command deduplication, propagation-protocol.md, Wave 2 skill refactor. The doctrine entry must include a per-artifact adoption-mode table (which artifacts are template-copy vs project-customize) per the code-reviewer's flagged pre-propagate fix.
- [ ] **First ADR**: a candidate is the "single Sprint-3 commit vs split commits" decision — but actually, that decision wasn't hard to reverse, so by the triple filter it shouldn't be an ADR. Better first candidate: "directory form mandatory for all new skills" if and when we want to remove the legacy escape hatch.
- [ ] **GitHub Actions CI workflow** (P3, carried from 2026-04-21).
- [ ] **`from_yaml` round-trip tests for 4 value functions** (P3, carried from 2026-04-21).

## Notes

- Skill discovery worked as expected during the session — every new directory-form skill appeared in the available-skills list within the response that created it.
- The python-prototyper subagent's permission block during Pass 2 is worth noting: subagents have their own permission scope distinct from the main thread. For doctrine-artifact writing, the main thread is more efficient anyway since it has full conversation context — but for genuine implementation work, this is a friction point to address (likely via the subagent's `allowed-tools` configuration or a more permissive default mode).
- The user's mid-session observation about line-count inconsistency was the highest-leverage feedback of the session — it surfaced a doctrine violation that we ourselves had introduced minutes earlier. Worth remembering: as soon as we write a rule, walk the existing codebase to see whether we already violate it.
