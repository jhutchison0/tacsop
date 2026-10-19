# Code Review: Decision Science Module -- Waves 2 and 3

**Reviewer**: code-reviewer
**Date**: 2026-03-26
**Scope**: sensitivity.py, visualization.py, tests, pyproject.toml, agent/team definitions
**CONOP**: docs/plans/decision_science_utility.md
**Result**: 58/58 tests pass. 2 issues, 7 notes.

---

## CONOP Compliance Summary

| TCS | Requirement | Status |
|-----|-------------|--------|
| 2.1 | `one_at_a_time()` -- vary each weight by delta, renormalize remaining | PASS |
| 2.2 | `monte_carlo()` -- Dirichlet-sampled weights via numpy, no scipy | PASS |
| 2.3 | `scenario_compare()` -- named weight profiles, validates names and sums | PASS |
| 2.4 | All tests pass, no scipy in required deps | PASS |
| 3.1 | `radar_chart()` -- returns Figure, uses pytest.importorskip | PASS |
| 3.2 | `tornado_plot()` -- returns Figure, readable with 2+ criteria | PASS |
| 3.3 | `rank_stability_heatmap()` -- matplotlib only, no seaborn | PASS |
| 3.4 | Optional dependency declared, guard-import with helpful error | PASS |

---

## Issues (should fix)

### ISSUE-1: `sensitivity.py` imports numpy unconditionally but numpy is not a required dependency

**File**: `src/myproject/decision_science/sensitivity.py:11`
**Also**: `pyproject.toml`

`sensitivity.py` has `import numpy as np` at module level. numpy is only declared in `[project.optional-dependencies].weights`, not in `[project.dependencies]`. This means a user who installs the base package and imports `from myproject.decision_science import one_at_a_time` will get an `ImportError` at import time with no helpful message.

This is the same class of problem that `visualization.py` solved correctly with `_require_matplotlib()`. The difference is that the CONOP states numpy is "already required (via pandas/weights.py)" -- but pyproject.toml says otherwise. Either:

(a) Add `numpy>=1.24` to `[project.dependencies]` (making it truly required), or
(b) Add numpy to the `decision-science` optional group alongside matplotlib, and guard-import it in `sensitivity.py` with a helpful error like visualization does.

Option (a) is the cleaner fix. The CONOP treats numpy as already present, `weights.py` uses it, and `scorer.py` will likely need it in downstream usage patterns. Making it required aligns the declared dependencies with the actual import graph.

**Why it matters**: A clean `pip install -e .` followed by `from myproject.decision_science import monte_carlo` will crash. The error message gives no hint about installing extras.

### ISSUE-2: Unused import `from typing import Any` in sensitivity.py

**File**: `src/myproject/decision_science/sensitivity.py:9`

`Any` is imported but never referenced anywhere in the file. This is a minor hygiene issue but it will flag on any linter pass and suggests a leftover from an earlier draft.

---

## Notes (minor observations)

### NOTE-1: Visualization functions lack return type annotations

**Files**: `visualization.py:36-40`, `visualization.py:89-93`, `visualization.py:172-175`

All three public functions (`radar_chart`, `tornado_plot`, `rank_stability_heatmap`) omit the return type annotation. The docstrings correctly state "Returns: matplotlib.figure.Figure" but the signatures themselves have no `-> Figure` hint. Since matplotlib is optional, annotating the return type requires either `from __future__ import annotations` or a `TYPE_CHECKING` guard:

```python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from matplotlib.figure import Figure
```

The sensitivity functions do have complete type annotations. This is an inconsistency between the two new modules.

### NOTE-2: `_require_matplotlib()` also lacks a return type annotation

**File**: `visualization.py:17`

The helper returns the matplotlib module but has no type hint on the return. Since the return value is unused at every call site (each function re-imports `matplotlib.pyplot as plt` after the guard), this is purely cosmetic.

### NOTE-3: `_rescored()` accesses `scorer._criteria` (private attribute)

**File**: `sensitivity.py:42`

All three sensitivity functions use `scorer._criteria` (the leading underscore marking it private). This is a cross-module access to a private attribute. It works and is pragmatic since both files live in the same package, but it creates coupling. If `MAUTScorer` ever changes its internal representation, `sensitivity.py` breaks silently.

Consider adding a `criteria` property to `MAUTScorer` that returns a read-only view (e.g., `tuple(self._criteria)`). This would formalize the contract without exposing mutability.

### NOTE-4: `one_at_a_time()` does not validate `alternatives` for emptiness

**File**: `sensitivity.py:47-107`

`monte_carlo()` explicitly checks `if not alternatives: raise ValueError(...)` (line 138-139). `one_at_a_time()` and `scenario_compare()` do not. With empty alternatives, they will silently produce empty result lists with no error. This inconsistency could confuse callers. The same guard would be appropriate in all three functions.

### NOTE-5: `__init__.py` unconditionally imports visualization symbols

**File**: `src/myproject/decision_science/__init__.py:18-22`

The `__init__.py` imports `radar_chart`, `rank_stability_heatmap`, and `tornado_plot` at the top level. These imports execute `from src.myproject.decision_science.visualization import ...` which itself only imports `math` and `scorer` (no matplotlib at module level) -- so this is safe. But it is worth noting: if `visualization.py` ever gains a module-level matplotlib import, this `__init__.py` would break for users without matplotlib installed. The current guard-import-inside-functions pattern is correct and must be preserved.

### NOTE-6: Monte Carlo performance with large n_samples

**File**: `sensitivity.py:156-161`

The inner loop calls `_rescored()` per sample, which creates a new `MAUTScorer` and calls `.rank()` each time. For `n_samples=10000` this builds and discards 10,000 scorer objects. This is fine for the intended use case (quick interactive analysis) but worth noting if anyone tries to scale it. A vectorized approach computing all utilities in a single numpy operation would be the optimization path, but that is premature for Wave 2.

### NOTE-7: Test file does not test `one_at_a_time()` with empty alternatives

**File**: `tests/unit/test_sensitivity.py`

Per NOTE-4, there is no test for what happens when `alternatives={}` is passed to `one_at_a_time()` or `scenario_compare()`. The behavior (silently returning results with empty rank lists) is defined by `MAUTScorer.rank()` which raises `ValueError` on empty input -- so the error would surface, but through the scorer, not through a clear sensitivity-layer validation. Adding explicit tests would document the expected behavior.

---

## Agent and Team Definitions

### decision-scientist.md -- PASS

- Scope matches CONOP: read-only analysis, write to `docs/` only, never modifies `src/`
- Audit checklist covers the domain correctly (weight sums, negative weights, value function ranges, missing sensitivity analysis)
- Tools list includes `Bash` which is broader than the CONOP sketch suggested (`Read, Write` only) but is consistent with other agents in the project (proposer has `Read, Write, Edit, Grep, Glob, Bash`). No issue -- Bash is needed for running validation commands.
- Model set to `inherit` per CONOP spec
- Frontmatter includes `memory: project` which is consistent with `proposer.md`

### decision-science.md team -- PASS

- 5 agents as specified in CONOP: proposer, decision-scientist, python-prototyper, test-runner, code-reviewer
- Workflow correctly separates domain review (step 9, decision-scientist) from code review (step 10, code-reviewer)
- Scaling notes correctly require decision-scientist whenever the model changes, even for config-only changes
- Format is consistent with `feature-development.md`

### README.md updates -- PASS

- Agent Catalog: decision-scientist correctly placed in Level 1 (project-specific) section, separate from Level 0 agents
- Scope Matrix: decision-scientist column added with correct access (Read for src, config; Write for docs; dash for tests)
- Team Templates table: decision-science row added with correct agent list
- Directory structure listing updated to include both new files
- All entries are internally consistent

One minor observation: the Scope Matrix shows decision-scientist has no access to `tests/` (dash), while `code-reviewer` has Read access to tests. This is correct per the CONOP (decision-scientist audits models, not test code) and consistent with the agent definition.

---

## Summary

Waves 2 and 3 are solid implementations that closely follow the CONOP. The code is clean, well-documented, and all 58 tests pass. The primary issue is the numpy dependency gap (ISSUE-1), which is a packaging correctness problem rather than a logic bug. The unused import (ISSUE-2) is trivial cleanup. The notes are minor and none block merge.

The agent and team definitions follow project conventions exactly and match the CONOP specification. No issues found.

**Recommendation**: Fix ISSUE-1 (numpy dependency) and ISSUE-2 (unused import), then merge. The notes can be addressed in a follow-up pass or left as-is.
