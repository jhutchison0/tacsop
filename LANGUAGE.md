# LANGUAGE.md — Project Glossary

A glossary of project-specific domain terms. One-line definitions, no synonyms.

This file follows the pattern from Matt Pocock's `grill-with-docs` skill (`CONTEXT-FORMAT.md`), adapted for this project's domains: decision science, the agent framework, the military-inspired escalation ladder, and the doctrine-propagation governance model.

**Rules** (verbatim from the source pattern):
- Keep definitions tight. One sentence max.
- Define what it IS, not what it does.
- Each term gets a bold name, one-line definition, and `_Avoid:_` list of synonyms (when ambiguity exists).
- This is a glossary and nothing else. Not a spec, not a scratch pad.

When a term is missing or contested, invoke the `maintaining-ubiquitous-language` skill.

---

## Decision Science

**Alternative**: A candidate option being compared in a decision analysis. _Avoid:_ choice, option (too generic), candidate (only when context makes it specific).

**Criterion**: A dimension along which alternatives are compared. _Avoid:_ factor, attribute, measure, metric.

**Weight**: A non-negative number expressing the relative importance of a criterion, normalized so all weights sum to 1.0. _Avoid:_ importance, priority (vague).

**Value Function**: A transform that maps a raw criterion score to a utility in [0, 1]. _Avoid:_ scoring rule, normalizer.

**Utility**: A criterion-level or alternative-level score in [0, 1] after value-function transformation and weighting. _Avoid:_ score (use only for raw input).

**MAUT**: Multi-Attribute Utility Theory — the additive-utility decision model this project implements in `src/myproject/utils/decision_science/`.

**Sensitivity Analysis**: A check of how the alternative ranking changes when weights or scores move. Three modes: OAT (one-at-a-time), Monte Carlo, scenario compare.

**Scenario**: A named alternative weighting set used to compare what-if rankings against a baseline. _Avoid:_ profile (already used for environment config).

**Robust Pick**: An alternative that retains its top position across reasonable weight perturbations in sensitivity analysis.

**Dominance**: One alternative strictly beats another on every criterion. A dominated alternative can be eliminated without further analysis.

---

## Agent Framework

**Agent**: A specialized worker with isolated context, a defined scope, and a model assignment, invoked via the `Agent` tool. Lives in `.claude/agents/<name>.md`. _Avoid:_ subagent (use only when contrasting with the lead in a multi-agent flow).

**Skill**: A self-loading capability defined in `.claude/skills/<name>/SKILL.md` (directory form, preferred) or `.claude/skills/<name>.md` (single-file, legacy), invoked by name or auto-triggered by Claude when the description matches. _Avoid:_ procedure (too generic), playbook (already taken by team templates).

**Command**: A user-invoked workflow defined in `.claude/commands/<name>.md`, executed only when the user types `/<name>`. Distinct from a skill in that timing is always user-controlled. _Avoid:_ slash command (redundant), shortcut.

**Team**: A pre-composed agent roster for a class of work, defined in `.claude/teams/<name>.md`. Templates only; teams are instantiated at deployment time. _Avoid:_ squad, group.

**Roster**: The set of agents currently defined in `.claude/agents/`. The live list is whatever is in that directory; CONTEXT.md tracks the current count and names.

**Subagent Type**: The named template a teammate is spawned from. Drives tool access and default model. _Avoid:_ agent role.

---

## Escalation Ladder

**Task**: One person, one session, one clear action. The smallest unit in `docs/tasks.md`. Promote upward when the work exceeds one session or requires multi-step coordination.

**TCS**: Task, Condition, Standard — a structured task spec with pass/fail criteria. The universal task-detail unit inside all plan types (CONOP, OPORD). _Avoid:_ ticket, story.

**CONOP**: Concept of Operations — a multi-wave plan covering design decisions and parallel tracks. Lives in `docs/plans/`. _Avoid:_ design doc (already taken).

**OPORD**: Operations Order — the sequential execution form of a decided strategy, organized in waves. Lives in `docs/plans/`. _Avoid:_ runbook (overloaded with ops connotations).

**Wave**: A tactical parallel-execution unit inside a CONOP or OPORD where agent teams deploy. Bounded by a shared exit criterion. _Avoid:_ sprint, batch.

**Phase**: A strategic roadmap milestone tracked in `config/project.yaml` under `build_phases`. Strictly distinct from wave. _Avoid:_ stage, milestone (use phase or wave specifically).

**Pillar**: A foundational design principle for the project. Three currently: Simplicity First, Shift-Left Testing, Config-Driven. Listed in `config/project.yaml`. _Avoid:_ tenet, principle (use pillar when referencing the formal list).

---

## Governance & Propagation

**Doctrine**: A framework-level convention or pattern intentionally maintained at the `utils` template repo and intended for adoption across downstream consumer repos. Not all changes are doctrine; only those meant to spread.

**Propagation**: The process of pushing a doctrine update from this repo to downstream consumer repos via `scripts/propagate_doctrine.py`. See `docs/propagation-protocol.md`.

**Downstream Repo**: A consumer of this template that has adopted some or all of its conventions and is auto-discovered by the propagation script at each cycle. The most recent cycle (2026-04-21) reached 11 repos; the current discoverable roster is larger and listed in `docs/propagation-protocol.md`.

**Upstream Update**: A pending doctrine notification waiting for review in a downstream repo, surfaced as `.claude/upstream-update.md` at session start.

**Doctrine Update Entry**: A dated section in `docs/doctrine-updates.md` describing one propagation cycle. Each entry is the unit that the propagation script extracts and distributes.

**Append Mode**: A propagation behavior that preserves unread notifications in downstream repos by appending new updates instead of overwriting. Default since 2026-03-30.

---

## Workflow Artifacts

**Session**: A bounded development working period, ideally a single Claude Code conversation, framed by `/session-start` and `/session-end`.

**Session Doc**: A dated record of one session in `docs/sessions/YYYYMMDD_<subject>.md`. Carries knowledge-graph edges to design docs, plans, and prior sessions.

**Review**: An agent-authored analysis output in `docs/reviews/YYYYMMDD_<subject>.md`. Convention introduced 2026-04-21; applies to code-reviewer, decision-scientist, and proposer outputs.

**LANGUAGE.md**: This file. The project's domain glossary. Maintained via the `maintaining-ubiquitous-language` skill.

**CONTEXT.md**: The project's narrative identity, mission, current state, and key constraints. Companion to `LANGUAGE.md` and `config/project.yaml`. Maintained via the `maintaining-project-context` skill.

**ADR**: Architecture Decision Record — a numbered file in `docs/adr/NNNN-<slug>.md` capturing one decision that satisfies the triple filter: hard to reverse AND surprising without context AND result of a real trade-off. Maintained via the `recording-architecture-decisions` skill. See `docs/adr/ADR-FORMAT.md`.

**Triple Filter**: The gate for whether a decision warrants an ADR. All three required: hard to reverse, surprising without context, real trade-off. Source: Matt Pocock's ADR format.

---

## Vocabulary Crosswalk (Military ↔ Civilian)

Used when externally-shared content (downstream skill descriptions, public docs) should not carry internal military framing. Keep military terms in this repo's internal docs; substitute civilian terms when the artifact crosses to a downstream repo or external audience.

| Internal (military) | External (civilian) |
|---|---|
| PCC | pre-commit-check |
| PCI | pre-merge-inspection |
| SITREP | status-report |
| OPORD | operations-order |
| CONOP | concept-of-operations |
| TCS | task-condition-standard |
| wave | execution-phase |
| backbrief | progress-summary |
| METL | mission-essential-task-list |

The crosswalk is intentionally one-way: external content adopts civilian, internal content stays military. Do not rename internal files.

---

## Anti-Glossary (Terms We Deliberately Don't Use)

**"Module"** as a unit of organization: ambiguous (Python module? Deep module per Ousterhout? Component?). Use the specific term: `package`, `file`, `function`, `class`, or `deep module` (when explicitly invoking Ousterhout).

**"Component"**: not used in this codebase. If imported from external prose, translate to `agent`, `skill`, `utility`, or `package` per context.

**"Plan"** unqualified: prefer `TCS`, `CONOP`, or `OPORD` — they signal scope. Reserve unqualified "plan" only for genuinely informal sketches.

**"Stage"**: ambiguous between phase and wave. Use one of those.

---

## Maintenance

Update LANGUAGE.md when:
- A new term emerges in conversation that risks being defined two ways.
- A term in use here is renamed or deprecated.
- A downstream repo reports confusion about a term we use.

Do not add a term just because it appeared once. The bar is recurrence + ambiguity.

When in doubt, invoke the `maintaining-ubiquitous-language` skill.

---

**Last Updated**: 2026-05-19
**Maintained by**: The `maintaining-ubiquitous-language` skill, with human review.
