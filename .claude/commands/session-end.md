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
- **docs/gaps.md**, the gap register (rule 5 of `.claude/skills/maintaining-the-common-operating-picture/SKILL.md`): add a row for each thing the session found that nobody can see yet, naming the collector that would close it and the decision it blocks. When a collector now covers a gap, or a measurement found it absent, set its Status to `closed YYYY-MM-DD by <pointer>`; when a newer row restates it, to `superseded YYYY-MM-DD by <pointer>`; never delete a row. A defect is a task, not a gap. Step 2 ran before this edit, so run the register's test again after it (here, `.venv/bin/pytest tests/unit/test_gaps.py -q`). A repo without the register starts it with its first row (the skill's `ADOPTION.md`, first slice).
- Include these updates in the commit (amend if needed)

## Step 5: Session Documentation

Create a session doc in `docs/sessions/` with format `YYYYMMDD_descriptive_name.md`.

**Format reference**: [docs/session-doc-format.md](../../docs/session-doc-format.md) — header template, knowledge-graph relationship types, tag taxonomy, body structure, diagram guidelines.

Quick reminders:
- Date-first filename so sessions sort chronologically.
- Knowledge-graph header: only include relationship fields that actually apply.
- Body must include Summary, Claims, and Next Steps. Other sections (Work Completed, Key Decisions, Pillar Compliance, Commits) are added as the session warrants.
- Prefer Mermaid over ASCII art for any non-trivial diagram (renders natively in GitHub).
- If a traversal informed the session's work, record it in Work Completed as a `KB-graph: <traversal run> → <what it changed or confirmed>` line, in the sub-topic it informed. That line is uptake metric M1 in `.claude/skills/traversing-the-knowledge-base/SKILL.md`; a walk with no line cannot be counted. The skill says when to write it.

Search related sessions with `grep -r "#domain" docs/sessions/` or `grep -r "References.*config" docs/sessions/`.

### The Claims table

The session doc carries a `## Claims` table: one row for each claim a reader will act on, per the verifying-claims skill (`.claude/skills/verifying-claims/SKILL.md`).

- Each row gives the claim, its state (written, tested, deployed, or observed), and what an `Evidence:` line would carry: the command and its output. A claim that could not be checked reads `UNVERIFIED: <blocker>`.
- Re-run the probe now for every claim about the session's end state (tests pass, pushed, merged), and name the commit each row checked. A claim about an earlier moment keeps its original output and says when it was taken.
- The commit that carries this doc cannot be in its own table. Report that push in your final message, with its own `Evidence:` line.
- Under the table, write `Overclaims the user caught this session: N`. Count each claim made to the user that proved false and that the user corrected, asked about, or had already relied on. Zero is a count; write it.
- Below it, write `Overclaims a reviewer caught this session: M`: every other claim a reviewer's re-run refuted. A claim is in N or in M, never both. A claim you retracted yourself, or that a tool refuted before anyone relied on it, is in neither count; its row shows the correction.
- A session that claimed no outcome writes the two count lines alone.

## Step 6: Evaluate Merge Readiness
- Is this a major functional milestone?
- If yes, consider merging to main
- If no, continue on current branch

Please walk me through each step, showing me the current state before asking what I want to do.
