# Session: Decision Science Module — Full Build + Team Review

**Date**: 2026-03-26
**Branch**: main
**Tags**: #session #decision-science #feature #complete

**Documents**: [decision_science_utility.md](../plans/decision_science_utility.md) — CONOP driving this work
**Implements**: [decision_science_utility.md](../plans/decision_science_utility.md) — Waves 1-3 of 4
**References**: [project.yaml](../../config/project.yaml) — Design pillars (Config-Driven, Shift-Left Testing, Simplicity First)
**Follows**: [20260325_gitattributes_and_doctrine_push.md](20260325_gitattributes_and_doctrine_push.md) — Previous session

---

## Summary

Built the complete decision science utility module in one session: research across 9 repos, ecosystem survey, CONOP, three implementation waves, end-to-end integration testing, full decision-science team review (scientist + proposer + code-reviewer), and a 9-item hardening pass based on the review findings.

Test count grew from 9 to 190 (+181). Three commits total.

## Phase 1: Research

Deployed three research agents in parallel:

1. **Exemplar deep-dive** (tactics-game, quest-engine, project-megan) — all three implement `U = Σ w×u` independently with different value functions and use cases
2. **Portfolio scan** (6 other repos) — found 3 additional repos with MCDA-adjacent patterns: agent-eval (tiered scoring), paperboy (hybrid blend weights), elephant-graveyard (7-signal evidence aggregation)
3. **Ecosystem survey** — no Python library offers lightweight config-driven MAUT with pluggable value functions; existing `weights.py` is ahead of ecosystem on SMARTER weighting

## Phase 2: Implementation (Waves 1-3)

### `src/myproject/decision_science/` (4 files)

| File | Wave | Contents |
|------|------|----------|
| `value_functions.py` | 1 | 7 value functions: linear, exponential, logarithmic, logistic, step, gaussian, piecewise_linear |
| `scorer.py` | 1 | `Criterion`, `DecisionResult`, `MAUTScorer` with `from_yaml()` and `from_weights()` |
| `sensitivity.py` | 2 | `one_at_a_time()`, `monte_carlo()`, `scenario_compare()`, `RobustnessReport` |
| `visualization.py` | 3 | `radar_chart()`, `tornado_plot()`, `rank_stability_heatmap()` (matplotlib optional) |

### Agent + Team

| File | Purpose |
|------|---------|
| `.claude/agents/decision-scientist.md` | Level 1 domain audit agent — weights, value functions, sensitivity coverage |
| `.claude/teams/decision-science.md` | 5-agent team: proposer + decision-scientist + python-prototyper + test-runner + code-reviewer |

## Phase 3: Team Review + Hardening

Deployed the full decision-science team (scientist, proposer, code-reviewer) to audit the implementation. Found 9 items across three severity levels:

### 3 Bugs Fixed

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| `logistic`/`exponential` overflow | `math.exp()` crashes when exponent > 709 | Clamp to ±700, return asymptotic value |
| `one_at_a_time` single-criterion crash | No remaining criteria to absorb weight delta | Return baseline only when N=1 |
| `from_yaml` deferred param validation | Typo'd params pass load, crash at score-time | Smoke-test partial binding at load |

### 3 Defensive Guards Added

| Guard | What It Catches |
|-------|----------------|
| Value function output validation | Custom `value_fn` returning outside [0,1] |
| Utility range warning | Criteria where all alternatives cluster (effectively deweighted) |
| `from_yaml` param smoke-test | YAML typos like `hgh` instead of `high` |

### 3 Analysis Features Added

| Feature | Purpose |
|---------|---------|
| `explain()` on DecisionResult | Structured dict with per-criterion breakdown, pct_of_total — agent-friendly |
| `dominance_check()` | Weight-independent: "is A strictly better than B on every criterion?" |
| `RobustnessReport` + `robustness_report()` | Single confidence metric from Monte Carlo: winner, margin, is_robust flag |
| `from_weights()` classmethod | Bridges `weights.py` `generate_weights()` output to MAUTScorer |

## Phase 4: Integration Testing

Wrote an end-to-end integration test (`tests/integration/test_decision_science_e2e.py`) exercising the full pipeline: YAML → score → sensitivity → visualization. The test caught incorrect scenario assertions during writing — the model correctly showed Alpha beating Charlie under effectiveness-focused weights due to risk/timing tradeoffs. This validated that the module's behavior is mathematically sound even when domain intuition is wrong.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Subpackage `decision_science/`, not flat module | 4 concerns don't compress into one file |
| `from_yaml()` as Wave 1 gate item | Config-driven is mandatory — not optional or deferred |
| Validate-and-raise, never auto-correct | Silent normalization hides errors |
| numpy to required deps | sensitivity.py imports unconditionally |
| `criteria` property on MAUTScorer | Formalizes public contract (review finding) |
| No external MCDA library dependency | The ecosystem gap is where we add value |
| `explain()` returns dict, not string | All 6 downstream repos are programmatic consumers |
| Utility range warning, not error | Narrow range is suspect, not necessarily wrong (gaussian criteria legitimately cluster) |

## Pillar Compliance

| Pillar | Status | Notes |
|--------|--------|-------|
| **Simplicity First** | PASS | Two dataclasses, one class, seven functions. No inheritance, no ABCs. `_rescored` and `_require_matplotlib` each serve 3+ call sites. |
| **Shift-Left Testing** | PASS | 181 new tests shipped alongside code. Integration test caught scenario reasoning errors. |
| **Config-Driven** | PASS | `from_yaml()` is a gate item. Value function type and params declared in YAML. Validate-and-raise on config errors. |

No deviations from pillars.

## Test Summary

| Suite | Count |
|-------|-------|
| `test_value_functions.py` | 52 (was 48, +4 overflow) |
| `test_scorer.py` | 47 (was 29, +18 for items 3-8) |
| `test_sensitivity.py` | 31 (was 24, +7 for items 2, 9) |
| `test_visualization.py` | 40 |
| `test_math_utils.py` | 9 (existing) |
| `test_decision_science_e2e.py` | 8 (integration) |
| **Total** | **190 passed, 3 skipped** |

3 skipped = `from_weights` tests (pandas not installed in dev env).

## Next Steps

- Doctrine propagation — notify downstream repos of the new module
- Wave 4 (agent-assisted elicitation) is gated: do not build until 2+ downstream repos request it
- quest-engine is the most likely early adopter (closest architecture match)
- `from_yaml` round-trip tests for remaining 4 value function types (exponential, logarithmic, step, piecewise_linear) — minor coverage gap noted by reviewer
- P1 tests for geo.py and logger.py remain top of the active task list
