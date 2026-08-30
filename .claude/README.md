# Claude Code Infrastructure

This directory contains agent definitions, team templates, slash commands, and skills for the myproject Python template. It provides everything needed to run single agents or coordinated multi-agent teams against this codebase.

## Design Principles

1. **Adversarial by design** — `code-reviewer` is always present on significant changes and always challenges
2. **Evidence over opinion** — No recommendation without data (test output, diff, file references)
3. **Clear ownership** — Each agent owns specific paths; reviewers read all, write only reports
4. **Shift-left testing** — Write-access agents must write tests alongside code, never after
5. **Frameworks as tools** — TCS/CONOP/OPORD are thinking structures for rigor, not identity or roleplay

## Directory Structure

```
.claude/
├── README.md              ← You are here
├── agents/                # Individual agent definitions
│   ├── test-runner.md
│   ├── code-reviewer.md
│   ├── proposer.md
│   ├── python-prototyper.md
│   └── decision-scientist.md
├── teams/                 # Team composition templates
│   ├── feature-development.md
│   ├── bug-fix.md
│   ├── code-review.md
│   └── decision-science.md
├── commands/              # Slash commands
│   ├── task.md            # /task — work tracker + escalation ladder
│   ├── session-start.md   # /session-start — load context
│   ├── session-end.md     # /session-end — close session
│   ├── sitrep.md          # /sitrep — narrative status report
│   ├── pcc.md             # /pcc — pre-commit check
│   └── pci.md             # /pci — pre-code inspection
└── skills/                # Reusable procedural knowledge
    ├── SKILLS_FRAMEWORK.md
    │
    └── # All Level 0 skills now use directory form (Anthropic Dec 18 open standard)
        ├── configuration-management/SKILL.md + 5 sidecars
        ├── shift-left-testing/SKILL.md + 7 sidecars
        ├── python-venv-management/SKILL.md + 2 sidecars
        ├── maintaining-ubiquitous-language/SKILL.md
        ├── maintaining-project-context/SKILL.md
        ├── recording-architecture-decisions/SKILL.md
        ├── using-topic-branches/SKILL.md
        ├── writing-simple-and-direct/SKILL.md + 4 sidecars
        ├── designing-clear-data-displays/SKILL.md + 4 sidecars
        ├── traversing-the-knowledge-base/SKILL.md
        └── lake-conventions/SKILL.md + 3 sidecars
```

> Note: legacy single-file skills `configuration-management.md`, `shift-left-testing.md`, `python-venv-management.md`, and `session-end.md` were retired 2026-05-19. The first three migrated to directory form with sidecar progressive disclosure; `session-end.md` reference content moved to `docs/session-doc-format.md`. The `/session-end` workflow remains in `.claude/commands/session-end.md`. See [SKILLS_FRAMEWORK.md](skills/SKILLS_FRAMEWORK.md) for the full inventory.

## Agent Catalog

| Agent | Purpose | Model | Access | When to Use |
|-------|---------|-------|--------|-------------|
| `test-runner` | Run pytest suites and report results | haiku | Read-only | After any code change to verify nothing is broken |
| `code-reviewer` | Adversarial review against design pillars and best practices | inherit | Read + Write reports | After significant changes, before merge |
| `proposer` | Analyze problems, propose bold approaches, debate before implementation | sonnet | Read + Write reports | Before committing to an implementation strategy |
| `python-prototyper` | Implement Python features, utilities, and tests | sonnet | Read/Write (scoped) | Feature implementation, bug fixes, new modules |

**Level 1 (project-specific)**

| Agent | Purpose | Model | Access | When to Use |
|-------|---------|-------|--------|-------------|
| `decision-scientist` | Audit decision models for MAUT correctness — weights, value functions, sensitivity coverage | inherit | Read + Write reports | When configuring criteria, reviewing decision model YAML, or before operationalizing a decision |

> **Model configuration**: Agents set to `inherit` use the orchestrator's model. Agents pinned to `sonnet` or `haiku` always use that model regardless of the orchestrator.

## Scope Matrix

| Path | test-runner | code-reviewer | proposer | python-prototyper | decision-scientist |
|------|:-----------:|:-------------:|:--------:|:-----------------:|:------------------:|
| `src/myproject/` | Read | Read | Read | **Write** | Read |
| `tests/` | Read/Run | Read | Read | **Write** | — |
| `config/` | Read | Read | Read | **Write** | Read |
| `docs/sessions/` | — | Read | Read | Write | Read |
| `docs/plans/` | — | Read | **Write** (proposals) | Write | Read |
| `docs/reviews/` | — | **Write** (reports) | Write (analysis) | — | **Write** (audits) |
| `.claude/` | — | Read | Read | — | — |

**Bold** = primary owner. Regular "Write" = secondary (for tests alongside their code). Dash = no access needed.

## Team Templates

Team compositions live in `.claude/teams/`. Use `/task promote` or `/task plan` to get recommendations on which team to assemble.

| Template | Agents | Use For |
|----------|--------|---------|
| [`feature-development`](teams/feature-development.md) | python-prototyper + test-runner + code-reviewer | New modules, utilities, or project components |
| [`bug-fix`](teams/bug-fix.md) | python-prototyper + test-runner | Targeted fixes with test verification |
| [`code-review`](teams/code-review.md) | code-reviewer + test-runner | Review-only passes, no new code |
| [`decision-science`](teams/decision-science.md) | proposer + decision-scientist + python-prototyper + test-runner + code-reviewer | MAUT/MCDA implementation, decision model design, scoring logic migration |

### Scaling Rules

| Work Size | Example | Agents |
|-----------|---------|--------|
| Config tweak (1–2 files) | Update a YAML value | 1 (lead only) |
| Bug fix (≤3 files) | Fix a function, add a test | python-prototyper + test-runner |
| New utility (single module) | Add a module to `utils/` | python-prototyper + test-runner + code-reviewer |
| New feature (cross-cutting) | Add a project component | proposer + code-reviewer + python-prototyper + test-runner via `feature-development` template |

## Inter-Agent Communication

Agents communicate through shared artifacts; no direct messaging is required for most workflows:

- **Config files** — `config/project.yaml` is the shared schema contract and project state
- **Test results** — `pytest` output validates changes and is the evidence standard for all agents
- **Task list** — `docs/tasks.md` tracks ownership and status across agent turns
- **Review reports** — `code-reviewer` and `decision-scientist` write findings to `docs/reviews/` for async review

## Escalation Paths

Involve the user when:

1. Agents disagree on approach and cannot resolve via evidence
2. A proposed change impacts more than 5 files or crosses module boundaries
3. Destructive operations are needed (dropping schema, removing public API)
4. A change would affect external integrations or production configuration
5. Test failures require architectural changes to resolve
6. `code-reviewer` flags a Critical finding (hardcoded secrets, security vulnerability)

## Work Organization

Work is tracked at two levels:

- **Strategic**: `config/project.yaml` → `state.active_work` (campaign focus, blockers, priorities)
- **Tactical**: `docs/tasks.md` (individual items with owners, priorities, status)

The `/task` command manages the tactical layer and includes an escalation ladder for promoting complex work into planning documents in `docs/plans/`:

| Level | Format | When to Use |
|-------|--------|-------------|
| Task | Single line in `docs/tasks.md` | One agent, one session, clear action |
| TCS | Structured criteria block | Multi-step with pass/fail conditions |
| CONOP | `docs/plans/` document | Multi-wave with design decisions |
| OPORD | `docs/plans/` document | Sequential execution of a decided strategy |

## Adding Project-Specific Agents

This is a **Level 0** template; the agents here are portable and generic. When the template becomes a real project:

1. Create a Level 1 agent file in `.claude/agents/` scoped to your domain
2. Add it to the Agent Catalog and Scope Matrix tables above
3. Update the agent table in `CLAUDE.md`
4. Add it to relevant team templates in `.claude/teams/`

Keep Level 0 agents (`test-runner`, `code-reviewer`, `proposer`, `python-prototyper`) unchanged: they are portable across projects and should not accumulate project-specific knowledge. A `tools:` line is capability, not knowledge; adding `WebSearch, WebFetch` so a proposer can verify a source is within Level 0.

See `.claude/skills/SKILLS_FRAMEWORK.md` for the Level 0/Level 1 distinction and porting guidance.
