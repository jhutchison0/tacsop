# Session End Workflow

Guide me through ending this development session properly.

## Step 1: Review Changes
- Run `git status` to see all modified and untracked files
- Run `git diff` to review the actual changes
- Identify any files that shouldn't be committed (secrets, temp files, etc.)

## Step 2: Pre-Code Check (PCC)

Run the full `/pcc` checklist before committing. The authoritative check list lives in `.claude/commands/pcc.md`; do not re-enumerate it here (an earlier copy of the list drifted from `pcc.md` and was caught 2026-08-14). Two session-end extras `/pcc` does not cover:

1. **Large files** - No model files (.bin, .pkl, .pt, .pth, .h5, .onnx, .safetensors, .parquet) staged
2. **Config validation** - `config/project.yaml` parses correctly

**If PCC fails**: Fix issues before proceeding to commit.

**If PCC passes but changes are significant** (new module, schema changes, API changes): Consider running `/pci` for deeper inspection.

See `/pcc` for the full checklist and output format.

## Step 3: Commit
- Stage appropriate files
- Write a descriptive commit message using `[area]` tags:
  - `[util]` - utility module changes
  - `[config]` - configuration changes
  - `[doc]` - documentation updates
  - `[fix]` - bug fixes
  - `[refactor]` - code restructuring
  - `[test]` - test additions/changes
  - `[infra]` - project infrastructure (.claude/, CI, etc.)
- Example: `[util] Add retry logic to slack webhook posting`
- Push to the current branch

## Step 4: Update Task List
- Read `docs/tasks.md` and update based on this session's work:
  - Mark completed tasks with today's date: `- [x] YYYY-MM-DD: Description`
  - Add any new tasks discovered during the session
  - Move blocked tasks if blockers were resolved
  - Flag any tasks that should be promoted (use the `/task promote` escalation ladder)
- Run `/task brief` mentally — does the backbrief make sense?

## Step 4.5: Update Project Status
- **config/project.yaml**: Update `state` section:
  - `last_session.date` - today's date
  - `last_session.file` - path to session doc
  - `last_session.summary` - one-line summary
  - `active_work` - update if changed
  - `known_issues` - add/resolve any discovered
- Include these updates in the commit (amend if needed)

## Step 5: Session Documentation

Create a session doc in `docs/sessions/` with format `YYYYMMDD_descriptive_name.md`.

**Format reference**: [docs/session-doc-format.md](../../docs/session-doc-format.md) — header template, knowledge-graph relationship types, tag taxonomy, body structure, diagram guidelines.

Quick reminders:
- Date-first filename so sessions sort chronologically.
- Knowledge-graph header: only include relationship fields that actually apply.
- Body must include Summary and Next Steps. Other sections (Work Completed, Key Decisions, Pillar Compliance, Commits) are added as the session warrants.
- Prefer Mermaid over ASCII art for any non-trivial diagram (renders natively in GitHub).
- If the session walked the knowledge base (lineage, backlinks, blast radius), record each walk in Work Completed as a `KB-graph: <traversal run> → <what it changed or confirmed>` line. That line is uptake metric M1 in `.claude/skills/traversing-the-knowledge-base/SKILL.md`; a walk with no line cannot be counted. Write it when the walk happens, before the edit it informs, not at session close.

Search related sessions with `grep -r "#domain" docs/sessions/` or `grep -r "References.*config" docs/sessions/`.

## Step 5.5: Upward Lesson Channel (fleet-scope lessons)

While writing the session doc, check each lesson's scope. A lesson is **fleet-scope** if other repos in the doctrine family would repeat the failure or benefit from the fix: convention gaps, tooling failure modes, template defects. Project-specific logic stays repo-scope.

For each fleet-scope lesson, append one line to `.claude/upstream-lesson.md` (create the file if absent; never gitignore it):

```
LESSON (OBSERVED): <one-line claim> | evidence: <repo-relative path or command> | scope: fleet | origin: <this-repo>/docs/sessions/<this-session-doc>.md
```

Rules:

- This file is the upward mirror of `.claude/upstream-update.md`: doctrine flows down, lessons flow up. The upstream template repo (`tacsop`) harvests it on machine visits and clears it after intake.
- Append below existing content, separated by a blank line; never rewrite or delete prior lessons.
- The session doc remains the record of truth; this file is the routing copy. Repo-scope lessons stay in the session doc only.
- In `tacsop` itself there is no upstream. Skip the file and route the lesson to its owner artifact, or to `docs/tasks.md` when no artifact owns it yet.

## Step 6: Evaluate Merge Readiness
- Is this a major functional milestone?
- If yes, consider merging to main
- If no, continue on current branch

Please walk me through each step, showing me the current state before asking what I want to do.
