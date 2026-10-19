# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working with code in this repository.

## Development Principles

### Shift-Left Testing (test-first, vertical-slice)
Every new behavior in `src/myproject/` is driven by a **failing test written first**, followed by the **minimum implementation** that makes it pass, then the next slice. This is vertical-slice (tracer-bullet) TDD; see [`.claude/skills/shift-left-testing/VERTICAL-SLICING.md`](.claude/skills/shift-left-testing/VERTICAL-SLICING.md).

Do not write a horizontal slice (all tests first, then all impl). Do not write production code without a failing test driving it.

A `PostToolUse` audit hook (`.claude/hooks/post-tool-shift-left-audit.sh`) fires after every `Write`/`Edit` to `src/myproject/**/*.py` and logs evidence to `.claude/audits/shift-left-violations.log`. The hook does not block; it produces an audit trail. See [`.claude/skills/shift-left-testing/ENFORCEMENT.md`](.claude/skills/shift-left-testing/ENFORCEMENT.md) for the full enforcement gradient.

- **Python** (`tests/`) — pytest suites for all utility modules.

### Simplicity First
Make every change as simple as possible. Avoid massive or complex changes. Every change should impact as little code as necessary. When in doubt, prefer the simpler solution. Prefer deep modules (small interfaces hiding meaningful implementation) over shallow ones; before declaring an interface done, ask whether each parameter is load-bearing or whether the function could derive it from one it already has.

### Branching (short-lived topic branches by work shape)
Branch on the shape of the work, not on a permanent partition of the codebase. Lead-only doc/ADR/small-refactor work lands directly on `main`. Team-deployed or multi-agent code work with an audit gate uses a short-lived `topic/<scope>-<slug>` branch, merged via merge-commit at the gate and **deleted (local + origin) immediately after merge**. No permanent domain branches. See [`.claude/skills/using-topic-branches/SKILL.md`](.claude/skills/using-topic-branches/SKILL.md), which also covers auditing standing branches.

### Session Documentation
Document work in `docs/sessions/YYYYMMDD_*.md`. See `config/project.yaml` for phase tracking.

### Documentation Style
When creating diagrams in markdown documentation, **prefer Mermaid over ASCII art**. Mermaid renders natively in GitHub and provides clear, maintainable visualizations.

## Prose Style

All prose artifacts follow the writing-simple-and-direct skill. The kernel:

1. Have a point; state it in the first sentence. No throat-clearing.
2. Prefer the concrete word: name the file, the number, the failure.
3. One idea per sentence. Link sentences; do not pack them.
4. Active voice unless the actor is unknown or irrelevant.
5. Cut cruft words. The banned list lives in LANGUAGE.md.
6. Hedge with numbers or not at all.
7. Read it back; if you would not say it, do not write it.
8. No em dashes in running prose. Choose the mark that states the relationship.

Schemas define what a document contains; this defines how the words go.
Never cut a required section to save tokens.

## Figure Style

All data displays follow the designing-clear-data-displays skill. The kernel:

1. Show the data; erase ink that carries none, within reason.
2. Label the data where it lives; a key the eye must decode fails.
3. Make every distinction as subtle as it can be and still be seen.
4. Two marks too close make a third; move one, do not shrink both.
5. Show the effect at its true size: lie factor between 0.95 and 1.05.
6. Answer "compared to what?"; small multiples over one lonely chart.
7. Document the display: title, source, units, scale on the figure.
8. Content counts most: simple design, intense content.

Schemas and a repo's UX rules define what a display must contain; this defines how the ink goes.
Before the eight: could a table or a sentence carry these numbers? Under about twenty, a table usually does (VDQI p. 56).
A UX rule that asks for a less dense display wins; state the override.

## Claim Style

Every claim a reader will act on (that something works, landed, synced, exists, or is absent) follows the verifying-claims skill. The kernel:

1. Name the state: written, tested, deployed, or observed. Claim no higher than your evidence reaches. An absence is a claim too.
2. Evidence comes from this turn, after the last change to the thing claimed. Earlier output is stale: re-run the check, re-measure the number.
3. Check the outcome the claim names, with a check that can fail. A launcher's exit 0 is not the outcome; no error is not evidence.
4. Under each claim a reader will act on, put an `Evidence:` line with the command and its output, or `UNVERIFIED: <blocker>`. A skipped check is not a blocker; run it.
5. A checkout a timer or service runs from is deployed only when clean: `git status --porcelain` prints nothing.
6. Probes read; they never write to the system they check.

A plan, an opinion, or an explanation of code is not a claim. The belief a plan rests on is one: check it before you act.
A diff shown in the same message is its own evidence. Say what you did not do; that needs no `Evidence:` line.
`/session-end` gathers the session's claims into a `## Claims` table.

## Picture Style

Every statement about what is true now (a host, a count, a schedule, a coverage figure, a version) follows the maintaining-the-common-operating-picture skill. The kernel:

1. The rendered picture is never hand-edited; its inputs may be.
2. Every line is a measurement or an estimate, and an input or an outcome, and says which. A measurement carries value, time, collector, subject, universe and shape; an estimate carries a range, its basis, and the observation that would prove it wrong.
3. Every quantity declares how it moves (constant, drifting, scheduled) and what would be a surprise; the picture shows the last measurement, its age, and the projection, and flags the surprise.
4. Supersede in place, never overwrite; tests count unmarked lines only.
5. Gaps are listed, each naming its collector and the decision it blocks, and the list is never empty.
6. Read the picture before you measure or assert state; re-measure for a named cause, never for comfort.
7. One horizon per line, not per document: current operations measured by command, the running estimate maintained, plans as intent with gates that name their command. Records keep every horizon and are never rewritten.
8. Never report clean: checked with its fields, or unchecked with a reason and no value.

A claim about what this turn changed follows Claim Style; a standing fact this turn did not touch follows this.
`assessment` is the process, never a line. A periodic report is a measurement at its stamp and an estimate thereafter.

## Environment Setup

This project uses **uv** (Astral) for interpreters, environments, and packages. **All commands must run inside the venv.**

```bash
# First-time setup
curl -LsSf https://astral.sh/uv/install.sh | sh   # If uv is not installed
uv python install 3.12             # uv-managed interpreter (no system coupling)
uv venv --managed-python           # Create .venv on the managed interpreter
uv pip install --python .venv -e ".[dev]"
cp .env.example .env               # Add your API keys
```

**Always use the venv's Python/pytest**:
```bash
source .venv/bin/activate           # Activate before working
# OR use the venv directly:
.venv/bin/pytest                    # Run tests without activating
```

uv venvs do not bundle pip. Run every package operation from the project root as `uv pip <command> --python .venv ...`; never `sudo pip`, never system pip. Name the target every time: a `VIRTUAL_ENV` inherited from another repo's shell outranks the project's `.venv`, and a bare `uv pip install` lands there.

## Quick Commands

```bash
# Run tests (venv must be active, or use .venv/bin/pytest)
pytest                             # All tests
pytest -k test_name                # Tests matching pattern
pytest -x                          # Stop on first failure
pytest --pdb                       # Debug on failure

# Install optional dependencies
uv pip install --python .venv -e ".[excel]"       # Excel utilities (pandas, openpyxl, xlsxwriter)
uv pip install --python .venv -e ".[slack]"       # Slack integration
uv pip install --python .venv -e ".[database]"    # PostgreSQL
uv pip install --python .venv -e ".[all]"         # Everything
```

## Project Overview

This is a Python project template with reusable utility modules. It provides a starting structure for new projects with proven patterns for testing, configuration, and development workflow.

## Tech Stack

- **Language**: Python (3.11+)
- **Base Dependencies**: pyyaml, python-dotenv
- **Optional**: pandas, openpyxl, xlsxwriter, slack-sdk, psycopg, numpy

## Project Structure

```
tacsop/
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
2. **TCS** — Multi-step with pass/fail criteria (Task, Condition, Standard, plus a Purpose column); also the universal task detail unit within all plan types
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
