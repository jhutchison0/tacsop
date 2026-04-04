# Bug Fix Team

**Goal**: Fix bugs with regression prevention — diagnose root cause, write a failing test, then fix the code.

**When to use**: When fixing reported bugs, correcting logic errors, or addressing issues found during audits. The regression-first approach ensures the bug cannot silently reappear.

## Composition

| Teammate | Role | Responsibility |
|----------|------|----------------|
| `python-prototyper` | Implementer | Diagnose the bug, write a regression test that fails, then fix the code |
| `test-runner` | Validator | Verify the regression test fails before the fix, confirm all tests are green after |

## Workflow

1. Lead describes the bug — include observed behavior, expected behavior, and any reproduction steps
2. `python-prototyper` reads the relevant source files to understand the logic and identify root cause
3. `python-prototyper` writes a regression test in `tests/` that captures the failure (test should fail at this point)
4. `test-runner` runs the new test to confirm it fails — this validates the test is correctly scoped
5. `python-prototyper` implements the fix in `src/myproject/`
6. `test-runner` runs the full test suite to confirm the regression test now passes and no existing tests regressed
7. Lead reviews the diff, commits with a descriptive message referencing the bug

## Scaling Notes

- Add `code-reviewer` if the fix touches more than 3 files, changes public API signatures, or involves security-sensitive code (e.g., input validation, file I/O, external calls).
- For data-only or config-only fixes (no logic change), the lead may handle alone without deploying this team.
- `test-runner` must confirm the regression test fails *before* the fix is applied — skipping this step defeats the purpose of regression testing.
