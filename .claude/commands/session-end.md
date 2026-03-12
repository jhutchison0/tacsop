# Session End Workflow

Guide me through ending this development session properly.

## Step 1: Review Changes
- Run `git status` to see all modified and untracked files
- Run `git diff` to review the actual changes
- Identify any files that shouldn't be committed (secrets, temp files, etc.)

## Step 2: Pre-Code Check (PCC)

Run the standardized PCC checklist before committing:

1. **Secrets check** - No API keys, passwords, tokens in staged files
2. **Tests pass** - Run `pytest`
3. **Debug artifacts** - No `print()`, `breakpoint()` left in code
4. **Git state** - Review what's staged vs unstaged

**If PCC fails**: Fix issues before proceeding to commit.

**If PCC passes but changes are significant**: Consider running `/pci` for deeper inspection.

See `@pcc` for the full checklist and output format.

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
  - Mark completed tasks with today's date: `- [x] 2026-03-12: Description`
  - Add any new tasks discovered during the session
  - Move blocked tasks if blockers were resolved

## Step 4.5: Update Project Status
- **config/project.yaml**: Update version, phase status
  - Update `build_phases` status as work progresses
  - Bump version number if appropriate
- Include these updates in the commit (amend if needed)

## Step 5: Session Documentation
- Create a session doc in `docs/sessions/` with format `YYYYMMDD_descriptive_name.md`
- Include:
  - Summary of work completed
  - Key changes made (files, functions)
  - Next steps / outstanding tasks

## Step 6: Evaluate Merge Readiness
- Is this a major functional milestone?
- If yes, consider merging to main
- If no, continue on current branch

Please walk me through each step, showing me the current state before asking what I want to do.
