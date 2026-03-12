# myproject

A Python project template with reusable utility modules and a structured development workflow.

## Quick Start

```bash
# Clone and setup
git clone <repo-url> myproject
cd myproject

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install (base only — lightweight)
pip install -e ".[dev]"

# Run tests
pytest

# Install optional modules as needed
pip install -e ".[excel]"      # pandas, openpyxl, xlsxwriter
pip install -e ".[slack]"      # slack-sdk
pip install -e ".[database]"   # psycopg
pip install -e ".[all]"        # everything
```

## Starting a New Project

1. Rename `src/myproject/` to `src/yourproject/`
2. Update `name` in `pyproject.toml` and `config/project.yaml`
3. Define your design pillars in `docs/design/pillars.md`
4. Update `docs/design/roadmap.md` with your phases
5. Copy `.env.example` to `.env` and fill in your keys
6. Delete utility modules you don't need from `src/yourproject/utils/`

## Utility Modules

| Module | Description | Dependency Group |
|--------|-------------|-----------------|
| `logger` | OOP logging with colors and timezone support | (none — stdlib) |
| `math_utils` | nCr/nCk combinatorics | (none — stdlib) |
| `geo` | Haversine distance and bearing | (none — stdlib) |
| `excel` | DataFrame-to-Excel with formatted tables | `[excel]` |
| `weights` | SMARTER/reciprocal/rank-sum weight generation | `[weights]` |
| `parallel` | Producer-consumer and starmap multiprocessing | (none — stdlib) |
| `slack` | Slack channel message posting | `[slack]` |
| `database` | Async PostgreSQL with JSONB | `[database]` |

## Project Structure

```
├── src/myproject/utils/    # Reusable utility modules
├── config/project.yaml     # Project identity and phases
├── tests/                  # pytest test suites
├── docs/                   # Design docs, sessions, plans
├── .claude/                # Agents, commands, skills
├── archive/                # Old code preserved for reference (gitignored)
└── pyproject.toml          # Modern Python packaging
```

## Development Workflow

This template includes Claude Code infrastructure for structured development:

- `/session-start` — Load context and check project health
- `/session-end` — Commit, document, and update tasks
- `/pcc` — Pre-Code Check before pushing
- `/pci` — Pre-Code Inspection for deeper review
- `/task` — Track and escalate work items

## License

GPL v3 — See [LICENSE](LICENSE) for details.
