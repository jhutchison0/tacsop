# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Principles

### Shift-Left Testing (test-first, vertical-slice)
Every new behavior in `src/myproject/` is driven by a **failing test written first**, followed by the **minimum implementation** that makes it pass, then the next slice. This is vertical-slice (tracer-bullet) TDD; see [`.claude/skills/shift-left-testing/VERTICAL-SLICING.md`](.claude/skills/shift-left-testing/VERTICAL-SLICING.md).

Do not write a horizontal slice (all tests first, then all impl). Do not write production code without a failing test driving it.

A `PostToolUse` audit hook (`.claude/hooks/post-tool-shift-left-audit.sh`) fires after every `Write`/`Edit` to `src/myproject/**/*.py` and logs evidence to `.claude/audits/shift-left-violations.log`. The hook does not block; it produces an audit trail. See [`.claude/skills/shift-left-testing/ENFORCEMENT.md`](.claude/skills/shift-left-testing/ENFORCEMENT.md) for the full enforcement gradient.

- **Python** (`tests/`) — pytest suites for all utility modules.

### Simplicity First
Make every change as simple as possible. Avoid massive or complex changes. Every change should impact as little code as necessary. When in doubt, prefer the simpler solution. Prefer deep modules — small interfaces hiding meaningful implementation — over shallow ones; before declaring an interface done, ask whether each parameter is load-bearing or whether the function could derive it from one it already has.

### Branching (short-lived topic branches by work shape)
Branch on the shape of the work, not on a permanent partition of the codebase. Lead-only doc/ADR/small-refactor work lands directly on `main`. Team-deployed or multi-agent code work with an audit gate uses a short-lived `topic/<scope>-<slug>` branch, merged via merge-commit at the gate and **deleted (local + origin) immediately after merge**. No permanent domain branches. See [`.claude/skills/using-topic-branches/SKILL.md`](.claude/skills/using-topic-branches/SKILL.md), which also covers auditing standing branches.

### Session Documentation
Document work in `docs/sessions/YYYYMMDD_*.md`. See `config/project.yaml` for phase tracking.

### Documentation Style
When creating diagrams in markdown documentation, **prefer Mermaid over ASCII art**. Mermaid renders natively in GitHub and provides clear, maintainable visualizations.

## Environment Setup

This project uses a Python virtual environment. **All commands must run inside the venv.**

```bash
# First-time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env               # Add your API keys
```

**Always use the venv's Python/pytest**:
```bash
source .venv/bin/activate           # Activate before working
# OR use the venv directly:
.venv/bin/pytest                    # Run tests without activating
```

## Quick Commands

```bash
# Run tests (venv must be active, or use .venv/bin/pytest)
pytest                             # All tests
pytest -k test_name                # Tests matching pattern
pytest -x                          # Stop on first failure
pytest --pdb                       # Debug on failure

# Install optional dependencies
pip install -e ".[excel]"          # Excel utilities (pandas, openpyxl, xlsxwriter)
pip install -e ".[slack]"          # Slack integration
pip install -e ".[database]"       # PostgreSQL
pip install -e ".[all]"            # Everything
```

## Project Overview

This is a Python project template with reusable utility modules. It provides a starting structure for new projects with proven patterns for testing, configuration, and development workflow.

## Tech Stack

- **Language**: Python (3.11+)
- **Base Dependencies**: pyyaml, python-dotenv
- **Optional**: pandas, openpyxl, xlsxwriter, slack-sdk, psycopg, numpy

## Project Structure

```
utils/
├── src/myproject/
│   ├── __init__.py
│   └── utils/                    # Reusable utility modules
│       ├── logger.py             # OOP logging with colors and timezones
│       ├── excel.py              # DataFrame-to-Excel tables
│       ├── parallel.py           # Multiprocessing patterns
│       ├── geo.py                # Haversine distance and bearing
│       ├── weights.py            # SMARTER/reciprocal/rank-sum weights
│       ├── slack.py              # Slack webhook posting
│       ├── database.py           # Async PostgreSQL with JSONB
│       └── math_utils.py         # Combinatorics (nCr, nCk)
├── config/
│   └── project.yaml              # Project identity and phases
├── tests/                        # pytest suites
├── docs/
│   ├── design/                   # Pillars and roadmap
│   ├── sessions/                 # Session documentation
│   └── plans/                    # Implementation plans
├── .claude/
│   ├── README.md               # Agent roster, teams, scope matrix
│   ├── agents/                  # Individual agent definitions
│   │   ├── test-runner.md
│   │   ├── code-reviewer.md
│   │   └── python-prototyper.md
│   ├── teams/                   # Team composition templates
│   │   ├── feature-development.md
│   │   ├── bug-fix.md
│   │   └── code-review.md
│   ├── commands/                # session-start, session-end, pcc, pci, task
│   └── skills/                  # Level 0 skills (config, testing, venv, etc.)
├── pyproject.toml
├── .env.example
└── CLAUDE.md
```

## Workflow Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/session-start` | Load context, check health, review tasks | Start of every session |
| `/session-end` | Commit, update tasks, write session doc | End of every session |
| `/task` | Manage task list, escalate work items | Track and plan work |
| `/pcc` | Pre-Code Check — fast pass/fail checklist | Before every push |
| `/pci` | Pre-Code Inspection — context-aware review | Before merge/PR or when PCC passes but confidence is low |

### Planning Escalation

Work scales through four levels. Use `/task promote` or `/task plan` to evaluate:

1. **Task** — One person, one session, clear action (`docs/tasks.md`)
2. **TCS** — Multi-step with pass/fail criteria (Task, Condition, Standard) — also the universal task detail unit within all plan types
3. **CONOP** — Multi-wave with design decisions and parallel tracks (`docs/plans/`)
4. **OPORD** — Sequential execution of a decided strategy in waves (`docs/plans/`)

**Terminology**: *Phases* are strategic roadmap milestones (`project.yaml`). *Waves* are tactical parallel execution units within CONOPs/OPORDs where agent teams deploy.

## Agents

**IMPORTANT**: Before deploying any agent team, read `.claude/README.md` for the current roster and usage guide.

| Agent | Model | Writes Code? | Primary Domain |
|---|---|---|---|
| `test-runner` | haiku | No | All — runs pytest, reports results |
| `code-reviewer` | inherit | No | All — reviews against pillars, writes to `docs/reviews/` |
| `proposer` | sonnet | No | All — analyzes problems, proposes bold approaches, writes proposals |
| `python-prototyper` | sonnet | Yes | Python implementation |
| `decision-scientist` | inherit | No | Decision science — MAUT audits, weight validation, writes to `docs/reviews/` |

## Config Workflow

YAML files in `config/` are the source of truth. Python reads YAML directly.

- `config/project.yaml` — Project identity, phases, paths

API keys live in `.env` (never committed). See `.env.example` for required variables.
