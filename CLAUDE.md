# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Principles

### Shift-Left Testing
Every new component must include a test plan. Tests are written alongside code, not as an afterthought.
- **Python** (`tests/`) — pytest suites for all utility modules

### Simplicity First
Make every change as simple as possible. Avoid massive or complex changes. Every change should impact as little code as necessary. When in doubt, prefer the simpler solution.

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

- **Language**: Python (3.10+)
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
│   ├── agents/                   # test-runner, code-reviewer, python-prototyper
│   ├── commands/                 # session-start, session-end, pcc, pci, task
│   └── skills/                   # Level 0 skills (config, testing, venv, etc.)
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
2. **TCS** — Multi-step with pass/fail criteria (Task, Condition, Standard)
3. **CONOP** — Multi-phase with design decisions and parallel tracks (`docs/plans/`)
4. **OPORD** — Sequential execution of a decided strategy (`docs/plans/`)

## Agents

**IMPORTANT**: Before deploying any agent team, read `.claude/agents/README.md` for the current roster and usage guide.

| Agent | Model | Writes Code? | Primary Domain |
|---|---|---|---|
| `test-runner` | haiku | No | All — runs pytest, reports results |
| `code-reviewer` | inherit | No | All — reviews against pillars |
| `python-prototyper` | sonnet | Yes | Python implementation |

## Config Workflow

YAML files in `config/` are the source of truth. Python reads YAML directly.

- `config/project.yaml` — Project identity, phases, paths

API keys live in `.env` (never committed). See `.env.example` for required variables.
