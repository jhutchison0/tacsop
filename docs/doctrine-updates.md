# Doctrine Updates

Changes to shared workflow commands and planning framework. Downstream repos are notified via `.claude/upstream-update.md` — review and selectively merge.

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
