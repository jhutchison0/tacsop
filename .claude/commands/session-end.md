# Session End Workflow

Guide me through ending this development session properly.

## Step 1: Review Changes
- Run `git status` to see all modified and untracked files
- Run `git diff` to review the actual changes
- Identify any files that shouldn't be committed (secrets, temp files, etc.)

## Step 2: Pre-Code Check (PCC)

Run the standardized PCC checklist before committing:

1. **Secrets check** - No API keys, passwords, tokens in staged files
2. **Large files check** - No model files (.bin, .pkl, .pt, .pth, .h5, .onnx, .safetensors, .parquet)
3. **Tests pass** - Run `pytest -x -q --tb=line`
4. **Debug artifacts** - No `print()`, `breakpoint()` left in code
5. **Config validation** - `project.yaml` parses correctly
6. **Git state** - Review what's staged vs unstaged

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
- Create a session doc in `docs/sessions/` with format `YYYYMMDD_descriptive_name.md`
- Start with the standard header following the knowledge graph format:
  ```markdown
  # Session: Descriptive Title

  **Date**: YYYY-MM-DD
  **Branch**: dev
  **Tags**: #session #domain #activity

  **Documents**: [project.yaml](../../config/project.yaml) — Config this session touched
  **Implements**: [plan.md](../plans/plan_name.md) — Plan being followed (if any)
  **References**: [some_config.yaml](../../config/some_config.yaml) — Configs consulted
  **Follows**: [prev_session.md](YYYYMMDD_prev.md) — Previous session (if continuing)
  **Completes**: Active work item (from project.yaml)
  **Requires**: [blocker.md](../design/blocker.md) — Unresolved dependency (if any)
  **Cites**: External reference or source document

  ---
  ```

- **Tags** — Use canonical taxonomy:

  | Category | Tags | Use for |
  |----------|------|---------|
  | **Type** | `#session` | Always include for session logs |
  | **Domain** | Project-specific area tags | What area of the project |
  | **Activity** | `#feature` `#bugfix` `#refactor` `#docs` `#setup` | Type of work |
  | **Status** | `#complete` `#in-progress` | Work completion state |

- **Relationships** — Session docs create edges to permanent docs, forming a navigable knowledge graph. Only include the relationship types that apply:

  | Relationship | When to Use |
  |--------------|-------------|
  | `**Documents**:` | Link to system/design docs this session touched (most common) |
  | `**Implements**:` | If following an implementation plan |
  | `**References**:` | Other docs consulted during work (configs, background) |
  | `**Follows**:` | If continuing a previous session |
  | `**Completes**:` | Active work item or milestone this session finishes |
  | `**Requires**:` | Unresolved dependency blocking future work |
  | `**Cites**:` | External reference, source document, or prior art |

- Include in the session body:
  - Summary of work completed
  - Key changes made (files, functions)
  - Any diagrams if helpful (prefer Mermaid for complex diagrams)
  - Next steps / outstanding tasks

**Tip**: Search sessions with `grep -r "#domain" docs/sessions/` or `grep -r "References.*config" docs/sessions/` to find related work.

## Step 6: Evaluate Merge Readiness
- Is this a major functional milestone?
- If yes, consider merging to main
- If no, continue on current branch

Please walk me through each step, showing me the current state before asking what I want to do.
