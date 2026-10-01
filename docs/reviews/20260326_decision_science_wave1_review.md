# Code Review: Decision Science Module -- Wave 1

**Reviewer**: code-reviewer
**Date**: 2026-03-26
**CONOP**: `docs/plans/decision_science_utility.md`
**Verdict**: Conditionally approved -- 2 ISSUE items must be resolved before shipping; the rest are minor.

---

## Summary

The Wave 1 implementation is clean, well-tested, and closely follows the CONOP specification. All 81 tests pass. The value functions are mathematically correct. The MAUTScorer API matches the CONOP interface. The `from_yaml()` extension was included (the CONOP marked it optional for Wave 1) and works well. Test coverage is thorough with both happy paths and error paths exercised.

Two issues require action before merge: an unused import in the test file, and the `_VALUE_FN_REGISTRY` in `scorer.py` which conflicts with the CONOP's explicit "no registries" design constraint. Everything else is PASS or NOTE-level.

---

## 1. CONOP Compliance

### TCS 1.1 -- 7 value functions with correct signatures

**PASS.** All 7 functions implemented in `value_functions.py` with signatures matching the CONOP spec exactly:
- `linear(x, low, high)` -- lines 6-24
- `exponential(x, low, high, rate)` -- lines 27-52
- `logarithmic(x, low, high)` -- lines 55-76
- `logistic(x, midpoint, steepness)` -- lines 79-98
- `step(x, threshold, below, above)` -- lines 101-122
- `gaussian(x, center, sigma)` -- lines 125-143
- `piecewise_linear(x, breakpoints)` -- lines 146-185

All return `float` in `[0, 1]`. All have type hints on all parameters and return values.

### TCS 1.2 -- MAUTScorer with correct interface

**PASS.** `scorer.py` implements:
- `add_criterion()` -- line 67
- `score()` -- line 97
- `rank()` -- line 130
- `validate_weights()` -- line 75
- `from_yaml()` -- line 149 (CONOP optional extension, included)

`rank()` returns `list[DecisionResult]` sorted descending by utility. Weight normalization is validated (not auto-normalized), matching CONOP Open Question #3's recommendation.

### TCS 1.3 -- Clean `__init__.py` re-exports

**PASS.** `__init__.py` re-exports all 7 value functions plus `Criterion`, `DecisionResult`, and `MAUTScorer` via `__all__`. No internal symbols leak.

### TCS 1.4 -- No new required dependencies

**PASS.** `pyproject.toml` shows no new entries in `[project.dependencies]`. The module uses only `math` (stdlib), `yaml` (already a project dependency), `functools`/`dataclasses`/`pathlib`/`typing` (stdlib). numpy is not used.

### from_yaml() -- CONOP extension

**PASS.** Cleanly implemented. YAML schema matches the CONOP's example schema at lines 284-296 exactly. The fixture file `tests/fixtures/decision_model.yaml` mirrors the CONOP example. The factory validates weights on load.

---

## 2. Design Pillar Compliance

### Simplicity First

**ISSUE -- `_VALUE_FN_REGISTRY` in `scorer.py:12-20`.**

The CONOP explicitly states at line 85: "No inheritance hierarchy. No abstract base classes. Two dataclasses and a scorer function. This is the simplest thing that works." And the review criteria says "No abstract base classes, no registries."

`_VALUE_FN_REGISTRY` is a module-level registry dict. While it is simple in implementation (just a dict mapping strings to functions), it is architecturally a registry pattern. It also creates a coupling problem: if a downstream repo defines a custom value function, it cannot be used with `from_yaml()` without modifying this dict.

**Suggested fix**: Replace the registry with a local dict inside `from_yaml()`, or accept an optional `custom_fns` parameter. The simplest approach:

```python
@classmethod
def from_yaml(cls, path: str | Path) -> "MAUTScorer":
    _BUILTIN_FNS = {
        "linear": vf.linear,
        "exponential": vf.exponential,
        "logarithmic": vf.logarithmic,
        "logistic": vf.logistic,
        "step": vf.step,
        "gaussian": vf.gaussian,
        "piecewise_linear": vf.piecewise_linear,
    }
    # ... rest of method uses _BUILTIN_FNS instead of _VALUE_FN_REGISTRY
```

This makes the mapping a local implementation detail of `from_yaml()` rather than a module-level registry. The behavior is identical but the signal is different: no one is tempted to import or modify `_VALUE_FN_REGISTRY`.

**Severity**: ISSUE. The CONOP was specific about this. Moving the dict inside the method is a 1-minute change.

### Config-Driven

**PASS.** `from_yaml()` supports full config-driven decision models. The YAML schema is clean and matches the CONOP example. Parameters are passed through `functools.partial`, which is elegant.

### Validate and Raise

**PASS.** All validation follows the "validate and raise" pattern:
- `validate_weights()` raises on no criteria, negative weights, or weights not summing to 1.0
- `score()` raises on missing criterion values
- `from_yaml()` raises on missing fields, unknown value functions, bad weights, missing file
- Value functions raise on degenerate parameters (low==high, rate==0, sigma==0, etc.)

---

## 3. Code Quality

### Style consistency with `weights.py`

**PASS.** Module docstring at top, concise function docstrings with Args/Returns/Raises sections, type hints on all public signatures, no unnecessary abstractions. The style is consistent with `weights.py`.

### Dataclass design

**PASS.** `Criterion` and `DecisionResult` are plain dataclasses, no inheritance. `DecisionResult.breakdown` uses `field(default_factory=dict)` correctly.

**NOTE -- `Criterion.value_fn` type narrowed from CONOP spec.**

The CONOP specifies `value_fn: Callable[[Any], float]` (line 76). The implementation uses `Callable[[float], float]` (scorer.py line 35). The implementation is more precise and correct -- all 7 value functions take `float` as their first argument. This is an improvement over the CONOP, not a deviation.

### Edge case: `logistic` output range

**NOTE.** The `logistic` function docstring correctly documents it returns values in the open interval `(0, 1)`, not the closed interval `[0, 1]`. This is mathematically correct (the logistic function is asymptotic). However, this means a criterion using `logistic` can never achieve exactly 0.0 or 1.0 utility. This is expected behavior and documented, but downstream consumers should be aware. No action needed.

### Edge case: `exponential` with extreme `rate` values

**NOTE.** With very large `|rate|` values (e.g., `rate=700`), `math.exp(-rate * t)` could overflow. Python's `math.exp` handles this gracefully (returns `inf` or `0.0` without crashing), and the formula still produces values in [0, 1], so this is not a bug. But a test with an extreme rate value would increase confidence. Low priority.

### Edge case: `piecewise_linear` with duplicate x-values in breakpoints

**NOTE.** If two breakpoints have the same x-coordinate but different y-coordinates, the behavior depends on sort stability and which segment matches first. This is an edge case the CONOP does not address. Current behavior is deterministic (first match wins after sort) but undocumented. Consider adding a validation check or documenting the behavior. Low priority.

---

## 4. Test Quality

### Coverage assessment

**PASS.** 81 tests across both files. Coverage is thorough:

| Area | Happy path | Boundary | Error path | Shape/property |
|------|-----------|----------|------------|----------------|
| linear | Y | Y (clamp both ends) | Y (low==high) | Y (inverted, default range) |
| exponential | Y | Y (clamp both ends) | Y (rate=0, low==high) | Y (concave/convex shape) |
| logarithmic | Y | Y (clamp both ends) | Y (low==high) | Y (diminishing returns) |
| logistic | Y | Y | Y (steepness=0) | Y (high steepness step-like) |
| step | Y | Y (at threshold) | Y (invalid below/above) | Y (custom values) |
| gaussian | Y | Y | Y (sigma=0) | Y (symmetry, 1-sigma value) |
| piecewise_linear | Y | Y (clamp, unsorted) | Y (< 2 points, y out of range) | Y (nonlinear shape) |
| validate_weights | Y (exact and within tolerance) | Y (boundary tolerance) | Y (too high, too low, negative, empty) | -- |
| score | Y | Y (single criterion) | Y (missing criterion, invalid weights) | Y (breakdown sums to utility) |
| rank | Y | Y (equal utility) | -- | Y (descending order, two-criteria weighted) |
| from_yaml | Y (load + score, load + rank) | -- | Y (unknown fn, missing field, bad weights, missing key, missing file) | -- |
| add_criterion | Y | -- | -- | -- |

### Unused imports

**ISSUE -- `test_scorer.py:7` imports `DecisionResult` but never uses it.**

```python
from src.myproject.decision_science.scorer import Criterion, DecisionResult, MAUTScorer
```

`DecisionResult` is never referenced in any assertion or type check in the file. Same for `step` on line 8 -- imported but never used in any test.

**Suggested fix**: Remove unused imports.

```python
from src.myproject.decision_science.scorer import Criterion, MAUTScorer
from src.myproject.decision_science.value_functions import linear
```

**Severity**: ISSUE. Unused imports are a lint failure in most CI setups and suggest untested intent (were there planned tests for `DecisionResult` or `step` that were not written?).

### Test gap: empty alternatives dict to `rank()`

**NOTE.** There is no test for `scorer.rank({})` -- an empty alternatives dict. Current behavior would return an empty list (which is reasonable), but the CONOP says "empty inputs raise ValueError" (TCS 1.2). The implementation does not raise on empty alternatives -- `validate_weights()` is called per-alternative in `score()`, so an empty dict silently returns `[]`. Decide whether empty alternatives should raise or return empty, and add a test either way.

### Test gap: `__init__.py` import test

**NOTE.** TCS 1.3 specifies "Import test passes" for the `__init__.py` public API. There is no explicit test that `from src.myproject.decision_science import MAUTScorer, linear, gaussian` works. The tests implicitly exercise the submodule imports, but a direct import test of the `__init__.py` surface would satisfy TCS 1.3 more explicitly.

---

## 5. Cross-Repo Compatibility

### tactics-game MAUTScorer replacement

**PASS.** The `MAUTScorer` API (add_criterion, score, rank, validate_weights, from_yaml) covers the full surface area described in the CONOP's migration section. The YAML schema matches tactics-game's doctrine profile pattern. `functools.partial` for binding value function params is the right approach -- it allows domain-specific parameterization without subclassing.

### quest-engine value function replacement

**PASS.** The 7 value functions are a superset of quest-engine's 4 (`linear`, `threshold_sigmoid` maps to `logistic`, `gaussian`, `binary_sigmoid` maps to `step`). The signature convention `(x, **params)` from the CONOP is satisfied -- all functions take `x` as the first positional argument and domain-specific parameters as keyword arguments.

### project-megan scorer

**PASS.** The `score()` method's `raw_scores: dict[str, float]` input format supports arbitrary criterion names. The `from_yaml()` factory enables config-driven criterion definitions, which is exactly what project-megan's ad-hoc sensor fusion needs to formalize.

---

## 6. Gaps

### Missing from CONOP that should be there

None. All Wave 1 TCS items are satisfied.

### Added that shouldn't be

The `_VALUE_FN_REGISTRY` (addressed above as ISSUE). Everything else is appropriate.

### Value function math correctness

All 7 value functions are mathematically correct:

- **linear**: Standard min-max normalization with clamping. Correct.
- **exponential**: Uses `(1 - e^(-rate*t)) / (1 - e^(-rate))` which correctly maps [0,1] to [0,1] for any nonzero rate. The concave/convex behavior with positive/negative rate is correct.
- **logarithmic**: Uses `ln(1 + 9t) / ln(10)` which maps [0,1] to [0,1] with diminishing returns. The constant c=9 gives a nice curve shape. Correct.
- **logistic**: Standard logistic sigmoid `1/(1 + e^(-k(x-m)))`. Correct.
- **step**: Simple threshold. Correct.
- **gaussian**: Standard Gaussian `e^(-(x-c)^2 / 2s^2)`. Correct.
- **piecewise_linear**: Linear interpolation between sorted breakpoints with endpoint clamping. Correct.

---

## Action Items

| # | Severity | File | Description |
|---|----------|------|-------------|
| 1 | ISSUE | `scorer.py:12-20` | Move `_VALUE_FN_REGISTRY` inside `from_yaml()` as a local variable to avoid module-level registry pattern |
| 2 | ISSUE | `test_scorer.py:7-8` | Remove unused imports `DecisionResult` and `step` |
| 3 | NOTE | `test_scorer.py` | Add test for `rank({})` -- decide if empty alternatives should raise or return `[]` |
| 4 | NOTE | `tests/` | Add explicit `__init__.py` import test per TCS 1.3 |
| 5 | NOTE | `value_functions.py:146` | Consider validating duplicate x-values in `piecewise_linear` breakpoints |
| 6 | NOTE | `test_value_functions.py` | Consider adding an extreme-rate test for `exponential` |

Items 1-2 should be addressed before merge. Items 3-6 can be addressed in a follow-up.
