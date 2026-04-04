"""End-to-end integration test: full decision science pipeline.

Exercises the complete flow a downstream repo would use:
  YAML config → MAUTScorer → rank → sensitivity analysis → visualization
"""

import pytest

from src.myproject.decision_science import (
    MAUTScorer,
    gaussian,
    linear,
    logistic,
    monte_carlo,
    one_at_a_time,
    scenario_compare,
)

plt = pytest.importorskip("matplotlib.pyplot")


# ---------------------------------------------------------------------------
# Fixture: a realistic 4-criterion decision model loaded from YAML
# ---------------------------------------------------------------------------

YAML_CONTENT = """\
criteria:
  - name: effectiveness
    weight: 0.35
    value_fn: linear
    params: {low: 0, high: 100}
  - name: cost
    weight: 0.25
    value_fn: linear
    params: {low: 100, high: 0}   # inverted: lower cost = higher utility
  - name: risk
    weight: 0.25
    value_fn: logistic
    params: {midpoint: 50, steepness: -0.15}  # higher risk = lower utility
  - name: time_to_deliver
    weight: 0.15
    value_fn: gaussian
    params: {center: 30, sigma: 15}  # ideal delivery ~30 days
"""

ALTERNATIVES = {
    "Alpha": {"effectiveness": 85, "cost": 40, "risk": 30, "time_to_deliver": 28},
    "Bravo": {"effectiveness": 60, "cost": 20, "risk": 70, "time_to_deliver": 35},
    "Charlie": {"effectiveness": 95, "cost": 90, "risk": 20, "time_to_deliver": 60},
}


@pytest.fixture
def scorer(tmp_path):
    yaml_file = tmp_path / "model.yaml"
    yaml_file.write_text(YAML_CONTENT)
    return MAUTScorer.from_yaml(yaml_file)


# ---------------------------------------------------------------------------
# Pipeline tests
# ---------------------------------------------------------------------------

class TestFullPipeline:
    """Verify the complete YAML → score → sensitivity → visualization flow."""

    def test_yaml_load_and_rank(self, scorer):
        results = scorer.rank(ALTERNATIVES)

        assert len(results) == 3
        assert results[0].utility > results[-1].utility
        # Every result has a breakdown covering all 4 criteria
        for r in results:
            assert len(r.breakdown) == 4
            assert sum(r.breakdown.values()) == pytest.approx(r.utility)

    def test_winner_makes_domain_sense(self, scorer):
        results = scorer.rank(ALTERNATIVES)
        winner = results[0]
        # Alpha should win: good effectiveness, moderate cost, low risk, ideal timing
        assert winner.alternative == "Alpha"

    def test_oat_sensitivity_detects_instability(self, scorer):
        oat = one_at_a_time(scorer, ALTERNATIVES, delta=0.15)

        assert "baseline" in oat
        baseline_winner = oat["baseline"][0].alternative

        # Check that at least one perturbation exists per criterion
        for crit in ["effectiveness", "cost", "risk", "time_to_deliver"]:
            assert f"{crit}+delta" in oat
            assert f"{crit}-delta" in oat

        # With a large enough delta, at least one perturbation should
        # change *something* about the ranking (utility values shift)
        shifted = False
        for key, results in oat.items():
            if key == "baseline":
                continue
            if results[0].utility != pytest.approx(oat["baseline"][0].utility):
                shifted = True
                break
        assert shifted, "OAT perturbations should shift at least one utility value"

    def test_monte_carlo_frequencies_are_valid(self, scorer):
        mc = monte_carlo(scorer, ALTERNATIVES, n_samples=500, seed=42)

        assert set(mc.keys()) == {"Alpha", "Bravo", "Charlie"}

        for alt, freqs in mc.items():
            # Frequencies sum to 1.0 for each alternative
            assert sum(freqs.values()) == pytest.approx(1.0)
            # All rank positions present
            assert set(freqs.keys()) == {"1", "2", "3"}
            # All frequencies non-negative
            assert all(f >= 0.0 for f in freqs.values())

    def test_monte_carlo_confirms_winner_dominance(self, scorer):
        mc = monte_carlo(scorer, ALTERNATIVES, n_samples=1000, seed=42)
        # Alpha should be rank-1 most often
        assert mc["Alpha"]["1"] > mc["Bravo"]["1"]
        assert mc["Alpha"]["1"] > mc["Charlie"]["1"]

    def test_scenario_compare_changes_winner(self, scorer):
        scenarios = {
            "balanced": {
                "effectiveness": 0.25, "cost": 0.25,
                "risk": 0.25, "time_to_deliver": 0.25,
            },
            "cost_only": {
                "effectiveness": 0.05, "cost": 0.85,
                "risk": 0.05, "time_to_deliver": 0.05,
            },
        }
        results = scenario_compare(scorer, ALTERNATIVES, scenarios)

        assert set(results.keys()) == {"balanced", "cost_only"}

        # Under cost_only scenario (85% weight), Bravo (cheapest at $20) wins
        cost_winner = results["cost_only"][0].alternative
        assert cost_winner == "Bravo"

        # Different scenarios produce different winners — that's the point
        balanced_winner = results["balanced"][0].alternative
        assert balanced_winner != cost_winner

    def test_visualization_pipeline(self, scorer):
        """Full viz pipeline: rank → OAT → MC → all three chart types."""
        from src.myproject.decision_science import (
            radar_chart,
            rank_stability_heatmap,
            tornado_plot,
        )

        results = scorer.rank(ALTERNATIVES)
        oat = one_at_a_time(scorer, ALTERNATIVES)
        mc = monte_carlo(scorer, ALTERNATIVES, n_samples=200, seed=42)

        # All three charts produce Figure objects without crashing
        fig1 = radar_chart(results, title="Alternative Comparison")
        fig2 = tornado_plot(oat, "Alpha", title="Alpha Sensitivity")
        fig3 = rank_stability_heatmap(mc, title="Rank Stability")

        for fig in [fig1, fig2, fig3]:
            assert type(fig).__name__ == "Figure"
            plt.close(fig)


class TestProgrammaticConstruction:
    """Verify the non-YAML path works identically."""

    def test_programmatic_matches_yaml(self, scorer, tmp_path):
        from functools import partial
        from src.myproject.decision_science import Criterion

        manual = MAUTScorer([
            Criterion("effectiveness", 0.35, partial(linear, low=0, high=100)),
            Criterion("cost", 0.25, partial(linear, low=100, high=0)),
            Criterion("risk", 0.25, partial(logistic, midpoint=50, steepness=-0.15)),
            Criterion("time_to_deliver", 0.15, partial(gaussian, center=30, sigma=15)),
        ])

        yaml_results = scorer.rank(ALTERNATIVES)
        manual_results = manual.rank(ALTERNATIVES)

        assert len(yaml_results) == len(manual_results)
        for yr, mr in zip(yaml_results, manual_results):
            assert yr.alternative == mr.alternative
            assert yr.utility == pytest.approx(mr.utility)
