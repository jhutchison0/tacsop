"""Tests for decision_science.sensitivity."""

import pytest

from src.myproject.decision_science.scorer import Criterion, MAUTScorer
from src.myproject.decision_science.sensitivity import (
    monte_carlo,
    one_at_a_time,
    scenario_compare,
)
from src.myproject.decision_science.value_functions import linear


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _criterion(name: str, weight: float) -> Criterion:
    return Criterion(name=name, weight=weight, value_fn=linear)


def _make_scorer(*criteria: Criterion) -> MAUTScorer:
    return MAUTScorer(list(criteria))


def _two_criterion_scorer() -> MAUTScorer:
    """Scorer with 'speed' (0.5) and 'accuracy' (0.5)."""
    return _make_scorer(
        _criterion("speed", 0.5),
        _criterion("accuracy", 0.5),
    )


def _three_criterion_scorer() -> MAUTScorer:
    """Scorer with cost (0.3), benefit (0.5), risk (0.2)."""
    return _make_scorer(
        _criterion("cost", 0.3),
        _criterion("benefit", 0.5),
        _criterion("risk", 0.2),
    )


# Two alternatives where speed-weight changes can flip the winner.
_SPEED_ACCURACY_ALTS = {
    "fast": {"speed": 1.0, "accuracy": 0.0},
    "precise": {"speed": 0.0, "accuracy": 1.0},
}

_THREE_ALTS = {
    "A": {"cost": 0.9, "benefit": 0.8, "risk": 0.2},
    "B": {"cost": 0.5, "benefit": 0.5, "risk": 0.5},
    "C": {"cost": 0.1, "benefit": 0.3, "risk": 0.9},
}


# ---------------------------------------------------------------------------
# one_at_a_time
# ---------------------------------------------------------------------------

class TestOneAtATime:
    def test_baseline_key_present(self):
        scorer = _two_criterion_scorer()
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS)
        assert "baseline" in result

    def test_baseline_matches_unperturbed_ranking(self):
        scorer = _two_criterion_scorer()
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS)
        baseline_order = [r.alternative for r in result["baseline"]]
        direct_order = [r.alternative for r in scorer.rank(_SPEED_ACCURACY_ALTS)]
        assert baseline_order == direct_order

    def test_correct_number_of_keys(self):
        scorer = _three_criterion_scorer()
        result = one_at_a_time(scorer, _THREE_ALTS)
        # 1 baseline + 2 perturbations × 3 criteria = 7
        assert len(result) == 7

    def test_perturbation_key_names(self):
        scorer = _two_criterion_scorer()
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS)
        expected_keys = {
            "baseline",
            "speed+delta",
            "speed-delta",
            "accuracy+delta",
            "accuracy-delta",
        }
        assert set(result.keys()) == expected_keys

    def test_rank_flip_detected(self):
        """Boosting speed weight should make 'fast' win; cutting should make 'precise' win."""
        scorer = _two_criterion_scorer()  # 50/50 — tied
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS, delta=0.3)

        speed_up_winner = result["speed+delta"][0].alternative
        speed_down_winner = result["speed-delta"][0].alternative
        # When speed weight is 0.8 'fast' should win; when 0.2 'precise' should win.
        assert speed_up_winner == "fast"
        assert speed_down_winner == "precise"

    def test_zero_delta_matches_baseline(self):
        scorer = _two_criterion_scorer()
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS, delta=0.0)
        for key, ranked in result.items():
            # With delta=0 every perturbation key is the same as baseline
            assert [r.alternative for r in ranked] == [
                r.alternative for r in result["baseline"]
            ]

    def test_large_delta_does_not_crash(self):
        """delta=0.5 on a weight=0.5 should clamp and renormalize without error."""
        scorer = _two_criterion_scorer()
        result = one_at_a_time(scorer, _SPEED_ACCURACY_ALTS, delta=0.5)
        # speed-delta: 0.5 - 0.5 = 0 → speed weight 0, accuracy weight 1
        assert result["speed-delta"][0].alternative == "precise"
        # speed+delta: min(1.0, 0.5 + 0.5) = 1.0 → accuracy weight 0
        assert result["speed+delta"][0].alternative == "fast"

    def test_all_results_have_all_alternatives(self):
        scorer = _three_criterion_scorer()
        result = one_at_a_time(scorer, _THREE_ALTS)
        for key, ranked in result.items():
            assert {r.alternative for r in ranked} == set(_THREE_ALTS.keys()), key

    def test_original_scorer_not_mutated(self):
        scorer = _two_criterion_scorer()
        original_weights = {c.name: c.weight for c in scorer._criteria}
        one_at_a_time(scorer, _SPEED_ACCURACY_ALTS)
        final_weights = {c.name: c.weight for c in scorer._criteria}
        assert original_weights == final_weights

    def test_each_result_is_sorted_descending(self):
        scorer = _three_criterion_scorer()
        result = one_at_a_time(scorer, _THREE_ALTS)
        for key, ranked in result.items():
            utilities = [r.utility for r in ranked]
            assert utilities == sorted(utilities, reverse=True), key


# ---------------------------------------------------------------------------
# monte_carlo
# ---------------------------------------------------------------------------

class TestMonteCarlo:
    def test_reproducibility_same_seed(self):
        scorer = _three_criterion_scorer()
        r1 = monte_carlo(scorer, _THREE_ALTS, n_samples=200, seed=42)
        r2 = monte_carlo(scorer, _THREE_ALTS, n_samples=200, seed=42)
        assert r1 == r2

    def test_different_seeds_may_differ(self):
        scorer = _three_criterion_scorer()
        r1 = monte_carlo(scorer, _THREE_ALTS, n_samples=500, seed=1)
        r2 = monte_carlo(scorer, _THREE_ALTS, n_samples=500, seed=2)
        # Not guaranteed to differ but overwhelmingly likely with 500 samples.
        assert r1 != r2

    def test_all_alternatives_present(self):
        scorer = _three_criterion_scorer()
        result = monte_carlo(scorer, _THREE_ALTS, n_samples=50, seed=0)
        assert set(result.keys()) == set(_THREE_ALTS.keys())

    def test_frequencies_sum_to_one_per_alternative(self):
        scorer = _three_criterion_scorer()
        result = monte_carlo(scorer, _THREE_ALTS, n_samples=200, seed=7)
        for alt_name, rank_freqs in result.items():
            total = sum(rank_freqs.values())
            assert total == pytest.approx(1.0, abs=1e-9), alt_name

    def test_all_rank_positions_present(self):
        scorer = _three_criterion_scorer()
        result = monte_carlo(scorer, _THREE_ALTS, n_samples=100, seed=3)
        n_alts = len(_THREE_ALTS)
        expected_ranks = {str(i + 1) for i in range(n_alts)}
        for alt_name, rank_freqs in result.items():
            assert set(rank_freqs.keys()) == expected_ranks, alt_name

    def test_dominant_alternative_wins_most_often(self):
        """When one alternative is uniformly better, it should top-rank most samples."""
        scorer = _make_scorer(
            _criterion("quality", 0.6),
            _criterion("speed", 0.4),
        )
        alts = {
            "dominant": {"quality": 1.0, "speed": 1.0},
            "weak": {"quality": 0.0, "speed": 0.0},
        }
        result = monte_carlo(scorer, alts, n_samples=200, seed=99)
        assert result["dominant"]["1"] > 0.9

    def test_n_samples_one_does_not_crash(self):
        scorer = _two_criterion_scorer()
        result = monte_carlo(scorer, _SPEED_ACCURACY_ALTS, n_samples=1, seed=0)
        assert len(result) == len(_SPEED_ACCURACY_ALTS)

    def test_frequency_values_in_range(self):
        scorer = _three_criterion_scorer()
        result = monte_carlo(scorer, _THREE_ALTS, n_samples=100, seed=5)
        for alt_name, rank_freqs in result.items():
            for rank_str, freq in rank_freqs.items():
                assert 0.0 <= freq <= 1.0, f"{alt_name} rank {rank_str}: {freq}"

    def test_two_alternatives_rank_frequencies_complement(self):
        """With two alternatives each rank-1 frequency + other's rank-1 freq = 1."""
        scorer = _two_criterion_scorer()
        result = monte_carlo(scorer, _SPEED_ACCURACY_ALTS, n_samples=300, seed=11)
        freq_fast_rank1 = result["fast"]["1"]
        freq_precise_rank1 = result["precise"]["1"]
        assert freq_fast_rank1 + freq_precise_rank1 == pytest.approx(1.0, abs=1e-9)

    def test_original_scorer_not_mutated(self):
        scorer = _three_criterion_scorer()
        original_weights = {c.name: c.weight for c in scorer._criteria}
        monte_carlo(scorer, _THREE_ALTS, n_samples=50, seed=0)
        final_weights = {c.name: c.weight for c in scorer._criteria}
        assert original_weights == final_weights


# ---------------------------------------------------------------------------
# scenario_compare
# ---------------------------------------------------------------------------

class TestScenarioCompare:
    def _scenarios(self) -> dict[str, dict[str, float]]:
        return {
            "speed_focused": {"speed": 0.8, "accuracy": 0.2},
            "accuracy_focused": {"speed": 0.2, "accuracy": 0.8},
            "balanced": {"speed": 0.5, "accuracy": 0.5},
        }

    def test_correct_scenario_names_in_output(self):
        scorer = _two_criterion_scorer()
        result = scenario_compare(scorer, _SPEED_ACCURACY_ALTS, self._scenarios())
        assert set(result.keys()) == {"speed_focused", "accuracy_focused", "balanced"}

    def test_each_scenario_returns_all_alternatives(self):
        scorer = _two_criterion_scorer()
        result = scenario_compare(scorer, _SPEED_ACCURACY_ALTS, self._scenarios())
        for name, ranked in result.items():
            assert {r.alternative for r in ranked} == set(_SPEED_ACCURACY_ALTS.keys()), name

    def test_different_weights_produce_different_winner(self):
        scorer = _two_criterion_scorer()
        result = scenario_compare(scorer, _SPEED_ACCURACY_ALTS, self._scenarios())
        assert result["speed_focused"][0].alternative == "fast"
        assert result["accuracy_focused"][0].alternative == "precise"

    def test_each_result_sorted_descending(self):
        scorer = _three_criterion_scorer()
        scenarios = {
            "cost_heavy": {"cost": 0.7, "benefit": 0.2, "risk": 0.1},
            "benefit_heavy": {"cost": 0.1, "benefit": 0.8, "risk": 0.1},
        }
        result = scenario_compare(scorer, _THREE_ALTS, scenarios)
        for name, ranked in result.items():
            utilities = [r.utility for r in ranked]
            assert utilities == sorted(utilities, reverse=True), name

    def test_wrong_criterion_names_raises(self):
        scorer = _two_criterion_scorer()
        bad_scenarios = {
            "bad": {"speed": 0.5, "nonexistent": 0.5},
        }
        with pytest.raises(ValueError, match="wrong criterion names"):
            scenario_compare(scorer, _SPEED_ACCURACY_ALTS, bad_scenarios)

    def test_missing_criterion_in_scenario_raises(self):
        scorer = _two_criterion_scorer()
        bad_scenarios = {
            "incomplete": {"speed": 1.0},  # missing accuracy
        }
        with pytest.raises(ValueError, match="missing criteria"):
            scenario_compare(scorer, _SPEED_ACCURACY_ALTS, bad_scenarios)

    def test_extra_criterion_in_scenario_raises(self):
        scorer = _two_criterion_scorer()
        bad_scenarios = {
            "too_many": {"speed": 0.4, "accuracy": 0.4, "extra": 0.2},
        }
        with pytest.raises(ValueError, match="unknown criteria"):
            scenario_compare(scorer, _SPEED_ACCURACY_ALTS, bad_scenarios)

    def test_weights_not_summing_to_one_raises(self):
        scorer = _two_criterion_scorer()
        bad_scenarios = {
            "bad_sum": {"speed": 0.6, "accuracy": 0.6},
        }
        with pytest.raises(ValueError, match="sum"):
            scenario_compare(scorer, _SPEED_ACCURACY_ALTS, bad_scenarios)

    def test_weights_within_tolerance_accepted(self):
        """Weights summing to 0.995 (within ±0.01) should not raise."""
        scorer = _two_criterion_scorer()
        near_one = {
            "nearly_one": {"speed": 0.497, "accuracy": 0.498},  # sum = 0.995
        }
        result = scenario_compare(scorer, _SPEED_ACCURACY_ALTS, near_one)
        assert "nearly_one" in result

    def test_single_scenario(self):
        scorer = _two_criterion_scorer()
        result = scenario_compare(
            scorer,
            _SPEED_ACCURACY_ALTS,
            {"only": {"speed": 0.5, "accuracy": 0.5}},
        )
        assert len(result) == 1
        assert "only" in result

    def test_original_scorer_not_mutated(self):
        scorer = _two_criterion_scorer()
        original_weights = {c.name: c.weight for c in scorer._criteria}
        scenario_compare(scorer, _SPEED_ACCURACY_ALTS, self._scenarios())
        final_weights = {c.name: c.weight for c in scorer._criteria}
        assert original_weights == final_weights
