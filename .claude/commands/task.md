# Task — Project Work Tracker

Manage the project task list and escalate work items through the planning framework.

**Military origin**: Task Organization — structuring work into manageable units with clear ownership, conditions, and standards. Small work stays a task. Complex work gets promoted to a plan.

## How To Use

Read the current task file and the user's request, then take the appropriate action.

**Current tasks**:
Read `docs/tasks.md` to see all current tasks.

**User's request**: $ARGUMENTS

## Subcommands

Interpret the user's arguments as one of these actions:

### `add <description>` — Add a new task
- Add to the appropriate section (Active, or under a plan heading if specified)
- Assign a priority: `P1` (do now), `P2` (do soon), `P3` (backlog)
- If no priority given, default to `P2`
- Format: `- [ ] [P2] Description — owner: unassigned`

### `list` or no arguments — Show current tasks
- Read and display `docs/tasks.md`
- Summarize: X active, Y blocked, Z completed recently
- Flag any tasks that look stale (no update in 3+ sessions)

### `done <task description or number>` — Complete a task
- Move from Active/Blocked to Completed with today's date
- Format: `- [x] 2026-03-12: Description`

### `block <task> — <reason>` — Mark a task as blocked
- Move to Blocked section with the blocking reason
- Format: `- [ ] [P2] Description — blocked: reason`

### `unblock <task>` — Move a blocked task back to Active

### `promote <task>` — Escalate a task to a planning document
- Evaluate the task against the Escalation Ladder (below)
- Recommend the appropriate document type
- If the user agrees, create a skeleton document in `docs/plans/`
- Link the task to the new document

### `update <task> — <note>` — Add a status note to a task

### `assign <task> — <owner>` — Assign ownership

### `brief` or `backbrief` — Generate a backbrief
- Summarize what's been accomplished since last session
- List open decisions and blocked items
- Recommend next actions

## Escalation Ladder

### Level 1: Task (single item in `docs/tasks.md`)
**When**: One person, one session, clear action.

**Indicators it should stay a Task**:
- Can explain in one sentence
- No design decisions needed
- Touches 1-3 files
- No dependencies on other work

### Level 2: TCS — Task, Condition, Standard
**When**: Multi-step task with measurable acceptance criteria.

TCS is also the **universal task specification unit** — every task within a CONOP or OPORD is written at TCS detail level. The document type escalates the frame; the task granularity stays consistent.

**Promote from Task when**:
- Needs explicit pass/fail criteria
- Multiple files across 2+ directories
- Has preconditions that must be verified

**Format**: Add TCS table to the task entry:
```
| Task | Condition | Standard |
|------|-----------|----------|
| Add new util | Given valid input | Returns expected output, type-hinted, docstring |
| Handle errors | Given invalid input | Raises appropriate exception, logs warning |
```

### Level 3: CONOP — Concept of Operations
**When**: Multi-wave plan with design decisions or multiple agent teams.

**Promote from TCS when**:
- Multiple waves of work that could run in parallel
- Design decisions needed before coding
- Touches 4+ components or introduces new architecture
- Will span multiple sessions

Every task within the CONOP is specified at TCS detail level.

**Format**: `docs/plans/conop_NNN_descriptive_name.md`

### Level 4: OPORD — Operations Order
**When**: Strategy is decided (CONOP approved), now executing a multi-wave operation.

**Promote from CONOP when**:
- CONOP's design decisions are resolved
- Waves must run in defined sequence
- Need to track wave-by-wave completion with checkpoints

Every task within the OPORD is specified at TCS detail level.

## Terminology: Phases vs Waves

- **Phase** — Strategic roadmap milestone (e.g., `build_phases` in `project.yaml`). Phases live outside CONOPs and OPORDs.
- **Wave** — Tactical parallel execution unit within a CONOP or OPORD. Agent teams deploy in waves.

A campaign-level OPORD may contain phases of waves, but this is deliberate and infrequent. Default to waves within orders; reserve phases for the roadmap.

## Decision Point Guidance

```
1. Can I explain this in one sentence?           → Yes: Task
2. Do I need pass/fail criteria?                  → Yes: TCS minimum
3. Are there design decisions to make?            → Yes: CONOP
4. Are there multiple parallel tracks?            → Yes: CONOP
5. Is the strategy decided, just need to execute? → Yes: OPORD
6. Does it span multiple sessions?                → Yes: CONOP or OPORD
```

## Backbrief Format

```
BACKBRIEF — [Date]
==================

SITUATION:
  Active tasks: X
  Blocked tasks: Y
  Completed this session: Z

ACTIONS TAKEN:
  - [What was done]

RESULTS:
  - [Outcome]
  - [Test status]

RECOMMENDATIONS:
  - Next priority: [task]
  - Consider promoting: [task] → [CONOP/TCS]
```

## File Location

Task list: `docs/tasks.md`

If the file doesn't exist, create it with the initial template structure.
