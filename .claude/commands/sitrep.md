# SITREP — Status Report

Generate a team-facing status report summarizing what was built, what was found, and what's next. Unlike `/task brief` (internal task inventory), a SITREP is a narrative outbrief for teammates and leadership.

**User's scope filter**: $ARGUMENTS

## Sources to Read

Read ALL of these to build the report:

1. `config/project.yaml` — version and phase (identity), and `lessons_learned` if the repo keeps one
2. `docs/tasks.md` — the `## Focus` section (the campaign's order), active and pending items, and the defects KNOWN ISSUES reports
3. `docs/gaps.md` — open gaps: what nobody can see yet, and the decision each one blocks
4. Newest file in `docs/sessions/` by name (`ls docs/sessions/*.md | sort | tail -1`; on a date with two docs, both) — last session details
5. `git log --oneline -10` — recent commit messages
6. `git log --oneline main..HEAD` — commits not yet on main (if on a dev branch)

## Scope Filtering

If the user provided a scope argument (e.g., `/sitrep api`, `/sitrep config`, `/sitrep tests`):

- Filter all sections to only include items related to that scope
- Search the codebase for concrete details: function signatures, config values, test counts
- Example: `/sitrep tests` → find test changes, pytest results, coverage numbers

If no scope argument, report on everything since the last merge to main (or last session).

## Filling in Concrete Details

A good sitrep includes specifics, not just summaries. When reporting on a capability:

- **Functions**: Find the actual function/class signature and include it
- **Config**: Find the actual config values, thresholds, settings
- **Test results**: Run `pytest -q 2>&1 | tail -5` for current counts
- **Metrics**: Pull specific numbers from session docs with the date each was taken; a number a reader will act on today is measured again, not restated
- **Known issues**: Include the specific symptom and magnitude, not just "there's an issue"

## Output Format

Generate the report in this format:

```
SITREP — [Date] — [Focus Area or "Full Project"]
=================================================

PERIOD: [Date range or "since last session"]
BRANCH: [current branch]
MERGE STATUS: [ahead/behind main by N commits, or "on main"]

COMPLETED:
  - [Capability with concrete details: function name, config key, what it does]
  - [Another capability...]

KEY FINDINGS:
  - [What was validated, discovered, or disproved — with numbers]

TEST STATUS:
  - [X passed, Y failed, Z errors — from pytest output]

KNOWN ISSUES:
  - [Issue]: [specific symptom and magnitude]

GAPS (open rows in docs/gaps.md):
  - [What nobody can see yet]: [the decision it blocks]

BLOCKED:
  - [Item]: [what's blocking it]

NEXT:
  - [The Focus section's next steps, then priority items from the task list]

OPEN DECISIONS:
  - [Decisions that need team input, if any]
```

## Style Guidelines

- **Lead with what was delivered**, not what was attempted
- **Include function/config specifics** — teammates should be able to find and use what was built
- **Numbers over adjectives** — "14 tests passing, 2 collection errors from missing deps" not "tests mostly work"
- **Known issues get the same specificity** — include the specific symptom, not "there's a problem"
- **Keep it to one screen** — if it scrolls too much, cut the least important items
- **No internal jargon about the planning framework** — teammates don't need to know about TCS/CONOP/OPORD levels; just tell them what was done and what's next
