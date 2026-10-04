# Session Start - Load Context

Load project context and prepare for a new development session.

## Step 1: Read Project Configuration

Read `config/project.yaml` - the central source of truth containing:
- Current phase and version
- Design pillars
- Build phases with status tracking
- Directory structure
- The machine roster (`machines:`), read in Step 1.5

## Step 1.5: Identify the Machine

```bash
.venv/bin/python -m src.myproject.utils.machine
```

Prints one line, for example `titanx (workstation, work+personal)`. Report it.

This runs before Step 4 because Step 4 is the first step whose behavior depends
on where you are: which remotes reach, whether a git identity is set, which
reference repos exist on disk.

If the output says the host is not in the roster, say so and offer to add it to
`config/project.yaml` under `machines:`. Do not add it silently. An unlisted box
still works; it just knows less.

## Step 2: Check Current Phase

Read `config/project.yaml` build_phases section:
- Find the current active phase (status: "in_progress")
- Understand what's being built
- What's the deliverable for this phase?
- What phases are completed vs pending?

## Step 3: Load Recent Session

Find and read the most recently modified file in `docs/sessions/` to understand what was done last session.

## Step 3.5: Check Task List

Read `docs/tasks.md` and report:
- The `## Focus` section at its head: the campaign's order, as intent
- Active tasks (count and list)
- Blocked tasks (count and reasons)
- Any stale tasks (no update in 3+ sessions)
- Suggest which active tasks align with today's work

## Step 3.6: Check Upstream Doctrine Updates

Check if `.claude/upstream-update.md` exists. If it does:
- Read and surface the contents to the user
- Flag it prominently: **"Upstream doctrine update available — review before proceeding"**
- Do NOT delete the file — the user decides when to act on it

## Step 3.7: Read the Gap Register

Read `docs/gaps.md` and report each open gap with the decision it blocks. A gap is
something nobody can see yet; if today's work rests on one of them, say so before
starting.

## Step 4: Verify Health

Run these commands:
```bash
git fetch && git pull # Sync with remote before anything else
.venv/bin/pytest      # All tests, on this project's venv (Windows: .venv\Scripts\pytest)
git status            # Check for uncommitted changes
git branch -v         # Current branch state
```

Then check the tools the session will need. Each check prints one line when
something is wrong and nothing when it is fine, so a gap surfaces in the first
minute instead of at session end:

```bash
if ! { git config user.name && git config user.email; } >/dev/null; then
  echo "NO GIT IDENTITY: commits fail (/session-end Step 3)"
fi
if [ -d "${VIRTUAL_ENV:-}" ] && [ "$(CDPATH= cd "$VIRTUAL_ENV" && pwd -P)" != "$(CDPATH= cd .venv 2>/dev/null && pwd -P)" ]; then
  echo "STRAY VIRTUAL_ENV=$VIRTUAL_ENV: an install without --python lands there, not in .venv (every uv pip command)"
fi
for cli in gh glab; do
  if command -v "$cli" >/dev/null && ! "$cli" auth status >/dev/null 2>&1; then
    echo "$cli AUTH CHECK FAILED (not logged in, or offline): merge and CI results are UNVERIFIED (/session-end Step 6)"
  fi
done
```

A stray `VIRTUAL_ENV` came from the shell that launched this session. Pin
`--python .venv` on every `uv pip` command. `unset VIRTUAL_ENV` lasts one shell,
and in Claude Code each Bash call is a new shell; to clear it, exit, run
`deactivate` in the launching shell, and relaunch. A failed `gh` or `glab` auth
check means a merge or CI result cannot be verified from here: report it as
`UNVERIFIED: <blocker>`, never as passing.

## Step 5: Summarize and Ready

Provide a brief summary. Each line ends with a tag saying where it came from, so a
reader can tell what was measured this turn from what a document held when it was
written:

- `[measured: <command>]`: run this turn; true now.
- `[identity: config/project.yaml]`: slow-moving; changes only when someone edits it.
- `[record: <file>, <date>]`: history; true as of that date, not now.
- `[intent: <file>]`: what is planned; not a state.
- `[register: <file>]`: maintained estimates and gaps.

Never restate a count or a status from a record or the task list as if it were
current. If a decision today rests on it, run the command that measures it (Picture
Style rule 6) and report that instead.

1. **Machine**: Which box this is, from Step 1.5 `[measured: .venv/bin/python -m src.myproject.utils.machine]`
2. **Version**: Current version `[identity: config/project.yaml]`
3. **Phase**: Current build phase and its deliverable `[identity: config/project.yaml]`
4. **Recent Work**: Last session summary `[record: <newest docs/sessions/ file>, <its date>]`
5. **Focus**: The campaign's next steps, in order `[intent: docs/tasks.md]`
6. **Tasks**: Active count, blocked count, top priority items `[intent: docs/tasks.md]`
7. **Gaps**: Open gaps and the decision each blocks, from Step 3.7 `[register: docs/gaps.md]`
8. **Pending**: Key items remaining in current phase `[intent: docs/tasks.md]`
9. **Test Status**: All passing or failures? `[measured: .venv/bin/pytest]`
10. **Git State**: Branch, uncommitted changes? `[measured: git status, git branch -v]`
11. **Tools**: each line Step 4's tool checks printed, or "all present" if they printed nothing `[measured: Step 4's tool checks]`

Then ask: **"What would you like to work on today?"**

---

## Quick Reference (Don't Read Unless Needed)

These docs exist for deeper dives - reference them when relevant:

| Topic | Location |
|-------|----------|
| Design philosophy | `docs/design/pillars.md` |
| Project roadmap | `docs/design/roadmap.md` |
| Phase tracking | `config/project.yaml` -> `build_phases:` section |
