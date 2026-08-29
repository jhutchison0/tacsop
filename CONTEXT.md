# CONTEXT.md — What This Project Is

A one-page narrative of the project's identity, mission, current state, and key constraints. Uses terms defined in [LANGUAGE.md](LANGUAGE.md). For machine-readable state, see [config/project.yaml](config/project.yaml).

Maintained via the `maintaining-project-context` skill. Update when the project's mission, scope, or downstream relationships materially change, not for routine task progress.

---

## Identity

`tacsop` (Tactical Standing Operating Procedure; renamed from `utils` 2026-07-17, [ADR-0002](docs/adr/0002-rename-repository-to-tacsop.md)) is a Python project template **and** a doctrine source. It serves two missions through one codebase: contributors clone it to start new projects, and existing downstream consumers receive convention updates from it via a propagation script.

The two missions are deliberately co-located. Doctrine that lives only in documentation drifts; doctrine that lives only in code becomes invisible. Keeping both in one repo forces every convention to survive contact with a working Python codebase before it is propagated.

---

## Mission

- **Provide a working Python project template** with utility modules, test scaffolding, and a Claude Code agent framework that a contributor can clone and have running in under an hour.
- **Source and propagate framework doctrine** to a roster of downstream consumer repos via `scripts/propagate_doctrine.py`, with append semantics so unread updates are never lost.
- **Codify our way of working** (the design pillars, the escalation ladder, the agent roster, the skills framework) in a form that can be read, audited, and reused.

This project is not a research artifact, not a product, and not a one-off tool. Treat changes here as having multiplicative downstream impact.

---

## Current State

See [config/project.yaml](config/project.yaml) for canonical values. Snapshot at last update of this file:

- **Version**: 0.1.0
- **Active phase**: Phase 1 (Foundation) complete; Phase 2 deliberately undefined, to be set by the current sprint.
- **Active work**: Agent output standardization, doctrine artifact build-out (LANGUAGE.md, CONTEXT.md, ADRs), TDD discipline upgrade.
- **Downstream consumers**: discovered automatically by `scripts/propagate_doctrine.py` at each cycle; the most recent cycle (2026-04-21) reached 11 repos; the current discoverable roster is larger (see [docs/propagation-protocol.md](docs/propagation-protocol.md) for the snapshot).
- **Most recent doctrine propagation**: 5th cycle (2026-04-21); 11 repos adopted the `docs/reviews/` convention.

---

## Constraints

The hard rules. Violating these requires explicit user override per change.

**Pillars** (formally tracked in `config/project.yaml`):
- **Simplicity First**: every change as small and simple as possible. When in doubt, the simpler solution wins.
- **Shift-Left Testing**: tests live alongside code, not after. Every new component carries a test plan.
- **Config-Driven**: YAML files in `config/` are the source of truth; Python reads YAML directly. Avoid hardcoding configurable values.

**Hard rules**:
- Python 3.11 minimum (bumped 2026-04-21).
- All Python commands run inside the project venv (`.venv/`). Environments are built with uv (`uv venv --managed-python`, `uv pip`); adopted 2026-08-03.
- Agent reports write to `docs/reviews/YYYYMMDD_<subject>.md` (convention since 2026-04-21).
- Session docs write to `docs/sessions/YYYYMMDD_<subject>.md`.
- Plans write to `docs/plans/`.
- Internal docs may use the military escalation vocabulary (PCC, PCI, SITREP, OPORD, CONOP, TCS). Externally-shared content uses civilian equivalents per the LANGUAGE.md crosswalk.
- Secrets live only in `.env`; never committed.

**Anti-rules** (do not do these):
- Do not add abstractions for hypothetical future requirements.
- Do not add new agents until existing agents are demonstrably saturated on their intended problems.
- Do not bulk-install third-party skill packs (mattpocock/skills, superpowers, community mega-bundles). Cherry-pick patterns; never the whole catalog.
- Do not migrate side-effect-carrying commands (session-end, pcc) to auto-triggering skills.

---

## Key Relationships

**Downstream consumers**: auto-discovered by the propagation script (presence of `.claude/commands/` directory under `~/projects/`) rather than maintained as an explicit registry. The most recent cycle (2026-04-21) reached 11 repos. See [docs/propagation-protocol.md](docs/propagation-protocol.md) for the full process and the current discoverable roster.

**Agent roster** (current, in `.claude/agents/`):
- `proposer` — analyzes problems and proposes bold approaches; debates with code-reviewer.
- `code-reviewer` — reviews changes against pillars; writes audit reports.
- `decision-scientist` — runs MAUT-style decision analyses and audits decision models.
- `python-prototyper` — writes Python implementation code.
- `test-runner` — runs pytest and reports results.

**Team templates** (in `.claude/teams/`): pre-composed rosters for feature-development, bug-fix, code-review, decision-science.

**Skills inventory**: see `.claude/skills/SKILLS_FRAMEWORK.md` for the canonical list.

---

## Reading Order for New Agents and Contributors

When an agent or human is introduced to this project, point them at these files in this order:

1. **This file** (`CONTEXT.md`) — what the project is.
2. [LANGUAGE.md](LANGUAGE.md) — how we name things.
3. [CLAUDE.md](CLAUDE.md) — workflow conventions and quick commands.
4. [config/project.yaml](config/project.yaml) — current machine-readable state.
5. [.claude/README.md](.claude/README.md) — agent roster, scope matrix, team templates.
6. [docs/propagation-protocol.md](docs/propagation-protocol.md) — required reading if touching anything that propagates downstream.
7. [docs/adr/](docs/adr/) — accepted architecture decisions; check before reopening any decision they cover.
8. [.claude/skills/lake-conventions/](.claude/skills/lake-conventions/) — required reading before writing to the lake, in repos that do.
9. [docs/sessions/](docs/sessions/) — recent session for live context (most recently modified file).

---

## Distinguishing This File from Adjacent Artifacts

| Artifact | What it answers |
|---|---|
| `CONTEXT.md` (this file) | *What is this project and what does it care about?* |
| [LANGUAGE.md](LANGUAGE.md) | *What do specific terms mean in this project?* |
| [config/project.yaml](config/project.yaml) | *What is the machine-readable current state?* |
| [CLAUDE.md](CLAUDE.md) | *What conventions and commands does the agent need at hand?* |
| [docs/sessions/](docs/sessions/) | *What was just worked on?* |
| [docs/plans/](docs/plans/) | *What is planned next?* |

Do not duplicate content across these files. When tempted, ask: "Which one of these is this *really* about?" and put it there.

---

**Last Updated**: 2026-05-19
**Maintained by**: The `maintaining-project-context` skill, with human review.
