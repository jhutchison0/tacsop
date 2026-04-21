# Doctrine Updates

Changes to shared workflow commands and planning framework. Downstream repos are notified via `.claude/upstream-update.md` — review and selectively merge.

---

## 2026-04-21: Agent Output Convention — docs/reviews/ and YYYYMMDD_<subject>.md

**Files changed**: `.claude/agents/decision-scientist.md`, `.claude/agents/code-reviewer.md`, `.claude/agents/proposer.md`, `.claude/agents/python-prototyper.md`, `.claude/README.md`, `.claude/teams/decision-science.md`, `.claude/teams/feature-development.md`, `CLAUDE.md`, `config/project.yaml`

**Files added**: `docs/reviews/` directory

### Change

Agents that write reports, audits, or analysis now share a single output convention:
- **Directory**: `docs/reviews/` (dedicated, not the `docs/` root)
- **Filename**: `YYYYMMDD_<subject>.md` (date first, sorts chronologically)
- **Author**: goes in the file header, not the filename

Previously, agents wrote to `docs/` with inconsistent filenames (e.g., `decision_audit_YYYYMMDD.md` — date buried, no subject, not sortable). The new convention matches the session doc pattern and makes it easy to find the most recent review across all agents.

Each agent definition now includes a standard report header template:

```markdown
# [Report title]

**Author**: [agent-name]
**Date**: YYYY-MM-DD
**Type**: [MAUT audit / Code review / Config review / ...]
```

### Scope changes per agent

| Agent | Write scope (before) | Write scope (after) |
|-------|---------------------|---------------------|
| `decision-scientist` | `docs/` | `docs/reviews/` |
| `code-reviewer` | `docs/` | `docs/reviews/` |
| `proposer` | `docs/` | `docs/plans/` (proposals), `docs/reviews/` (analysis) |
| `python-prototyper` | `docs/` | `docs/sessions/`, `docs/plans/` (explicitly, no `docs/reviews/`) |

The `.claude/README.md` scope matrix was updated to reflect explicit per-directory rows (`docs/sessions/`, `docs/plans/`, `docs/reviews/`) instead of a single `docs/` column.

`config/project.yaml` `paths:` section now includes `reviews: "docs/reviews/"`.

### Action Required

**For all repos with agent definitions** — update each agent that writes reports:

1. **`decision-scientist.md`** (if present): change output path to `docs/reviews/YYYYMMDD_<subject>.md`. Add the standard header template to the Output Format section.

2. **`code-reviewer.md`** (or equivalent auditor): change output path to `docs/reviews/YYYYMMDD_<subject>.md`. Add the standard header template.

3. **`proposer.md`** (if present): proposals → `docs/plans/YYYYMMDD_<subject>.md`, investigation reports → `docs/reviews/YYYYMMDD_<subject>.md`. Update Scope Write to enumerate both.

4. **`python-prototyper.md`** (if present): narrow `docs/` Write grant to `docs/sessions/`, `docs/plans/` explicitly — prototypers should not write to `docs/reviews/`.

5. **`.claude/README.md` scope matrix**: replace single `docs/` row with three rows: `docs/sessions/`, `docs/plans/`, `docs/reviews/`. Assign Write access only to the agents that own each directory.

6. **`config/project.yaml`**: add `reviews: "docs/reviews/"` under `paths:`.

7. **Create `docs/reviews/`**: `mkdir -p docs/reviews && touch docs/reviews/.gitkeep`

8. **Team templates** (`.claude/teams/*.md`): update any role description that says "write to `docs/`" to name the specific subdirectory.

9. **`CLAUDE.md` agent table**: if `decision-scientist` is listed, confirm it shows `docs/reviews/` as its output. If it is absent, add it.

---

## 2026-03-31: Session-Start — Add Git Sync

**Files changed**: `.claude/commands/session-start.md`

### Change

Added `git fetch && git pull` as the first command in Step 4 (Verify Health). Session-start now syncs with remote before running tests or checking status.

### Action Required

Update your `.claude/commands/session-start.md` Step 4 to include the fetch/pull before other health checks:

```bash
git fetch && git pull # Sync with remote before anything else
pytest                # Verify all tests pass
git status            # Check for uncommitted changes
git branch -v         # Current branch state
```

---

## 2026-03-26: Decision Science Module — Shared MAUT/MCDA Utility

**Files added**: `src/myproject/decision_science/` (4 modules), `.claude/agents/decision-scientist.md` (new), `.claude/teams/decision-science.md` (new)

### 1. Shared MAUT Scorer

A new `decision_science` subpackage provides the infrastructure that 6+ repos were building independently:

- **`value_functions.py`** — 7 pluggable value functions: `linear`, `exponential`, `logarithmic`, `logistic`, `step`, `gaussian`, `piecewise_linear`. All return `float` in `[0, 1]`.
- **`scorer.py`** — `MAUTScorer` class with additive aggregation `U = Σ w×u`. Includes:
  - `from_yaml()` — config-driven model loading (mandatory, not optional)
  - `from_weights()` — bridge to `weights.py` `generate_weights()` output
  - `score()` / `rank()` — with weight validation and value function output bounds checking
  - `explain()` on `DecisionResult` — structured dict for programmatic consumption
  - `dominance_check()` — weight-independent dominated alternative detection
- **`sensitivity.py`** — `one_at_a_time()`, `monte_carlo()` (Dirichlet sampling), `scenario_compare()`, `robustness_report()` (single confidence metric)
- **`visualization.py`** — `radar_chart()`, `tornado_plot()`, `rank_stability_heatmap()` (matplotlib optional)

### 2. Decision-Scientist Agent

New Level 1 agent that audits decision models for MAUT correctness:
- Validates weights sum to 1.0, no negatives, value functions output in [0,1]
- Flags missing sensitivity analysis, inappropriate value function shapes
- Audit-only scope: reads everything, writes only to `docs/`

### 3. Decision-Science Team

New 5-agent team template: proposer + decision-scientist + python-prototyper + test-runner + code-reviewer. Use for any MAUT/MCDA work.

### 4. YAML Config Schema

Decision models are defined in YAML:

```yaml
criteria:
  - name: effectiveness
    weight: 0.35
    value_fn: linear
    params: {low: 0, high: 100}
  - name: risk
    weight: 0.40
    value_fn: gaussian
    params: {center: 0, sigma: 50}
  - name: survival
    weight: 0.25
    value_fn: logistic
    params: {midpoint: 0.5, steepness: 8}
```

### Action Required

**If your repo does MAUT/MCDA scoring** (tactics-game, quest-engine, project-megan, agent-eval, paperboy, elephant-graveyard):
- Review the shared module — it can replace your local scorer implementation
- Your domain-specific criteria, value function parameters, and profiles stay in your repo
- The scoring infrastructure, sensitivity analysis, and visualization come from utils
- Migration is opt-in and additive — nothing breaks if you don't adopt

**If your repo does NOT do MAUT/MCDA**:
- No action required — ignore this update
- The module exists if you ever need weighted multi-criteria decision analysis

**Agent/team adoption** (all repos):
- Copy `.claude/agents/decision-scientist.md` if you do any form of weighted scoring
- Copy `.claude/teams/decision-science.md` for MAUT/MCDA workflow support
- Update `.claude/README.md` agent roster and scope matrix if you adopt either

---

## 2026-03-24: Planning Framework, Proposer Agent, and Doctrine Propagation

**Files changed**: `.claude/commands/task.md`, `.claude/commands/session-start.md`, `.claude/agents/proposer.md` (new), `.claude/README.md`, `.claude/teams/feature-development.md`, `CLAUDE.md`

### 1. TCS Universal + Wave Terminology

- **TCS is now the universal task detail standard** — every task within a CONOP or OPORD is written at TCS (Task, Condition, Standard) level. The document type escalates the frame; the task granularity stays consistent.
- **"Wave" terminology adopted for tactical execution** — agent teams deploy in *waves* within CONOPs and OPORDs. "Phase" is reserved for strategic roadmap milestones (`project.yaml` build_phases). A campaign-level OPORD may contain phases of waves, but this is deliberate and infrequent.
- **New section added**: "Terminology: Phases vs Waves" in the escalation ladder.

### 2. Proposer Agent

- **New `proposer` agent** — analyzes problems and proposes bold approaches before implementation. Reads the full codebase, writes proposals to `docs/`. Instructed not to write code — same access pattern as `code-reviewer`.
- **Feature-development team updated** — workflow is now: proposer explores and proposes → code-reviewer challenges → user decides → python-prototyper builds → test-runner verifies.
- **Agent roster is now 4 agents** — test-runner, code-reviewer, proposer, python-prototyper.
- Inspired by the AgenticSciML paper (arxiv.org/html/2511.07262v2) — structured debate before implementation produces better solutions than jumping straight to code.

### 3. Doctrine Propagation System

- **Upstream doctrine notifications** — utils now maintains this changelog and can propagate notifications to downstream repos via `.claude/upstream-update.md`.
- **Session-start check (Step 3.6)** — `/session-start` now checks for `.claude/upstream-update.md` and surfaces it if present. This is how you'll receive future updates.

### Action Required

**Planning framework**:
- Review your `.claude/commands/task.md` escalation ladder against `utils/.claude/commands/task.md`
- Update "phase" references within CONOP/OPORD descriptions to "wave"
- Add TCS detail requirement to CONOP and OPORD level descriptions
- Add the "Terminology: Phases vs Waves" section
- Update your `CLAUDE.md` planning escalation summary to match

**Proposer agent**:
- Copy `.claude/agents/proposer.md` from utils (or create your own adapted version)
- Add proposer to your agent catalog and scope matrix in `.claude/README.md`
- Update `.claude/teams/feature-development.md` to include the propose → challenge → implement workflow
- Add proposer to your `CLAUDE.md` agent table
- Update any "3-agent" references to "4-agent"

**Doctrine propagation** (do this first so you receive future updates):
- Add Step 3.6 to your `.claude/commands/session-start.md`:

```markdown
## Step 3.6: Check Upstream Doctrine Updates

Check if `.claude/upstream-update.md` exists. If it does:
- Read and surface the contents to the user
- Flag it prominently: **"Upstream doctrine update available — review before proceeding"**
- Do NOT delete the file — the user decides when to act on it
```

- After reviewing all updates, delete `.claude/upstream-update.md` from your repo
