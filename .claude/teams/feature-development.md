# Feature Development Team

**Goal**: Build new utility modules and project components with quality gates at each step.

**When to use**: When adding new utility modules, implementing significant new functionality, or building new project components from scratch. Use this team whenever the feature requires design decisions, tests, and a quality review before merging.

## Composition

| Teammate | Role | Responsibility |
|----------|------|----------------|
| `python-prototyper` | Implementer | Design and implement the feature alongside its tests |
| `test-runner` | Validator | Run tests after each implementation step, report coverage gaps |
| `code-reviewer` | Quality gate | Review against design pillars, flag security issues, verify conventions |

## Workflow

1. Lead assigns the feature with scope and acceptance criteria
2. `python-prototyper` reads existing patterns in `src/myproject/utils/`, designs the module, and implements it with tests in `tests/`
3. `test-runner` runs `pytest` and reports pass/fail counts and any coverage gaps
4. If tests fail, `python-prototyper` fixes and `test-runner` re-validates
5. `code-reviewer` runs `git diff`, reads changed files, and reviews against the checklist in its agent definition
6. `python-prototyper` addresses any Critical or Warning findings from the review
7. `test-runner` does a final validation pass to confirm all tests are green
8. Lead reviews the summary, commits, and updates `docs/sessions/` per session documentation policy

## Scaling Notes

- For trivial additions (single helper function, minor extension to an existing module), `code-reviewer` may be omitted if the lead is confident in the change.
- For complex features touching multiple modules or introducing new dependencies, this 3-agent composition is the minimum — do not reduce it further.
- If the feature requires significant design decisions before implementation begins, the lead should write a plan in `docs/plans/` before deploying this team.
- `test-runner` should never be removed — shift-left testing is a core project principle.
