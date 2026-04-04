# Code Review Team

**Goal**: Audit code quality and test health without modifying production code — purely investigative.

**When to use**: Pre-merge review, periodic quality audits, post-incident review, or evaluating code before a planned refactor. Use this team when you need an objective assessment of what's there before deciding what to change.

## Composition

| Teammate | Role | Responsibility |
|----------|------|----------------|
| `code-reviewer` | Reviewer | Read all target files, review against design pillars and checklist, write a findings report |
| `test-runner` | Validator | Run the full test suite, report coverage gaps and any flaky or failing tests |

## Workflow

1. Lead identifies the scope — a list of files, a module, a recent set of commits, or the full `src/myproject/` tree
2. `code-reviewer` runs `git diff` (if reviewing recent changes) or reads the target files directly, then applies its review checklist
3. `test-runner` runs `pytest` across the full test suite and reports total pass/fail counts, failing test names, and any obvious coverage gaps
4. `code-reviewer` compiles a findings report organized by priority: Critical, Warning, Suggestion
5. Lead triages the findings — decides which to fix now, defer, or accept as-is

## Scaling Notes

- This is the smallest team. Keep it lean — the task is investigative, not implementation-heavy.
- Neither agent writes production code. If the review reveals issues that need fixing, escalate to the appropriate team: `bug-fix` for defects, `feature-development` for missing functionality or structural improvements.
- `code-reviewer` is read-only by design. If it identifies a Critical finding, it reports and stops — it does not attempt to fix.
- For pre-merge reviews on a specific PR, scope `code-reviewer` to the changed files only (`git diff main...HEAD`). For periodic audits, scope it to the full module.
