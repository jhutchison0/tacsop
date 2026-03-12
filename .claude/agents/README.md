# Agent Roster

This directory contains the project's prepositioned agents. **Read this before deploying any multi-agent plan.**

Each agent's `.md` file is the authoritative definition of its role, boundaries, and workflow. This README is the index and composition guide.

## The Roster

| Agent | Model | Writes Code? | Primary Domain |
|-------|-------|-------------|----------------|
| `test-runner` | haiku | No | All — runs pytest, reports results |
| `code-reviewer` | inherit | No | Reviews against design pillars, code quality, security |
| `python-prototyper` | sonnet | Yes | Full Python implementation across all modules |

## How to Compose a Team

### Scale to the work

Not every task needs all agents. Scale to fit:

| Work Size | Example | Agents |
|-----------|---------|--------|
| Config tweak | Update a YAML value | 1 (you) |
| Bug fix | Fix a function, add test | python-prototyper + test-runner (2) |
| New utility | Add a new module to utils/ | python-prototyper + test-runner + code-reviewer (3) |
| New feature | Add a new project component | All 3 agents |

### Assign file ownership

Every file must have exactly one owner. If two agents need to touch the same file, restructure the task.

Typical ownership boundaries:
- `src/myproject/` → python-prototyper
- `tests/` → python-prototyper (writes), test-runner (runs)
- `config/`, `docs/` → python-prototyper

## Adding Project-Specific Agents

As your project grows, add Level 1 (domain-specific) agents:

1. Create the agent file in this directory
2. Update this README's roster table
3. Update the agent table in `CLAUDE.md`

Keep Level 0 agents (test-runner, code-reviewer, python-prototyper) unchanged — they're portable across projects.

## Common Mistakes

**Inventing ad-hoc roles**: Check if an existing agent covers the need before creating a new one.

**Skipping code-reviewer on significant changes**: Reviews cost little and catch issues early.
