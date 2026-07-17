# Feature Development Team

**Goal**: Build new utility modules and project components with quality gates at each step.

**When to use**: When adding new utility modules, implementing significant new functionality, or building new project components from scratch. Use this team whenever the feature requires design decisions, tests, and a quality review before merging.

## Composition

| Teammate | Role | Responsibility |
|----------|------|----------------|
| `proposer` | Analyst | Explore the problem space, propose approaches (including bold ones), write proposal to `docs/plans/` |
| `python-prototyper` | Implementer | Implement the approved approach alongside its tests |
| `test-runner` | Validator | Run tests after each implementation step, report coverage gaps |
| `code-reviewer` | Quality gate | Challenge proposals before implementation; review code against design pillars after |

## Workflow

1. Lead assigns the feature with scope and acceptance criteria
2. `proposer` reads the codebase, analyzes the problem, and writes a proposal with multiple approaches to `docs/plans/`
3. `code-reviewer` challenges the proposal — stress-tests assumptions, identifies risks, flags gaps
4. Lead decides which approach to proceed with (or asks `proposer` to revise)
5. `python-prototyper` implements the approved approach with tests in `tests/`
6. `test-runner` runs `pytest` and reports pass/fail counts and any coverage gaps
7. If tests fail, `python-prototyper` fixes and `test-runner` re-validates
8. `code-reviewer` reviews the implementation against the checklist in its agent definition
9. `python-prototyper` addresses any Critical or Warning findings from the review
10. `test-runner` does a final validation pass to confirm all tests are green
11. Lead reviews the summary, commits, and updates `docs/sessions/` per session documentation policy

## Scaling Notes

- For trivial additions (single helper function, minor extension to an existing module), `proposer` and `code-reviewer` may be omitted if the lead is confident in the change.
- For complex features touching multiple modules or introducing new dependencies, this 4-agent composition is the minimum — do not reduce it further.
- The propose-then-challenge cycle (steps 2–4) is the key differentiator — it ensures design decisions are debated before code is written.
- `test-runner` should never be removed — shift-left testing is a core project principle.
