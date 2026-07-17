# tacsop

**TACSOP** — *Tactical Standing Operating Procedure*: the document through which a headquarters publishes the standing procedures its units operate by, and from which each unit derives its own local SOP.

Here: a Python project template and upstream doctrine hub for Claude Code agent workflows — the doctrinal foundation for agents and teams to operate together, and for task escalation. (Renamed from `utils` 2026-07-17; see [ADR-0002](docs/adr/0002-rename-repository-to-tacsop.md).)

This repo serves two purposes:

1. **Template** — Clone it to start a new Python project with proven utilities, testing infrastructure, and a full Claude Code agent workflow already wired up.
2. **Upstream Hub** — Maintain shared agent best practices, decision science tooling, and workflow commands here, then propagate updates to all downstream repos.

## What's Included

| Category | Contents |
|----------|----------|
| **Utilities** | Logging (colored, timezone-aware), geo (haversine, bearing), Excel tables, Slack webhooks, PostgreSQL/JSONB, multiprocessing patterns, SMARTER weights |
| **Decision Science** | MAUT scorer with 7 value functions, sensitivity analysis (OAT, Monte Carlo), visualization (radar, tornado, heatmap) — all config-driven via YAML |
| **Agent Workflow** | 4 agents (test-runner, code-reviewer, proposer, python-prototyper), team templates, session commands (`/session-start`, `/session-end`, `/pcc`, `/pci`, `/task`) |
| **Testing** | 189 tests, 53% coverage, pytest-cov configured |

## Line of Effort 1: Build a New Repo

Clone this template and strip it down to what your project needs.

```bash
git clone <this-repo> my-new-project
cd my-new-project
rm -rf .git && git init

# Rename the package
mv src/myproject src/my_new_project
# Update references in: pyproject.toml, config/project.yaml, CLAUDE.md, tests/

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Verify
pytest
```

Delete modules you don't need, reset `docs/tasks.md` and `docs/sessions/`, and make your first commit. See **[From Template to Project](docs/design/from_template_to_project.md)** for the full Day-1 checklist.

## Line of Effort 2: Propagate Updates Downstream

When agent workflows, commands, or shared utilities change here, push updates to all downstream repos.

```bash
# 1. Document the change in the changelog
#    Add a new ## YYYY-MM-DD entry to docs/doctrine-updates.md

# 2. Propagate to all downstream repos
python scripts/propagate_doctrine.py          # writes .claude/upstream-update.md
python scripts/propagate_doctrine.py --dry-run # preview without writing

# 3. Downstream repos see the update on their next /session-start
```

The script finds all repos under `~/projects/` with `.claude/commands/` directories. Updates append to existing notifications — repos that haven't reviewed earlier updates won't lose them.

## Project Structure

```
tacsop/
├── src/myproject/
│   ├── utils/              # Reusable utility modules
│   │   ├── logger.py       # get_logger() — colored, timezone-aware, console or file
│   │   ├── geo.py          # Haversine distance and bearing
│   │   ├── excel.py        # DataFrame-to-Excel tables
│   │   ├── parallel.py     # Multiprocessing patterns
│   │   ├── slack.py        # Slack webhook posting
│   │   ├── database.py     # Synchronous PostgreSQL with JSONB
│   │   ├── weights.py      # SMARTER/reciprocal/rank-sum weights
│   │   └── math_utils.py   # Combinatorics
│   └── decision_science/   # MAUT/MCDA subpackage
│       ├── scorer.py       # MAUTScorer with from_yaml()
│       ├── value_functions.py
│       ├── sensitivity.py
│       └── visualization.py
├── .claude/                # Agent definitions, teams, commands, skills
├── scripts/                # Doctrine propagation tooling
├── config/project.yaml     # Project identity, phases, state
├── tests/                  # 189 tests (pytest)
├── docs/
│   ├── design/             # Pillars, roadmap, template guide
│   ├── sessions/           # Session documentation
│   ├── plans/              # CONOPs and OPORDs
│   └── doctrine-updates.md # Changelog for downstream propagation
└── pyproject.toml          # Packaging, deps, coverage config
```

## Quick Start (Development)

```bash
source .venv/bin/activate
pytest                     # Run all tests
pytest --cov               # With coverage report
pytest -k test_name        # Run specific tests
```

## Standards

- **pathlib everywhere** — No `os.path`. Use `Path` for all filesystem operations.
- **Shift-left testing** — Tests ship alongside code, not as an afterthought.
- **Config-driven** — `config/project.yaml` is the source of truth. YAML for structure, `.env` for secrets.

## License

GPL v3 — See [LICENSE](LICENSE) for details.
