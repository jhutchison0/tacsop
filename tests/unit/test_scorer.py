"""Tests for decision_science.scorer."""

import warnings
from pathlib import Path
from unittest.mock import patch

import pytest

from src.myproject.decision_science.scorer import Criterion, DecisionResult, MAUTScorer, dominance_check
from src.myproject.decision_science.value_functions import linear

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def _make_scorer(*criteria: Criterion) -> MAUTScorer:
    return MAUTScorer(list(criteria))


def _criterion(name: str, weight: float, fn=None) -> Criterion:
    if fn is None:
        fn = linear
    return Criterion(name=name, weight=weight, value_fn=fn)


class TestWeightValidation:
    def test_weights_sum_to_one(self):
        scorer = _make_scorer(
            _criterion("a", 0.6),
            _criterion("b", 0.4),
        )
        scorer.validate_weights()  # no exception

    def test_weights_within_tolerance(self):
        scorer = _make_scorer(
            _criterion("a", 0.605),
            _criterion("b", 0.4),
        )
        scorer.validate_weights()  # 0.005 deviation — within ±0.01

    def test_weights_exceeding_tolerance_raises(self):
        scorer = _make_scorer(
            _criterion("a", 0.7),
            _criterion("b", 0.4),
        )
        with pytest.raises(ValueError, match="sum"):
            scorer.validate_weights()

    def test_weights_too_low_raises(self):
        scorer = _make_scorer(
            _criterion("a", 0.3),
            _criterion("b", 0.3),
        )
        with pytest.raises(ValueError, match="sum"):
            scorer.validate_weights()

    def test_negative_weight_raises(self):
        scorer = _make_scorer(
            _criterion("a", 1.1),
            _criterion("b", -0.1),
        )
        with pytest.raises(ValueError, match="negative"):
            scorer.validate_weights()

    def test_no_criteria_raises(self):
        scorer = MAUTScorer()
        with pytest.raises(ValueError):
            scorer.validate_weights()


class TestScore:
    def test_additive_aggregation(self):
        # u("x") = 0.5 (raw=0.5 with linear 0-1)
        # U = 0.6*0.5 + 0.4*0.5 = 0.5
        scorer = _make_scorer(
            _criterion("x", 0.6),
            _criterion("y", 0.4),
        )
        result = scorer.score("alt1", {"x": 0.5, "y": 0.5})
        assert result.utility == pytest.approx(0.5)

    def test_breakdown_sums_to_utility(self):
        scorer = _make_scorer(
            _criterion("a", 0.7),
            _criterion("b", 0.3),
        )
        result = scorer.score("alt", {"a": 0.8, "b": 0.2})
        assert sum(result.breakdown.values()) == pytest.approx(result.utility)

    def test_breakdown_keys_match_criteria(self):
        scorer = _make_scorer(
            _criterion("cost", 0.5),
            _criterion("benefit", 0.5),
        )
        result = scorer.score("opt", {"cost": 1.0, "benefit": 0.0})
        assert set(result.breakdown.keys()) == {"cost", "benefit"}

    def test_alternative_name_preserved(self):
        scorer = _make_scorer(_criterion("a", 1.0))
        result = scorer.score("TargetAlpha", {"a": 0.5})
        assert result.alternative == "TargetAlpha"

    def test_missing_criterion_raises(self):
        scorer = _make_scorer(
            _criterion("x", 0.5),
            _criterion("y", 0.5),
        )
        with pytest.raises(ValueError, match="missing"):
            scorer.score("alt", {"x": 0.5})

    def test_single_criterion(self):
        scorer = _make_scorer(_criterion("only", 1.0))
        result = scorer.score("solo", {"only": 0.75})
        assert result.utility == pytest.approx(0.75)

    def test_invalid_weights_raises_in_score(self):
        scorer = _make_scorer(
            _criterion("a", 0.3),
            _criterion("b", 0.3),
        )
        with pytest.raises(ValueError):
            scorer.score("alt", {"a": 1.0, "b": 1.0})


class TestRank:
    def test_descending_order(self):
        scorer = _make_scorer(
            _criterion("val", 1.0),
        )
        results = scorer.rank({
            "low": {"val": 0.1},
            "high": {"val": 0.9},
            "mid": {"val": 0.5},
        })
        utilities = [r.utility for r in results]
        assert utilities == sorted(utilities, reverse=True)

    def test_correct_winner(self):
        scorer = _make_scorer(_criterion("val", 1.0))
        results = scorer.rank({
            "A": {"val": 0.9},
            "B": {"val": 0.1},
        })
        assert results[0].alternative == "A"

    def test_returns_all_alternatives(self):
        scorer = _make_scorer(_criterion("v", 1.0))
        alts = {"X": {"v": 0.1}, "Y": {"v": 0.5}, "Z": {"v": 0.9}}
        results = scorer.rank(alts)
        assert {r.alternative for r in results} == {"X", "Y", "Z"}

    def test_equal_utility_stable_sort(self):
        scorer = _make_scorer(_criterion("v", 1.0))
        results = scorer.rank({
            "A": {"v": 0.5},
            "B": {"v": 0.5},
        })
        # Both have utility 0.5; list must still have length 2
        assert len(results) == 2
        assert all(r.utility == pytest.approx(0.5) for r in results)

    def test_empty_alternatives_raises(self):
        scorer = _make_scorer(_criterion("v", 1.0))
        with pytest.raises(ValueError, match="No alternatives"):
            scorer.rank({})

    def test_two_criteria_weighted_correctly(self):
        scorer = _make_scorer(
            _criterion("speed", 0.3),
            _criterion("accuracy", 0.7),
        )
        # A: fast but inaccurate; B: slow but accurate
        results = scorer.rank({
            "A": {"speed": 1.0, "accuracy": 0.0},
            "B": {"speed": 0.0, "accuracy": 1.0},
        })
        # B has higher weighted utility (0.7 vs 0.3)
        assert results[0].alternative == "B"


class TestFromYaml:
    def test_loads_fixture(self):
        scorer = MAUTScorer.from_yaml(FIXTURES_DIR / "decision_model.yaml")
        result = scorer.score(
            "candidate",
            {
                "damage_output": 80.0,
                "threat_proximity": 10.0,
                "survival_probability": 0.8,
            },
        )
        assert 0.0 <= result.utility <= 1.0

    def test_fixture_breakdown_keys(self):
        scorer = MAUTScorer.from_yaml(FIXTURES_DIR / "decision_model.yaml")
        result = scorer.score(
            "c",
            {
                "damage_output": 50.0,
                "threat_proximity": 0.0,
                "survival_probability": 0.5,
            },
        )
        assert set(result.breakdown.keys()) == {
            "damage_output",
            "threat_proximity",
            "survival_probability",
        }

    def test_unknown_value_fn_raises(self, tmp_path):
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text(
            "criteria:\n"
            "  - name: x\n"
            "    weight: 1.0\n"
            "    value_fn: nonexistent_fn\n"
            "    params: {}\n"
        )
        with pytest.raises(ValueError, match="Unknown value_fn"):
            MAUTScorer.from_yaml(bad_yaml)

    def test_missing_required_field_raises(self, tmp_path):
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text(
            "criteria:\n"
            "  - name: x\n"
            "    value_fn: linear\n"
            # weight is missing
        )
        with pytest.raises(ValueError, match="weight"):
            MAUTScorer.from_yaml(bad_yaml)

    def test_bad_weights_raises(self, tmp_path):
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text(
            "criteria:\n"
            "  - name: x\n"
            "    weight: 0.5\n"
            "    value_fn: linear\n"
            "    params: {low: 0, high: 1}\n"
            "  - name: y\n"
            "    weight: 0.3\n"
            "    value_fn: linear\n"
            "    params: {low: 0, high: 1}\n"
        )
        with pytest.raises(ValueError, match="sum"):
            MAUTScorer.from_yaml(bad_yaml)

    def test_missing_criteria_key_raises(self, tmp_path):
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text("something_else:\n  - x\n")
        with pytest.raises(ValueError, match="criteria"):
            MAUTScorer.from_yaml(bad_yaml)

    def test_file_not_found_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            MAUTScorer.from_yaml(tmp_path / "nonexistent.yaml")

    def test_from_yaml_rank(self):
        scorer = MAUTScorer.from_yaml(FIXTURES_DIR / "decision_model.yaml")
        results = scorer.rank({
            "alpha": {"damage_output": 90.0, "threat_proximity": 5.0, "survival_probability": 0.9},
            "beta": {"damage_output": 10.0, "threat_proximity": 200.0, "survival_probability": 0.1},
        })
        # alpha should win: high damage, close threat, high survival
        assert results[0].alternative == "alpha"


class TestAddCriterion:
    def test_add_criterion_incrementally(self):
        scorer = MAUTScorer()
        scorer.add_criterion(_criterion("a", 0.4))
        scorer.add_criterion(_criterion("b", 0.6))
        result = scorer.score("x", {"a": 1.0, "b": 1.0})
        assert result.utility == pytest.approx(1.0)


class TestFromYamlParamValidation:
    """BUG 3: from_yaml should catch typo'd params at load time."""

    def test_typo_in_params_raises_at_load(self, tmp_path):
        bad_yaml = tmp_path / "bad_params.yaml"
        bad_yaml.write_text(
            "criteria:\n"
            "  - name: x\n"
            "    weight: 1.0\n"
            "    value_fn: linear\n"
            "    params: {hgh: 100}\n"  # typo: should be 'high'
        )
        with pytest.raises(ValueError, match="Invalid params"):
            MAUTScorer.from_yaml(bad_yaml)

    def test_valid_params_loads_successfully(self, tmp_path):
        good_yaml = tmp_path / "good_params.yaml"
        good_yaml.write_text(
            "criteria:\n"
            "  - name: x\n"
            "    weight: 1.0\n"
            "    value_fn: linear\n"
            "    params: {low: 0, high: 100}\n"
        )
        scorer = MAUTScorer.from_yaml(good_yaml)
        assert scorer is not None


class TestValueFunctionOutputValidation:
    """ITEM 4: value functions returning outside [0,1] must raise."""

    def test_bad_value_function_raises(self):
        def bad_fn(x: float) -> float:
            return 1.5  # always out of range

        scorer = MAUTScorer([Criterion("a", 1.0, bad_fn)])
        with pytest.raises(ValueError, match="outside \\[0, 1\\]"):
            scorer.score("alt", {"a": 0.5})

    def test_good_value_function_does_not_raise(self):
        scorer = _make_scorer(_criterion("a", 1.0))
        result = scorer.score("alt", {"a": 0.5})
        assert 0.0 <= result.utility <= 1.0


class TestFromWeights:
    """ITEM 5: from_weights classmethod bridges weights.py output to MAUTScorer."""

    def test_builds_scorer_from_weights_df(self):
        pd = pytest.importorskip("pandas")
        import pandas

        weights_df = pandas.DataFrame(
            {"Ranks": [1, 2], "SMARTER": [0.6, 0.4]},
            index=["quality", "speed"],
        )
        weights_df.index.name = "Attributes"

        scorer = MAUTScorer.from_weights(
            weights_df,
            value_fns={"quality": linear, "speed": linear},
            method="SMARTER",
        )
        result = scorer.score("alt", {"quality": 1.0, "speed": 0.0})
        assert result.utility == pytest.approx(0.6)

    def test_missing_method_column_raises(self):
        pd = pytest.importorskip("pandas")
        import pandas

        weights_df = pandas.DataFrame(
            {"Ranks": [1], "SMARTER": [1.0]},
            index=["x"],
        )
        with pytest.raises(ValueError, match="Method column"):
            MAUTScorer.from_weights(weights_df, {"x": linear}, method="NoSuchMethod")

    def test_missing_value_fn_raises(self):
        pd = pytest.importorskip("pandas")
        import pandas

        weights_df = pandas.DataFrame(
            {"Ranks": [1, 2], "SMARTER": [0.6, 0.4]},
            index=["quality", "speed"],
        )
        with pytest.raises(ValueError, match="missing entries"):
            MAUTScorer.from_weights(weights_df, {"quality": linear})  # speed missing

    def test_missing_pandas_raises_with_uv_hint(self):
        import builtins

        real_import = builtins.__import__

        def raiser(name, *args, **kwargs):
            if name == "pandas":
                raise ImportError("No module named 'pandas'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=raiser):
            with pytest.raises(ImportError, match="uv pip install"):
                MAUTScorer.from_weights(object(), {"x": linear})


class TestUtilityRangeWarning:
    """ITEM 6: rank() should warn when a criterion's utility range < 0.2."""

    def test_warns_when_utility_range_is_narrow(self):
        scorer = _make_scorer(
            _criterion("clustered", 0.5),
            _criterion("spread", 0.5),
        )
        # clustered criterion: all alternatives have nearly the same raw score
        alts = {
            "A": {"clustered": 0.51, "spread": 0.0},
            "B": {"clustered": 0.52, "spread": 1.0},
        }
        with pytest.warns(UserWarning, match="clustered"):
            scorer.rank(alts)

    def test_no_warning_when_range_is_wide(self):
        scorer = _make_scorer(
            _criterion("a", 0.5),
            _criterion("b", 0.5),
        )
        alts = {
            "A": {"a": 0.0, "b": 0.0},
            "B": {"a": 1.0, "b": 1.0},
        }
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            scorer.rank(alts)  # should not raise


class TestDecisionResultExplain:
    """ITEM 7: explain() returns structured dict with expected shape."""

    def test_explain_keys(self):
        scorer = _make_scorer(
            _criterion("x", 0.6),
            _criterion("y", 0.4),
        )
        result = scorer.score("opt", {"x": 1.0, "y": 0.5})
        explanation = result.explain()
        assert explanation["alternative"] == "opt"
        assert "utility" in explanation
        assert "criteria" in explanation

    def test_explain_criteria_structure(self):
        scorer = _make_scorer(
            _criterion("x", 0.6),
            _criterion("y", 0.4),
        )
        result = scorer.score("opt", {"x": 1.0, "y": 0.5})
        explanation = result.explain()
        for item in explanation["criteria"]:
            assert "name" in item
            assert "raw_utility" in item
            assert "weighted_contribution" in item
            assert "pct_of_total" in item

    def test_explain_sorted_descending_by_contribution(self):
        scorer = _make_scorer(
            _criterion("x", 0.6),
            _criterion("y", 0.4),
        )
        result = scorer.score("opt", {"x": 1.0, "y": 0.5})
        explanation = result.explain()
        contributions = [c["weighted_contribution"] for c in explanation["criteria"]]
        assert contributions == sorted(contributions, reverse=True)

    def test_explain_pct_sums_to_one(self):
        scorer = _make_scorer(
            _criterion("x", 0.6),
            _criterion("y", 0.4),
        )
        result = scorer.score("opt", {"x": 1.0, "y": 0.5})
        explanation = result.explain()
        total_pct = sum(c["pct_of_total"] for c in explanation["criteria"])
        assert total_pct == pytest.approx(1.0, abs=0.01)

    def test_raw_utilities_populated(self):
        scorer = _make_scorer(_criterion("a", 1.0))
        result = scorer.score("s", {"a": 0.75})
        assert result.raw_utilities["a"] == pytest.approx(0.75)

    def test_decision_result_raw_utilities_defaults_empty(self):
        # Backwards compatibility: raw_utilities defaults to empty dict.
        dr = DecisionResult(alternative="x", utility=0.5, breakdown={"a": 0.5})
        assert dr.raw_utilities == {}


class TestDominanceCheck:
    """ITEM 8: dominance_check() detects dominated alternatives."""

    def _result(self, name: str, raw: dict[str, float]) -> DecisionResult:
        return DecisionResult(
            alternative=name,
            utility=sum(raw.values()),
            breakdown={k: v for k, v in raw.items()},
            raw_utilities=raw,
        )

    def test_detects_strict_dominance(self):
        strong = self._result("strong", {"quality": 0.9, "speed": 0.8})
        weak = self._result("weak", {"quality": 0.3, "speed": 0.2})
        pairs = dominance_check([strong, weak])
        assert ("strong", "weak") in pairs

    def test_no_dominance_when_tradeoff(self):
        fast = self._result("fast", {"quality": 0.2, "speed": 0.9})
        precise = self._result("precise", {"quality": 0.9, "speed": 0.2})
        pairs = dominance_check([fast, precise])
        assert pairs == []

    def test_empty_results(self):
        assert dominance_check([]) == []

    def test_single_result(self):
        r = self._result("only", {"x": 0.5})
        assert dominance_check([r]) == []

    def test_dominated_not_in_dominator_position(self):
        strong = self._result("strong", {"q": 0.9, "s": 0.9})
        weak = self._result("weak", {"q": 0.1, "s": 0.1})
        pairs = dominance_check([strong, weak])
        # weak does not dominate strong
        assert ("weak", "strong") not in pairs
