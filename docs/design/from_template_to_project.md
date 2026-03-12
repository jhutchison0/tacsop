# From Template to Project

**Audience**: A developer who just cloned this repo and needs to ship something real.

**What this document is**: A concrete playbook for turning the template into your project. Read it once, then use the Day-1 checklist to get your hands dirty.

---

## 1. Overview

This template gives you a working Python project scaffold with zero wasted code. What you get on clone:

- `src/myproject/` package with eight production-quality utility modules
- `pyproject.toml` with optional dependency groups (install only what you need)
- pytest infrastructure with an example passing test suite
- Claude Code workflow: session commands, three prepositioned agents, PCC/PCI quality gates
- Design pillars, roadmap, and task escalation framework ready to fill in

What you do **not** get: a README, a CI pipeline, and working test coverage beyond `math_utils`. Those gaps are documented in Section 9.

**Why it exists**: Starting a Python project from scratch means making a dozen identical decisions every time — how to structure packages, how to handle optional deps, whether to use src-layout, how to set up logging, how to run parallel tasks. This template makes those decisions once so you can focus on the domain.

**The model**: `config/project.yaml` is the runtime source of truth. `pyproject.toml` is the packaging source of truth. They don't overlap. Everything else — agents, commands, skills — is workflow infrastructure that guides how you work, not what you build.

---

## 2. Day-1 Checklist

Do these steps in order. Every file that needs changing is listed.

### Step 1: Rename the package

Replace `myproject` with your project name everywhere. Pick a name that is a valid Python identifier (lowercase, underscores, no hyphens).

```bash
# In the terminal — replace "newname" with your actual project name
NEW=newname

# Rename the source directory
mv src/myproject src/$NEW
```

Files that contain `myproject` and need to be updated:

| File | What to change |
|------|----------------|
| `pyproject.toml` | `name = "myproject"` → `name = "newname"` |
| `pyproject.toml` | `"myproject[dev,excel,...]"` in `all` group → `"newname[...]"` |
| `config/project.yaml` | `name: "myproject"` → `name: "newname"` |
| `config/project.yaml` | `source: "src/myproject"` → `source: "src/newname"` |
| `CLAUDE.md` | All occurrences of `myproject` in paths and examples |
| `.claude/commands/pci.md` | `src/myproject/utils/*.py` path references |
| `.env.example` | Comments referencing `src/myproject/utils/` |
| `src/newname/utils/*.py` | Module docstrings — none reference `myproject` directly, but verify |
| `tests/conftest.py` | Any import of `myproject` |
| Any test files | `import myproject` or `from myproject` |

### Step 2: Update project metadata

In `pyproject.toml`:
```toml
[project]
name = "newname"
version = "0.1.0"
description = "What your project actually does"
# Add these if you want them:
authors = [{name = "Your Name", email = "you@example.com"}]
```

In `config/project.yaml`:
```yaml
project:
  name: "newname"
  version: "0.1.0"
  description: "What your project actually does"
```

### Step 3: Set up the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"          # Base + test deps only
cp .env.example .env             # Then fill in any secrets you need
```

Install optional deps for any utilities you're keeping:
```bash
pip install -e ".[excel]"        # If keeping excel.py
pip install -e ".[slack]"        # If keeping slack.py
pip install -e ".[database]"     # If keeping database.py (fix it first — see Section 9)
pip install -e ".[weights]"      # If keeping weights.py
```

### Step 4: Verify tests pass

```bash
pytest
```

You should see the `math_utils` tests pass. If anything fails, the rename step missed something — re-check all `myproject` references.

### Step 5: Update the task list

Create `docs/tasks.md` if it doesn't exist (run `/task list` in Claude Code to generate the stub). Add your first real tasks here.

### Step 6: Initial commit

```bash
git add -A
git commit -m "[config] Rename myproject → newname, update metadata"
```

This is your project's starting line. Everything before this point is template. Everything after is yours.

---

## 3. What to Keep, Evaluate, or Remove

Every module is optional unless your project actually needs it. Be ruthless — dead code in a template becomes dead code in your project.

### Keep (universal)

**`logger.py`** — Every project needs logging. This implementation handles the two common footguns (duplicate handlers on re-import, timezone-correct timestamps) correctly. Drop it in and use `LoggerSetup.setup_logger()`.

One caveat: the `Formatter.converter` assignment on line 72 is a global mutation that affects all formatters in the process. If you set up two loggers with different timezones, the last one wins. Fine for most projects; document the constraint if your project runs multiple loggers concurrently.

### Evaluate (domain-dependent)

**`geo.py`** — Keep if your project involves geographic data. Pure stdlib, no deps, correct haversine and bearing formulas. Drop it if you're not doing geo work.

**`parallel.py`** — Keep if you need multiprocessing. Two patterns: producer-consumer for heterogeneous tasks, starmap for homogeneous batch work. Well-designed default worker counts. Drop it if your workload is single-threaded.

**`weights.py`** — Keep if you're doing multi-criteria decision analysis or ranking. Three weighting methods (SMARTER, rank reciprocal, rank sum) with tie handling. Requires `numpy` + `pandas` (`pip install -e ".[weights]"`). Drop it if you're not doing MCDA work.

**`excel.py`** — Keep if you're generating Excel reports. Handles DataFrame-to-table formatting cleanly. Has a known bug (see Section 9). Requires `pandas`, `openpyxl`, `xlsxwriter`. Drop it if you're not generating Excel files.

**`slack.py`** — Keep if you need Slack notifications. Thin wrapper — the whole module is 37 lines. Easy to understand and extend. Requires `slack-sdk`. Drop it if you're not posting to Slack.

**`database.py`** — **Do not use as-is.** The sync/async mismatch makes `insert_or_update_data` uncallable at runtime. Fix the mismatch before building on this module (see Section 9). Keep after fixing if you need PostgreSQL + JSONB storage. Drop it if you're using a different database or ORM.

### Consider removing

**`math_utils.py`** — The module itself acknowledges that `math.comb()` is in the stdlib since Python 3.8. These implementations are kept "for educational reference." If you're not doing combinatorics work or teaching, this is dead weight. Remove the module and its tests.

### Pattern: How to remove a module

1. Delete `src/newname/utils/the_module.py`
2. Delete `tests/unit/test_the_module.py` (if it exists)
3. Remove the corresponding optional dep group from `pyproject.toml` (if it exists only for that module)
4. Remove references from `CLAUDE.md`

---

## 4. Defining Your Project

### Filling in `config/project.yaml`

Phase 1 is already marked complete — that's the template foundation. Define your actual phases starting with Phase 2:

```yaml
build_phases:
  phase_1:
    name: "Foundation"
    status: "complete"
    deliverable: "Project template with utility modules and dev workflow"
  phase_2:
    name: "Core Feature X"          # Be specific — name the thing
    status: "in_progress"
    deliverable: "Working X that does Y, with Z test coverage"
  phase_3:
    name: "Integration"             # Can be vague if it's far out
    status: "not_started"
    deliverable: "TBD"
```

Good deliverables are concrete and verifiable. Bad: "Backend complete." Good: "API endpoints for user auth, with pytest suite at >80% coverage."

### Writing design pillars that work

The template's three pillars (`Simplicity First`, `Shift-Left Testing`, `Config-Driven`) are examples. Replace them with your project's actual constraints. The format in `docs/design/pillars.md` is the right structure:

- **Principle**: One sentence rule
- **Why**: Why this matters _for this project specifically_
- **In practice**: Concrete guidelines
- **Violation example**: A real code smell that breaks this pillar

The violation example is the most important part. Without it, pillars are aspirational. With it, they're a code review checklist.

Aim for 3-5 pillars. More than 5 means you haven't prioritized.

### Setting up the task list

Run `/task add <description>` or edit `docs/tasks.md` directly. Structure for the initial list:

```markdown
## Active

- [ ] [P1] Fix database.py sync/async mismatch — owner: unassigned
- [ ] [P1] Write README.md — owner: unassigned
- [ ] [P2] Add tests for geo.py — owner: unassigned
- [ ] [P2] Add tests for logger.py — owner: unassigned

## Blocked

## Completed
```

P1 = do now, P2 = do soon, P3 = backlog. Assign when ownership is clear. Keep it honest — a task list with 40 open items is noise.

---

## 5. Your First Design Doc

Before writing code for your project's first feature, write a design doc. This doesn't need to be long — it needs to answer the questions that will otherwise be answered implicitly by whoever writes the first file.

Use this structure in `docs/design/FEATURE_NAME.md`:

---

### Problem Statement

_One paragraph. What problem exists? Who has it? What happens today without a solution?_

> Example: Research analysts manually compile weekly briefings from 12 data sources. The process takes 4 hours and produces inconsistent output because each analyst structures differently.

### Scope

**In scope**:
- [ ] Feature A
- [ ] Feature B
- [ ] Automated test suite for the above

**Out of scope**:
- Feature C (future phase)
- Feature D (separate system)

### Key Decisions to Make Before Coding

List the decisions that will shape the architecture. Don't leave these implicit.

| Decision | Options | Recommended | Rationale |
|----------|---------|-------------|-----------|
| Storage layer | SQLite / PostgreSQL / files | PostgreSQL | Need JSONB and concurrent writes |
| Sync vs async | sync / async | sync | No I/O concurrency needed in v1 |

### Architecture Sketch

```mermaid
flowchart LR
    A[Data Source] --> B[Ingest]
    B --> C[Store]
    C --> D[Transform]
    D --> E[Output]
```

### Success Criteria

How will you know when this phase is done?

- [ ] Feature A works end-to-end with real inputs
- [ ] Test coverage for new modules > 80%
- [ ] Design pillars not violated (run `/pci`)

---

Writing this doc surfaces disagreements before they become bugs. If you can't fill it in, you don't understand the problem well enough to write the code.

---

## 6. Configuration Deep Dive

### How config flows

```mermaid
flowchart TD
    A[config/project.yaml] -->|pyyaml| B[Python dict]
    C[.env] -->|python-dotenv| D[os.environ]
    B --> E[Your Code]
    D --> E
```

YAML is for structured config (phases, paths, thresholds, toggles). Environment variables are for secrets and deployment-specific values. They serve different purposes and never overlap.

### Reading config in Python

```python
import yaml
from pathlib import Path

config_path = Path(__file__).parent.parent.parent / "config" / "project.yaml"
with config_path.open() as f:
    config = yaml.safe_load(f)

# Access values
project_name = config["project"]["name"]
phase_status = config["build_phases"]["phase_2"]["status"]
```

### Reading env vars

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into os.environ
db_host = os.environ.get("DB_HOST", "localhost")
```

Call `load_dotenv()` once at your application's entry point, not in every module.

### Adding new config

Add to `config/project.yaml`:
```yaml
# Your new section
my_feature:
  max_retries: 3
  timeout_seconds: 30
  enabled: true
```

Then read it from Python. Don't add new YAML files — one config file keeps things findable. The `config/` directory growing to 10 files is a maintenance burden.

### Adding new optional dependencies

In `pyproject.toml`:
```toml
[project.optional-dependencies]
myfeature = [
    "some-package>=1.0",
]
# Update the "all" group:
all = [
    "myproject[dev,excel,slack,database,weights,myfeature]",
]
```

Then document the install command in `CLAUDE.md`'s Quick Commands section.

### What .env.example should contain

Every key your code reads from `os.environ`, with a dummy value and a comment explaining what it is. This file is committed. The actual `.env` is never committed. Keep them in sync — if you add a new env var, add it to `.env.example` immediately.

---

## 7. Testing Strategy

### The pattern to follow

Look at `tests/unit/test_math_utils.py`. It's the only complete test in the repo. Key patterns:

- Tests are in `tests/unit/` for unit tests, `tests/integration/` for integration tests
- Test file names match module names: `test_math_utils.py` tests `math_utils.py`
- Each function gets at least one happy-path test and one edge case
- No test should depend on network, filesystem, or execution order unless that's exactly what's being tested

### Handling optional dependencies in tests

For modules that require optional deps, gate with `pytest.importorskip`:

```python
# At the top of test_excel.py
pd = pytest.importorskip("pandas", reason="pandas required for excel tests")
openpyxl = pytest.importorskip("openpyxl", reason="openpyxl required for excel tests")

# Then write your tests normally
def test_excel_style_index():
    from myproject.utils.excel import excel_style_index
    assert excel_style_index(1, 1) == "A1"
    assert excel_style_index(1, 26) == "Z1"
    assert excel_style_index(1, 27) == "AA1"
```

This skips the entire test file gracefully when deps aren't installed, rather than failing.

### Priority order for new tests

Write tests in this order (easiest to hardest):

1. Pure functions with no side effects (geo.py, math_utils.py)
2. Functions with file I/O (logger.py — use `tmp_path` fixture)
3. Functions with external deps gated by importorskip (excel.py, weights.py)
4. Functions requiring mocks (slack.py with `unittest.mock.patch`)
5. Database / multiprocessing (database.py after fixing, parallel.py)

### Running with coverage

```bash
pytest --cov=src --cov-report=term-missing
```

Note: `pytest --cov=myproject` will fail because `myproject` is not a top-level package. Use `--cov=src` to hit the `src/` layout correctly.

### Coverage target

`config/project.yaml` declares 80% as the threshold. The template ships at 4%. Closing that gap is your first real task. Section 9 lists the must-fix modules.

### Current state

The template violates its own Shift-Left Testing pillar at Phase 1 completion. Seven of eight utility modules have 0% test coverage. This is the most important thing to fix before building on top of the template.

---

## 8. Dev Workflow Guide

### The session cadence

```mermaid
flowchart LR
    A[/session-start/] --> B[Work]
    B --> C[/pcc/]
    C --> D{PCC pass?}
    D -->|No| E[Fix issues]
    E --> C
    D -->|Yes, significant change| F[/pci/]
    D -->|Yes, small change| G[Commit]
    F --> G
    G --> H[/session-end/]
```

**session-start**: Load project config, review last session doc, check task list, verify tests pass. Don't skip this — it takes 30 seconds and prevents you from working in the wrong context.

**session-end**: Git status review, PCC, commit with `[area]` tag, update tasks, write session doc. The session doc in `docs/sessions/YYYYMMDD_*.md` is your audit trail. Future-you will thank you.

### PCC vs PCI

| | PCC | PCI |
|---|---|---|
| **Speed** | Seconds | Minutes |
| **Checks** | Secrets, tests, debug artifacts, git state | All of PCC + type hints, docstrings, error handling, test coverage |
| **When** | Before every push | Before merge/PR, or when PCC passes but you want confidence |
| **Decision** | Pass/fail, no judgment | Context-aware findings with recommendations |

Run PCC always. Run PCI when the diff is large or touches core logic.

### Task escalation: when to promote

Don't over-plan. Start with a task. Promote only when complexity demands it.

| Situation | Level |
|-----------|-------|
| Clear action, one session, 1-3 files | Task |
| Multi-step, needs pass/fail criteria | TCS |
| Multiple phases, design decisions, spans sessions | CONOP |
| Strategy decided, executing sequentially | OPORD |

The decision tree from `/task`:
```
Can I explain this in one sentence?      → Yes: Task
Do I need pass/fail criteria?            → Yes: TCS minimum
Are there design decisions to make?      → Yes: CONOP
Is the strategy decided, just execute?   → Yes: OPORD
```

Erring toward CONOP for anything uncertain is better than erring toward Task. A task that balloons into a 3-session effort without a plan is chaos.

### Agent usage

| Team size | When | Template |
|-----------|------|----------|
| Solo | Config changes, small bug fixes | Just you |
| 2 agents | Bug fix with tests | `.claude/teams/bug-fix.md` |
| 3 agents | New utility module | `.claude/teams/feature-development.md` |
| Review | Code review pass | `.claude/teams/code-review.md` |

Read `.claude/README.md` before deploying a team. The key rule: every file has exactly one owner. If two agents need to touch the same file, restructure the task.

Add domain-specific Level 1 agents as your project grows. Level 0 agents (test-runner, code-reviewer, python-prototyper) are portable — don't modify them.

### Commit message conventions

Use `[area]` tags as defined in `session-end.md`:

```
[util] Add retry logic to slack.py
[config] Add max_retries to project.yaml
[doc] Write initial design doc for feature X
[fix] Correct keep_index logic in update_excel_workbook
[test] Add tests for geo.py haversine and bearing
[infra] Add GitHub Actions CI workflow
```

---

## 9. Known Issues & First Fixes

These are bugs and gaps the next team inherits. Fix them before building on top.

### Critical: database.py sync/async mismatch

`DatabaseManager.__init__` uses `psycopg.connect()` (synchronous). But `insert_or_update_data` is `async` and calls `await self.conn.cursor()` — which doesn't exist on a sync connection. This raises `TypeError` at runtime.

**Fix**: Convert to fully async using `psycopg.AsyncConnection`:

```python
# Change __init__ to async factory method
@classmethod
async def create(cls, db_config: dict[str, str]) -> "DatabaseManager":
    instance = cls.__new__(cls)
    instance.conn = await psycopg.AsyncConnection.connect(**db_config)
    await instance._create_table()
    return instance
```

Or simplify to fully synchronous if you don't need async. Don't leave the mismatch.

### Critical: Test coverage is 4%

Before building anything new, add tests for at least `geo.py` and `logger.py`. These are the easiest (pure functions, no external deps). Together they will bring coverage above 25% and validate the test infrastructure.

Start with `tests/unit/test_geo.py`:
```python
from myproject.utils.geo import get_distance, get_bearing

def test_same_point_distance():
    assert get_distance(0, 0, 0, 0) == 0.0

def test_known_distance():
    # Chicago to NYC is approximately 1145 km
    dist = get_distance(41.85, -87.65, 40.71, -74.01)
    assert abs(dist - 1145) < 10
```

### Warning: excel.py keep_index logic inverted

In `update_excel_workbook` at line 97-98:

```python
if not keep_index:
    df = df.reset_index(level=0, drop=False)  # drop=False adds index as column
```

When `keep_index=False`, the intent is to not include the index — but `drop=False` adds it as a column. Compare to `save_excel_table` which correctly inserts the index column only when `keep_index=True`. The logic is inverted.

**Fix**: Change to `drop=True` when `keep_index=False`, or restructure to match `save_excel_table`'s pattern.

### Warning: session-end.md skill has leftover paperboy content

`.claude/skills/session-end.md` contains domain-specific commit tags (`[source]`, `[select]`, `[distill]`, `[pipeline]`, `[tts]`) and branch names (`dev-source`, `dev-select`) from a different project. This is a Level 0 skill — it must be project-agnostic.

**Fix**: Replace domain-specific tags with generic examples. Update branch naming section to use generic names.

### Warning: SKILLS_FRAMEWORK.md references "paperboy"

`.claude/skills/SKILLS_FRAMEWORK.md` lines 103-106 list example Level 1 skills for "paperboy" by name. This exposes the template's origin project.

**Fix**: Replace with generic placeholder examples (e.g., "For a data pipeline project, Level 1 skills might include: `api-integration.md`, `pipeline-debugging.md`").

### Informational: No README.md

There's no `README.md` at the project root. `CLAUDE.md` is for Claude Code, not for humans on GitHub. A new team member cloning the repo has no entry point.

**Fix**: Write a minimal README covering: what the project does, how to set up the environment, how to run tests, and how to contribute.

### Informational: Coverage config incomplete

`pyproject.toml` has no `[tool.coverage.run]` or `[tool.coverage.report]` section. Add:

```toml
[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## 10. Common Pitfalls

**Keeping modules you don't need.** Dead code accumulates debt. If your project isn't doing geo work, delete `geo.py` on Day 1. Removing it later is harder.

**Not writing the first design doc.** The impulse to jump straight into code is strong when you have a working scaffold. Resist it. Thirty minutes writing the problem statement and scope catches half the architecture mistakes before they're written.

**Skipping session-start.** It feels like overhead until the session where you spend 20 minutes re-orienting because you forgot what was done last time.

**Letting the task list grow unchecked.** A task list with 40 items is not a task list — it's a guilt log. Keep active tasks under 10. Promote complex work to plans. Archive stale tasks.

**Running PCI instead of PCC for small changes.** PCC is cheap. Run it on every push. Save PCI for big diffs and pre-merge reviews.

**Building on top of database.py before fixing the sync/async bug.** This is the most dangerous pitfall. The module looks correct — it has type hints, docstrings, proper structure. The bug is subtle. If you write application code that calls `insert_or_update_data` before fixing the mismatch, you'll get a runtime error that's annoying to trace back.

**Treating design pillars as aspirational rather than enforceable.** Pillars only work if PCI checks against them and code review flags violations. If your pillar says "every new component includes tests" and a PR adds 200 lines with zero tests, that's a violation, not a missed ideal.

**Not updating .env.example when adding new secrets.** Future team members will be missing env vars with no indication of what's needed. `.env.example` is documentation. Keep it current.
