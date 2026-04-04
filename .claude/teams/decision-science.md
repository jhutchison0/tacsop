# Decision Science Team

**Goal**: Design, implement, audit, and validate MAUT/MCDA decision models with domain correctness gates at each step.

**When to use**: Any work involving MAUT/MCDA implementation, decision model design, value function selection, weight assignment, or migration of scoring logic to the shared `decision_science` module. This team is a specialization of `feature-development` — use it whenever a decision model is in scope.

## Composition

| Teammate | Role | Responsibility |
|----------|------|----------------|
| `proposer` | Analyst | Frame the decision problem, propose model structure and value function choices, write proposal to `docs/plans/` |
| `decision-scientist` | Domain reviewer | Audit model structure for MAUT correctness — weights, value functions, sensitivity coverage; write findings to `docs/` |
| `python-prototyper` | Implementer | Implement the approved model alongside its tests |
| `test-runner` | Validator | Run tests after each implementation step, report coverage gaps |
| `code-reviewer` | Quality gate | Review code against design pillars; does not evaluate domain correctness (that is `decision-scientist`'s role) |

## Workflow

1. Lead assigns the task with scope and acceptance criteria
2. `proposer` reads the codebase and decision problem, proposes model structure (criteria, value function choices, weight elicitation method) to `docs/plans/`
3. `decision-scientist` audits the proposal — checks that weights are valid, value functions are appropriate for the domain, and sensitivity analysis is planned
4. `code-reviewer` challenges the proposal — stress-tests assumptions, identifies implementation risks, flags design gaps
5. Lead decides which approach to proceed with (or asks `proposer` to revise)
6. `python-prototyper` implements the approved model with tests in `tests/`
7. `test-runner` runs `pytest` and reports pass/fail counts and any coverage gaps
8. If tests fail, `python-prototyper` fixes and `test-runner` re-validates
9. `decision-scientist` reviews the implementation against the audit checklist — weights, value function outputs, sensitivity analysis presence
10. `code-reviewer` reviews the implementation against the code quality checklist
11. `python-prototyper` addresses any Critical or Warning findings from either review
12. `test-runner` does a final validation pass to confirm all tests are green
13. Lead reviews the summary, commits, and updates `docs/sessions/` per session documentation policy

## Scaling Notes

- For config-only changes (adjusting weights in YAML, swapping a value function), `proposer` may be omitted if the lead is confident in the change — but `decision-scientist` review is always required when the model changes.
- `decision-scientist` and `code-reviewer` run independent review passes (steps 9 and 10) — domain correctness and code quality are separate concerns. Do not merge these passes.
- `test-runner` should never be removed — shift-left testing is a core project principle.
- For downstream repo migrations (replacing a local scorer with `MAUTScorer`), include `decision-scientist` to audit the implicit weights and value functions in the existing code before migration begins.
