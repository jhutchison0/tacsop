"""Round-trip tests: YAML spec -> MAUTScorer.from_yaml -> value-function behavior.

Each test builds a one-criterion model (weight 1.0, so weight validation is
inert), loads it through from_yaml, and asserts the loaded criterion's value
function agrees with calling the module function directly with the same params.
Closes the round-trip gap for exponential, logarithmic, step, piecewise_linear.

Equality is exact by construction: yaml.safe_dump writes params as repr(float)
text, which parses back to the identical double, and both sides then execute
the same function object. A mismatch means wrong wiring, not rounding.
"""

import math

import pytest
import yaml
from hypothesis import given, strategies as st

from src.myproject.decision_science import value_functions as vf
from src.myproject.decision_science.scorer import MAUTScorer


@pytest.fixture(scope="module")
def model_dir(tmp_path_factory):
    """Module-scoped dir: property tests rewrite the same file once per example,
    and a function-scoped tmp_path would trip Hypothesis's fixture health check."""
    return tmp_path_factory.mktemp("from_yaml_roundtrip")


def load_value_fn(model_dir, value_fn_name: str, params: dict):
    """Write a one-criterion model to YAML and return the loaded value function."""
    doc = {
        "criteria": [
            {"name": "c", "weight": 1.0, "value_fn": value_fn_name, "params": params}
        ]
    }
    path = model_dir / "model.yaml"
    path.write_text(yaml.safe_dump(doc))
    return MAUTScorer.from_yaml(path).criteria[0].value_fn


# Bounded float strategies exclude nan/inf. The probe range extends past the
# param range so clamping branches (x outside [low, high]) get exercised.
finite = st.floats(min_value=-1e6, max_value=1e6)
unit = st.floats(min_value=0.0, max_value=1.0)
probe = st.floats(min_value=-2e6, max_value=2e6)

distinct_bounds = st.tuples(finite, finite).filter(lambda lh: lh[0] != lh[1])

# |rate| floor: exponential() raises ZeroDivisionError for nonzero |rate| below
# ~2.2e-16 (1 - e^(-rate) rounds to 0.0). That is a value_functions bug, tracked
# separately; this file tests from_yaml wiring, so the strategy stays clear of it.
rates = st.floats(min_value=-1000.0, max_value=1000.0).filter(lambda r: abs(r) >= 1e-6)


class TestConcreteAnchor:
    """One hand-checkable example before the properties (see PROPERTY-BASED.md)."""

    def test_exponential_from_yaml_matches_direct_call(self, model_dir):
        loaded = load_value_fn(
            model_dir, "exponential", {"low": 0.0, "high": 100.0, "rate": 2.0}
        )
        assert loaded(50.0) == vf.exponential(50.0, low=0.0, high=100.0, rate=2.0)
        # At t=0.5, rate=2: (1-e^-1)/(1-e^-2) simplifies to e/(e+1).
        assert loaded(50.0) == pytest.approx(math.e / (math.e + 1.0), rel=1e-12)


class TestRoundTripProperties:
    @given(bounds=distinct_bounds, rate=rates, x=probe)
    def test_exponential_round_trips(self, model_dir, bounds, rate, x):
        low, high = bounds
        params = {"low": low, "high": high, "rate": rate}
        loaded = load_value_fn(model_dir, "exponential", params)
        assert loaded(x) == vf.exponential(x, **params)

    @given(bounds=distinct_bounds, x=probe)
    def test_logarithmic_round_trips(self, model_dir, bounds, x):
        low, high = bounds
        params = {"low": low, "high": high}
        loaded = load_value_fn(model_dir, "logarithmic", params)
        assert loaded(x) == vf.logarithmic(x, **params)

    @given(threshold=finite, below=unit, above=unit, x=probe)
    def test_step_round_trips(self, model_dir, threshold, below, above, x):
        params = {"threshold": threshold, "below": below, "above": above}
        loaded = load_value_fn(model_dir, "step", params)
        assert loaded(x) == vf.step(x, **params)

    # Breakpoints as [x, y] lists so YAML carries the exact structure the
    # direct call receives (safe_dump would silently coerce tuples to lists).
    breakpoint_lists = st.lists(
        st.tuples(finite, unit).map(list), min_size=2, max_size=8
    )

    @given(breakpoints=breakpoint_lists, x=probe)
    def test_piecewise_linear_round_trips(self, model_dir, breakpoints, x):
        loaded = load_value_fn(
            model_dir, "piecewise_linear", {"breakpoints": breakpoints}
        )
        assert loaded(x) == vf.piecewise_linear(x, breakpoints=breakpoints)
