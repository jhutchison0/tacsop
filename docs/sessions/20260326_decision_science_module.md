# Session: Decision Science Module — Waves 1-3

**Date**: 2026-03-26
**Branch**: main
**Tags**: #session #decision-science #feature #complete

**Documents**: [decision_science_utility.md](../plans/decision_science_utility.md) — CONOP driving this work
**Implements**: [decision_science_utility.md](../plans/decision_science_utility.md) — Waves 1-3 of 4
**References**: [project.yaml](../../config/project.yaml) — Design pillars (Config-Driven, Shift-Left Testing, Simplicity First)
**Follows**: [20260325_gitattributes_and_doctrine_push.md](20260325_gitattributes_and_doctrine_push.md) — Previous session

---

## Summary

Built the decision science utility module from research through implementation. Researched MAUT/MCDA patterns across 9 repos (found 6 with independent implementations), surveyed the Python ecosystem, and deployed a proposer to write a CONOP. Then executed Waves 1-3: core MAUT scorer with config-driven YAML loading, sensitivity analysis (OAT, Monte Carlo, scenario comparison), and visualization helpers (radar, tornado, heatmap). Added a decision-scientist agent and decision-science team template.

Test count grew from 9 to 149 (+140).

## Research Phase

Deployed three research agents in parallel:

1. **Exemplar deep-dive** (tactics-game, quest-engine, project-megan) — all three implement `U = Σ w×u` independently with different value functions and use cases
2. **Portfolio scan** (6 other repos) — found 3 additional repos with MCDA-adjacent patterns: agent-eval (tiered scoring), paperboy (hybrid blend weights), elephant-graveyard (7-signal evidence aggregation)
3. **Ecosystem survey** — no Python library offers lightweight config-driven MAUT with pluggable value functions; existing `weights.py` is ahead of ecosystem on SMARTER weighting

## Changes Made

### New: `src/myproject/decision_science/` (4 files)

| File | Wave | Contents |
|------|------|----------|
| `value_functions.py` | 1 | 7 value functions: linear, exponential, logarithmic, logistic, step, gaussian, piecewise_linear |
| `scorer.py` | 1 | `Criterion`, `DecisionResult`, `MAUTScorer` with `from_yaml()` factory |
| `sensitivity.py` | 2 | `one_at_a_time()`, `monte_carlo()`, `scenario_compare()` |
| `visualization.py` | 3 | `radar_chart()`, `tornado_plot()`, `rank_stability_heatmap()` (matplotlib optional) |

### New: Tests (4 files, 140 tests)

| File | Count | Coverage |
|------|-------|----------|
| `test_value_functions.py` | 48 | All 7 functions: boundaries, edge cases, monotonicity, output range |
| `test_scorer.py` | 29 | Aggregation, weight validation, YAML loading (happy + 6 error paths), ranking |
| `test_sensitivity.py` | 31 | OAT perturbation, Monte Carlo reproducibility, scenario validation, scorer immutability |
| `test_visualization.py` | 32 | Figure creation, axes properties, error guards, matplotlib import mock |

### New: Agent + Team

| File | Purpose |
|------|---------|
| `.claude/agents/decision-scientist.md` | Level 1 domain audit agent — weights, value functions, sensitivity coverage |
| `.claude/teams/decision-science.md` | 5-agent team: proposer + decision-scientist + python-prototyper + test-runner + code-reviewer |

### Modified

| File | Change |
|------|--------|
| `pyproject.toml` | numpy moved to required deps; `[decision-science]` optional group for matplotlib |
| `.claude/README.md` | Agent roster and team template updates |

### New: Planning

| File | Purpose |
|------|---------|
| `docs/plans/decision_science_utility.md` | Full CONOP: 4-wave plan, module architecture, migration path for 6 repos |

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Subpackage `decision_science/`, not flat module | 4 concerns (value functions, scoring, sensitivity, visualization) don't compress into one file |
| `from_yaml()` as Wave 1 gate item | Config-driven is mandatory per user directive — not optional or deferred |
| Validate-and-raise, never auto-correct | Silent normalization hides errors; the config author should see their mistake |
| numpy to required deps | sensitivity.py imports unconditionally; keeping it optional would create confusing ImportErrors |
| `criteria` property on MAUTScorer | Formalizes the public contract instead of sensitivity.py reaching into `_criteria` |
| No external MCDA library dependency | The ecosystem gap is where we add value; wrapping pymcdm/pyDecision adds cost without benefit |

## Code Review Findings (resolved)

- Module-level registry moved inside `from_yaml()` as local lookup
- Unused imports removed
- `rank({})` changed to raise ValueError (was silently returning `[]`)
- Redundant `scorer.criteria` defensive copies cached in local variable
- Return type annotations added where missing (noted for follow-up)

## Next Steps

- Doctrine propagation — notify downstream repos of the new module
- Wave 4 (agent-assisted elicitation) is gated: do not build until 2+ downstream repos request it
- quest-engine is the most likely early adopter (closest architecture match)
- P1 tests for geo.py and logger.py remain top of the active task list
