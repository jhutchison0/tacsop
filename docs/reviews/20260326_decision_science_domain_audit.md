# Decision Science Module -- Domain Audit

**Auditor**: decision-scientist
**Date**: 2026-03-26
**Scope**: Full module (`src/myproject/decision_science/`), fixture YAML, integration tests
**Prior reviews incorporated**: Wave 1 code review (2026-03-26), Waves 2-3 code review (2026-03-26)

---

## Executive Summary

The decision science module is **structurally sound** for its stated purpose: a shared MAUT library for 6+ downstream repos. The MAUT formula implementation is correct, weight validation is enforced at all entry points, and the config-driven design via YAML is well-executed. The sensitivity analysis suite (OAT, Monte Carlo, scenario compare) covers the three most important methods.

There are **no critical findings** -- the module will not produce silently wrong decisions under normal operating conditions. There are **4 warnings** and **7 suggestions**. Two warnings involve numerical stability (overflow in `logistic` and `exponential` under extreme parameters), one involves a missing completeness feature (value function output validation at scoring time), and one is a missing Dirichlet alpha guard. The suggestions address completeness gaps a practitioner would eventually need.

---

## Audit Checklist Results

### Critical (model is wrong) -- ALL PASS

| Check | Result | Evidence |
|-------|--------|----------|
| Weights sum to 1.0 (+-0.01) | PASS | `validate_weights()` enforces this; called in `score()`, `rank()`, `from_yaml()`, all sensitivity functions |
| No negative weights | PASS | `validate_weights()` raises `ValueError` on any weight < 0 |
| Value function output in [0, 1] | PASS (with caveat) | All 7 functions are mathematically constrained to [0, 1] (or open interval for `logistic`). `step` validates its `below`/`above` params. `piecewise_linear` validates all breakpoint y-values. See WARNING-3 for the caveat. |
| Weights in config, not code-only | PASS | `from_yaml()` supports full config-driven models. The `builtin_fns` dict is local to `from_yaml()`, not a module-level registry (the prior review's registry issue was resolved). |

### Warnings (model is suspect)

**WARNING-1: `logistic` overflow with large `|steepness * (x - midpoint)|`**

- **Location**: `value_functions.py:98` -- `math.exp(-steepness * (x - midpoint))`
- **Issue**: When the argument to `math.exp()` exceeds approximately 709.8, Python raises `OverflowError`. This occurs when `steepness` is large and positive and `x` is well below `midpoint` (or `steepness` is large and negative and `x` is above `midpoint`).
- **Verified failing cases**:
  - `logistic(49, midpoint=50, steepness=1000)` -- crashes with `OverflowError: math range error`
  - `logistic(0, midpoint=50, steepness=100)` -- crashes
  - `logistic(100, midpoint=50, steepness=-100)` -- crashes
- **Why it matters**: The logistic function is documented as returning values in `(0, 1)`. A crash is neither `0` nor `1` -- it is an unrecoverable error. A downstream repo using `logistic` for a threshold criterion with moderate steepness and wide input ranges will hit this. The result should be approximately `0.0` (since `1 / (1 + inf) = 0`), not an exception.
- **Suggested fix**: Clamp the exponent argument before calling `math.exp()`:
  ```python
  z = -steepness * (x - midpoint)
  z = max(-700.0, min(700.0, z))
  return 1.0 / (1.0 + math.exp(z))
  ```
  Alternatively, use `try/except OverflowError: return 0.0` since the only overflow direction produces a result of 0.

**WARNING-2: `exponential` overflow with large negative `rate`**

- **Location**: `value_functions.py:52` -- `math.exp(-rate * t)` and `math.exp(-rate)`
- **Issue**: When `rate` is large and negative, `-rate` is large and positive, so `math.exp(-rate)` overflows. Verified: `exponential(0.5, 0, 1, rate=-800)` crashes with `OverflowError`.
- **Why it matters**: Same as WARNING-1. While `rate=-800` is extreme, it is reachable if a downstream repo programmatically fits or sweeps rate parameters. The exponential function should degrade gracefully to its asymptotic value, not crash.
- **Suggested fix**: Clamp the arguments to `math.exp()` at +-700, or catch `OverflowError` and return the appropriate boundary value.

**WARNING-3: No value function output validation at scoring time**

- **Location**: `scorer.py:116` -- `u = c.value_fn(raw_scores[c.name])`
- **Issue**: The scorer calls the value function and trusts the output is in [0, 1]. If a user supplies a custom `value_fn` (via programmatic construction, not YAML) that returns values outside [0, 1], the aggregate utility silently exceeds the valid range. There is no `assert 0.0 <= u <= 1.0` or equivalent check.
- **Why it matters**: The MAUT formula `U = sum(w_i * u_i)` produces a meaningful utility in [0, 1] only if each `u_i` is in [0, 1]. If a custom function returns 2.5, the utility could exceed 1.0, and rankings would still be computed without any error signal. This is the primary vector for silently wrong decisions.
- **Suggested fix**: Add a bounds check after calling the value function:
  ```python
  u = c.value_fn(raw_scores[c.name])
  if not (0.0 <= u <= 1.0):
      raise ValueError(f"Criterion '{c.name}' value_fn returned {u}; must be in [0, 1]")
  ```
  This adds negligible overhead but catches the entire class of custom-function bugs. The built-in functions are already correct, so this is primarily a safety net for downstream programmatic usage.

**WARNING-4: Monte Carlo Dirichlet alpha with zero-weight criteria**

- **Location**: `sensitivity.py:148` -- `alpha = original_weights * n_criteria`
- **Issue**: If a criterion has weight 0.0 (which passes `validate_weights()` since weights are non-negative and can sum to 1.0 with others), the Dirichlet alpha for that criterion becomes 0.0. Dirichlet with alpha=0 is mathematically undefined. NumPy's `rng.dirichlet()` happens to produce 0.0 for that component, but this is implementation-dependent behavior, not a documented guarantee.
- **Why it matters**: A zero-weight criterion is a legitimate modeling choice meaning "this criterion is tracked but does not influence the decision." The Monte Carlo sensitivity analysis should handle this gracefully, either by excluding zero-weight criteria from the Dirichlet or by setting a minimum alpha floor (e.g., `alpha = max(eps, w * n)`).
- **Suggested fix**: Before computing alpha, clamp to a small positive floor: `alpha = np.maximum(original_weights * n_criteria, 1e-6)`.

### Suggestions (consider)

**SUGGESTION-1: `logistic` value function shape for the risk criterion in e2e test**

- **Location**: `tests/integration/test_decision_science_e2e.py:39` -- `logistic` with `steepness=-0.15`
- **Observation**: Using negative steepness to invert the logistic (higher risk = lower utility) works mathematically, but it couples the direction of preference to the value function's steepness sign rather than to the `low`/`high` convention used by `linear`. This is a framing inconsistency: for `linear`, you swap `low` and `high` to invert; for `logistic`, you negate `steepness`. A practitioner unfamiliar with the module must learn two different inversion patterns.
- **No action required now**, but consider documenting the inversion pattern for non-linear functions in the YAML schema. A "direction" parameter (maximize/minimize) at the criterion level would be the cleaner long-term solution.

**SUGGESTION-2: Missing dominance checking**

- **Issue**: The module has no way to detect strict or weak dominance. If alternative A has higher utility than B on every single criterion, A strictly dominates B, and B should be flagged as irrelevant to the decision. This is a standard MCDA analysis step.
- **Why it matters**: In a ranked list of 10 alternatives, knowing which are dominated simplifies the decision-maker's review. It also catches data entry errors (an alternative that is dominated on all criteria is suspicious).
- **Suggested location**: A `check_dominance(results: list[DecisionResult]) -> list[tuple[str, str]]` function in `scorer.py` or a new `analysis.py`.

**SUGGESTION-3: Missing rank reversal detection**

- **Issue**: The sensitivity analysis suite produces OAT and Monte Carlo results, but there is no convenience function to extract "which weight perturbations cause rank reversals?" A user must manually compare `oat_result["criterion+delta"]` rankings to the baseline to find flips.
- **Why it matters**: Rank reversal is the primary output of sensitivity analysis in practice. The data is there but the interpretation step is missing.
- **Suggested addition**: A helper like `rank_reversals(oat_result) -> dict[str, bool]` that returns which perturbations changed the winner.

**SUGGESTION-4: Missing decision confidence metric**

- **Issue**: The Monte Carlo frequency matrix tells you how often each alternative is rank-1, but there is no scalar "confidence" metric. A decision where the winner is rank-1 in 95% of samples is far more robust than one at 35%.
- **Suggested addition**: A function that returns `{alternative: rank_1_frequency}` as a simple confidence proxy, or a "margin of victory" metric showing the utility gap between rank-1 and rank-2 alternatives.

**SUGGESTION-5: Weight elicitation integration gap**

- **Issue**: The `weights.py` module in `src/myproject/utils/` generates SMARTER, rank-reciprocal, and rank-sum weights. The `decision_science` module accepts weights but has no direct integration with `weights.py`. A user must manually extract weights from the DataFrame and assign them to criteria.
- **Why it matters**: This is the obvious workflow: rank your criteria, generate SMARTER weights, build a scorer. The two modules should have a documented integration path or a helper.
- **Suggested addition**: Either a `MAUTScorer.from_ranked_criteria()` factory or a documented recipe in a docstring.

**SUGGESTION-6: `piecewise_linear` duplicate x-coordinate behavior is undocumented**

- **Location**: `value_functions.py:167` -- `pts = sorted(breakpoints, key=lambda p: p[0])`
- **Issue**: If two breakpoints have the same x-value but different y-values, the sort is stable by insertion order, and the interpolation returns the first segment's value. This is deterministic but undocumented. A user providing `[(0, 0.0), (50, 0.3), (50, 0.8), (100, 1.0)]` (a jump at x=50) gets the lower value at x=50, which may not be the intent.
- **Suggested fix**: Either validate that x-values are unique, or document the behavior.

**SUGGESTION-7: `from_yaml()` does not support custom value functions**

- **Location**: `scorer.py:177-185` -- `builtin_fns` dict inside `from_yaml()`
- **Issue**: A downstream repo with a domain-specific value function (e.g., a proprietary damage curve for tactics-game) cannot use it in a YAML model without modifying the utils library. The programmatic path works (pass any callable as `value_fn`), but the config-driven path is limited to the 7 built-ins.
- **Suggested fix**: Add an optional `custom_fns: dict[str, Callable]` parameter to `from_yaml()`. This was noted in the Wave 1 review but not yet implemented. Priority: low until a downstream repo actually needs it.

---

## Cognitive Bias Vulnerability Assessment

### Anchoring

**LOW RISK.** The additive MAUT formula `U = sum(w_i * u_i)` is commutative -- the order of criteria in the YAML file or the order of alternatives in the input dict does not affect the computed utility. The ranking is deterministic given the same weights and scores. The only anchoring risk is psychological, not computational: the first criterion listed in a YAML file may receive more attention during weight elicitation. This is outside the module's scope.

### Status Quo Bias

**NOT PRESENT.** There is no default weighting that privileges inaction. Weights must be explicitly set by the user; there are no built-in defaults. The `validate_weights()` check refuses to score without a valid weight vector. This is the correct design choice.

### Availability Bias

**LOW RISK.** The module does not weight criteria by visibility, frequency, or any heuristic. All weights are explicitly user-supplied. However, the module also does nothing to *counter* availability bias -- a user who overweights a vivid criterion (e.g., "risk" after a recent failure) will get a model that reflects that bias. This is expected: MAUT is a preference-encoding tool, not a debiasing tool. Sensitivity analysis is the correct mitigation, and it is available.

### Framing Effects

**MODERATE RISK.** This is the most substantive bias concern.

The module supports two mechanisms for "minimize" criteria:
1. **`linear` with inverted `low`/`high`**: `linear(x, low=100, high=0)` -- higher raw value = lower utility. Clear and explicit.
2. **`logistic` with negative `steepness`**: `logistic(x, midpoint=50, steepness=-0.15)` -- inverts the S-curve. Less obvious to read.

These two mechanisms are semantically identical (both produce "higher input = lower utility") but syntactically different. A practitioner reviewing a YAML model must understand both patterns. More importantly, there is no criterion-level "direction" field (maximize/minimize) that would make the framing explicit.

This means the same decision criterion -- "minimize cost" -- can be configured in multiple ways that all produce correct but differently shaped utility curves. A reviewer cannot tell from the YAML alone whether a criterion is being maximized or minimized without understanding the value function parameters.

**Mitigation**: This is an inherent property of flexible value functions and is not a bug. But adding an optional `direction: minimize` field to the YAML schema (that flips the value function output: `u = 1.0 - fn(x)`) would make framing explicit and auditable.

---

## Mathematical Correctness Assessment

### Division by Zero

| Function | Protected? | Notes |
|----------|-----------|-------|
| `linear` | Yes | Raises `ValueError` if `low == high` |
| `exponential` | Yes | Raises `ValueError` if `low == high` or `rate == 0` |
| `logarithmic` | Yes | Raises `ValueError` if `low == high` |
| `logistic` | Yes | Raises `ValueError` if `steepness == 0` |
| `gaussian` | Yes | Raises `ValueError` if `sigma == 0` |
| `piecewise_linear` | Partial | If two adjacent breakpoints have the same x-value, `(x - x0) / (x1 - x0)` divides by zero. The sort and `x0 <= x <= x1` guard makes this unlikely but not impossible with duplicate x-values. |
| `one_at_a_time` | Yes | `remaining_total == 0` case is explicitly handled |

### Numerical Stability

| Scenario | Status | Notes |
|----------|--------|-------|
| `logistic` with large `|steepness * (x - midpoint)|` | **FAILS** | `math.exp()` overflow. See WARNING-1. |
| `exponential` with large `|rate|` | **FAILS** | `math.exp()` overflow. See WARNING-2. |
| Extreme weight ratios (0.001 vs 0.997) | PASS | Floating point handles this range without issue; sum stays within tolerance |
| Floating point accumulation in `sum(breakdown.values())` | PASS | Python's `sum()` uses pairwise summation for floats, which is stable for typical criterion counts (< 100). Tested with 100 criteria of weight 0.01: sum = 1.0 exactly. |
| Value functions at domain boundaries | PASS | `linear`, `exponential`, `logarithmic` all clamp `t` to [0, 1] before applying the formula. `gaussian` returns 0.0 at extreme distances. `step` is a simple comparison. |

### Additive Formula Correctness

The core formula `U(a) = sum(w_i * u_i(x_i))` is implemented in `scorer.py:114-117` as:
```python
for c in self._criteria:
    u = c.value_fn(raw_scores[c.name])
    breakdown[c.name] = c.weight * u
utility = sum(breakdown.values())
```

This is mathematically correct. The breakdown stores `w_i * u_i` per criterion, and the aggregate is their sum. The breakdown sums to utility by construction. The e2e test verifies this property (`sum(r.breakdown.values()) == pytest.approx(r.utility)`).

---

## Completeness Gap Analysis

| Feature | Present? | Priority for practitioners |
|---------|----------|---------------------------|
| Additive MAUT scoring | Yes | Core |
| Weight validation | Yes | Core |
| Config-driven models (YAML) | Yes | Core |
| OAT sensitivity analysis | Yes | High |
| Monte Carlo sensitivity (Dirichlet) | Yes | High |
| Scenario comparison | Yes | High |
| Radar chart | Yes | Medium |
| Tornado diagram | Yes | Medium |
| Rank stability heatmap | Yes | Medium |
| Dominance checking | **No** | Medium |
| Rank reversal detection helper | **No** | Medium |
| Decision confidence metric | **No** | Medium |
| Weight elicitation integration | **No** | Low (weights.py exists separately) |
| Custom value function in YAML | **No** | Low until needed |
| Direction (maximize/minimize) field | **No** | Low (workarounds exist) |
| Multi-linear (interaction) models | **No** | Low (additive is the design choice) |
| AHP/pairwise comparison | **No** | Low (out of scope per CONOP) |

---

## Downstream Repo Compatibility Assessment

### tactics-game: DoctrineProfile mapping

**COMPATIBLE.** The `MAUTScorer` API maps directly to tactics-game's unit action selection pattern. The YAML schema supports the same structure as a doctrine profile. `functools.partial` allows binding game-specific parameters (damage curves, range tables) without subclassing. The one gap is custom value functions in YAML (SUGGESTION-7) -- if tactics-game defines a proprietary damage falloff curve, it must use programmatic construction rather than YAML to reference it.

### quest-engine: Pluggable value functions

**COMPATIBLE.** Quest-engine's 4 value functions (`linear`, `threshold_sigmoid`, `gaussian`, `binary_sigmoid`) map to the module's `linear`, `logistic`, `gaussian`, `step` respectively. The signature convention `(x, **params)` is satisfied. Quest-engine's `evaluation.yaml` format should translate cleanly to the module's YAML schema. The `validate_weights()` call at scoring time will catch quest-engine's known gap (weight redistribution when attributes are missing).

### project-megan: Sensor fusion

**COMPATIBLE WITH WORK.** Project-megan's ad-hoc sensor fusion (smile detection, giggle detection, distance, novelty) is functionally MAUT but uses implicit weights. Migration requires: (1) identifying the implicit weights in the existing code, (2) defining them explicitly in a decision model YAML, (3) selecting appropriate value functions for each sensor. The module API supports this, but the migration is a modeling exercise, not just a code swap.

---

## Prior Review Issue Tracking

The following issues from the Wave 1 and Waves 2-3 code reviews have been verified resolved:

| Issue | Status |
|-------|--------|
| `_VALUE_FN_REGISTRY` moved inside `from_yaml()` | Resolved -- now `builtin_fns` local dict |
| Unused import `DecisionResult` in `test_scorer.py` | Resolved -- import removed |
| numpy not in required dependencies | Resolved -- `numpy>=1.24` in `[project.dependencies]` |
| Unused `from typing import Any` in `sensitivity.py` | Resolved -- import removed |
| `_rescored()` accesses `scorer._criteria` | Resolved -- uses `scorer.criteria` property |
| `rank({})` behavior | Resolved -- raises `ValueError("No alternatives to rank")` |

---

## Summary of Findings

| Severity | Count | Items |
|----------|-------|-------|
| Critical | 0 | -- |
| Warning | 4 | W1: logistic overflow, W2: exponential overflow, W3: no output validation at scoring, W4: Dirichlet alpha=0 |
| Suggestion | 7 | S1: inversion pattern docs, S2: dominance checking, S3: rank reversal helper, S4: confidence metric, S5: weights.py integration, S6: piecewise_linear duplicate x, S7: custom fns in YAML |

**Verdict**: The module is **fit for use** in downstream repos under normal operating conditions. The two overflow warnings (W1, W2) should be fixed before any downstream repo uses `logistic` or `exponential` with programmatically-generated parameters, as parameter sweeps or optimization loops could easily hit the overflow boundary. The output validation warning (W3) should be fixed before any downstream repo uses custom value functions programmatically. W4 is an edge case that matters only if a zero-weight criterion is used with Monte Carlo sensitivity analysis.
