# Decision Science Module -- Implementation Quality Review

**Date**: 2026-03-26
**Reviewer**: code-reviewer agent
**Scope**: All source and test files across the decision_science subpackage
**Test status**: 148/148 passing (0.80s)

---

## ISSUE-1: `one_at_a_time` crashes on single-criterion scorer

**File**: `src/myproject/decision_science/sensitivity.py:90-96`
**Severity**: Bug -- runtime crash on valid input

When a scorer has exactly one criterion, the `-delta` perturbation reduces its weight (e.g., from 1.0 to 0.9), but there are no remaining criteria to absorb the leftover 0.1. The code enters the `remaining_total == 0.0` branch, computes `n_others = 0`, and the `for name in remaining_original` loop body never executes. The resulting weight dict sums to 0.9, which fails `validate_weights()`.

**Reproduction**:
```python
scorer = MAUTScorer([Criterion('only', 1.0, linear)])
one_at_a_time(scorer, {'A': {'only': 0.8}}, delta=0.1)
# ValueError: Weights must sum to 1.0 (+-0.01); got 0.9000
```

**Fix**: When there is only one criterion (`n_others == 0`), skip the perturbation or force `perturbed = 1.0` since there is nothing to redistribute to:

```python
if remaining_total == 0.0:
    leftover = 1.0 - perturbed
    n_others = len(criteria) - 1
    if n_others == 0:
        # Single criterion: no redistribution possible; keep weight at 1.0
        new_weights[criterion.name] = 1.0
    else:
        for name in remaining_original:
            new_weights[name] = leftover / n_others
```

---

## ISSUE-2: numpy is a hard dependency but only sensitivity.py uses it

**File**: `pyproject.toml:13`, `src/myproject/decision_science/__init__.py:4-8`, `src/myproject/decision_science/sensitivity.py:9`
**Severity**: Dependency hygiene -- violates Pillar 1 (Simplicity First)

`numpy>=1.24` is listed under core `dependencies` in pyproject.toml. The only two consumers are `src/myproject/utils/weights.py` (which also requires pandas) and `sensitivity.py`. Every other module in the project is pure stdlib + pyyaml + python-dotenv.

The problem is compounded by `__init__.py` eagerly importing all three sensitivity functions at module level. This means `from myproject.decision_science import MAUTScorer` -- which needs zero numpy -- triggers `import numpy`, adding ~150ms startup cost and a 30MB+ transitive dependency for users who only want scoring.

**Fix** (two options, pick one):

**Option A** -- Guard-import numpy in sensitivity.py, matching the matplotlib pattern in visualization.py:
```python
def _require_numpy():
    try:
        import numpy as np
        return np
    except ImportError:
        raise ImportError(
            "numpy is required for sensitivity analysis. "
            "Install it with: pip install numpy"
        )
```
Then move numpy out of core dependencies and into `[decision-science]` optional deps alongside matplotlib.

**Option B** -- Lazy-import the sensitivity submodule in `__init__.py` using `__getattr__` so that `import numpy` is deferred until `monte_carlo`, `one_at_a_time`, or `scenario_compare` are actually accessed.

Option A is simpler and matches the existing pattern.

---

## ISSUE-3: `from_yaml` does not validate params against value function signature

**File**: `src/myproject/decision_science/scorer.py:202-203`
**Severity**: Late/confusing error -- bad params produce a `TypeError` at score-time, not at load-time

`functools.partial(builtin_fns[fn_name], **params)` binds params lazily. If the YAML contains a typo (`hgh: 100` instead of `high: 100`), no error is raised until the first call to `scorer.score()`, which produces a generic `TypeError: linear() got an unexpected keyword argument 'hgh'` with no reference to which criterion or YAML line is wrong.

**Fix**: Add an eager validation call right after binding:
```python
bound_fn = functools.partial(builtin_fns[fn_name], **params)
# Validate params eagerly by inspecting the signature
import inspect
sig = inspect.signature(builtin_fns[fn_name])
try:
    # Bind only keyword args to check for unknown params
    sig.bind_partial(**params)
except TypeError as e:
    raise ValueError(
        f"Criterion '{entry['name']}': invalid params for "
        f"value_fn '{fn_name}': {e}"
    ) from None
```

---

## ISSUE-4: Scorer does not validate value function output range

**File**: `src/myproject/decision_science/scorer.py:116`
**Severity**: Silent corruption -- a value function returning >1 or <0 produces wrong utility without warning

At line 116, `u = c.value_fn(raw_scores[c.name])` is used directly without any range check. While the built-in value functions are designed to return [0, 1], a user supplying a custom `value_fn` (the primary use case for `Criterion` accepting any `Callable`) can silently produce utilities >1 or <0, leading to meaningless rankings.

The `logistic` function itself is documented as returning values in the open interval (0, 1), so it never actually violates this, but custom callables have no guard.

**Fix**: Add a post-call assertion:
```python
u = c.value_fn(raw_scores[c.name])
if not (0.0 <= u <= 1.0):
    raise ValueError(
        f"Value function for '{c.name}' returned {u}; "
        f"expected [0, 1]. Input was {raw_scores[c.name]}"
    )
```

Consider making this optional via a `validate=True` parameter on `score()` if performance is a concern (it is called per-criterion per-alternative per-sample in Monte Carlo). Benchmark before deciding -- the check is a single float comparison, likely negligible.

---

## NOTE-1: Extra keys in `raw_scores` are silently ignored

**File**: `src/myproject/decision_science/scorer.py:108-112`
**Severity**: Low -- defensive but may mask user mistakes

`score()` validates that all criterion names appear in `raw_scores`, but does NOT check for extra keys. Passing `{'a': 0.5, 'b': 0.5, 'typo_key': 0.9}` when criteria are `['a', 'b']` silently discards `typo_key`. This could mask data entry errors.

**Suggested fix**: Add a warning or optional strict mode:
```python
extra = set(raw_scores.keys()) - {c.name for c in self._criteria}
if extra:
    import warnings
    warnings.warn(f"raw_scores contains extra keys not in criteria: {sorted(extra)}")
```

---

## NOTE-2: `piecewise_linear` does not validate duplicate x-values in breakpoints

**File**: `src/myproject/decision_science/value_functions.py:167-183`
**Severity**: Low -- silent incorrect behavior on malformed input

Breakpoints with duplicate x-values (e.g., `[(5.0, 0.0), (5.0, 1.0)]`) produce undefined interpolation behavior: which y-value "wins" depends on Python's sort stability. The function does not raise, but the result is meaningless. This was noted in the Wave 1 review and is still present.

**Suggested fix**: After sorting, check for duplicate x-values:
```python
for i in range(len(pts) - 1):
    if pts[i][0] == pts[i + 1][0]:
        raise ValueError(
            f"Duplicate x-value {pts[i][0]} in breakpoints"
        )
```

---

## NOTE-3: No `from_yaml` test coverage for all 7 value function types

**File**: `tests/unit/test_scorer.py`, `tests/fixtures/decision_model.yaml`
**Severity**: Test gap

The YAML fixture uses only `linear`, `gaussian`, and `logistic`. The remaining 4 value function types (`exponential`, `logarithmic`, `step`, `piecewise_linear`) have no `from_yaml` round-trip test. The `piecewise_linear` case is particularly important because its `breakpoints` param serializes as a list-of-lists in YAML, not a dict of scalars like all other functions.

**Suggested fix**: Add a fixture YAML or parametrized test covering all 7 types.

---

## NOTE-4: Visualization functions lack return type annotations

**File**: `src/myproject/decision_science/visualization.py:36,89,172`
**Severity**: Style -- inconsistent with the rest of the module

`radar_chart`, `tornado_plot`, and `rank_stability_heatmap` all return `matplotlib.figure.Figure` but have no return type annotation. Every other public function in the subpackage has full type hints. The return type cannot be annotated at module level since matplotlib is optional, but a `TYPE_CHECKING` guard works:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure

def radar_chart(...) -> Figure:
```

---

## NOTE-5: `monte_carlo` uses `list.index()` for rank lookup -- O(n) per alternative per sample

**File**: `src/myproject/decision_science/sensitivity.py:160`
**Severity**: Low -- acceptable at current scale

`alt_names.index(result.alternative)` is O(n_alternatives) per call, making the inner loop O(n_alts^2) per sample. With the benchmarked scale (20 alternatives, 1000 samples = 50ms), this is fine. At 100+ alternatives it would start to matter. A dict-based lookup would be O(1):

```python
alt_index = {name: i for i, name in enumerate(alt_names)}
# then: alt_index[result.alternative]
```

Not urgent, but worth doing if this grows.

---

## PASS: Areas that look good

- **API surface consistency**: Naming is clean and consistent. All sensitivity functions take `(scorer, alternatives, ...)`. All value functions take `(x, ...)` and return float. Dataclass names are clear.
- **Immutability discipline**: `_rescored()` correctly avoids mutating the input scorer. The `.criteria` property returns a copy. Tests explicitly verify non-mutation.
- **Error messages**: Validation errors are specific and actionable (e.g., "raw_scores is missing criterion values: ['x']", "Scenario 'bad' has wrong criterion names -- missing criteria: ['accuracy']").
- **Visualization guard-import pattern**: matplotlib is cleanly optional with a helpful install message. The test suite properly covers the ImportError path.
- **Test quality**: 148 tests with good coverage of happy paths, error paths, edge cases, and integration. The autouse `close_figures` fixture prevents memory leaks. The e2e test validates domain sense, not just mechanics.
- **Monte Carlo performance**: 1000 samples with 3 criteria and 3 alternatives completes in 29ms. The Dirichlet alpha scaling is well-designed.
- **Weight validation**: Consistent +/-0.01 tolerance across scorer and scenario_compare. Negative weights are caught.

---

## Summary

| Priority | Count | Items |
|----------|-------|-------|
| ISSUE    | 4     | single-criterion OAT crash, numpy hard dep, late YAML param errors, no value_fn output validation |
| NOTE     | 5     | extra raw_scores keys, duplicate breakpoint x-values, YAML test coverage gap, missing viz return types, list.index() in MC |
| PASS     | 7     | API consistency, immutability, error messages, viz guards, test quality, MC perf, weight validation |
