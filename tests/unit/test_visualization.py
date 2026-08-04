"""Tests for decision_science.visualization."""

from unittest.mock import patch

import pytest

matplotlib = pytest.importorskip("matplotlib")
import matplotlib.pyplot as plt  # noqa: E402

from src.myproject.decision_science.scorer import DecisionResult
from src.myproject.decision_science.visualization import (
    radar_chart,
    rank_stability_heatmap,
    tornado_plot,
)


# ---------------------------------------------------------------------------
# Session fixture: close all figures after each test to avoid memory warning.
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


# ---------------------------------------------------------------------------
# Shared test fixtures / helpers
# ---------------------------------------------------------------------------

def _result(alt: str, utility: float, breakdown: dict[str, float]) -> DecisionResult:
    return DecisionResult(alternative=alt, utility=utility, breakdown=breakdown)


# Three alternatives for multi-alternative tests.
_THREE_RESULTS = [
    _result("Alpha", 0.72, {"cost": 0.27, "benefit": 0.36, "risk": 0.09}),
    _result("Beta",  0.60, {"cost": 0.18, "benefit": 0.30, "risk": 0.12}),
    _result("Gamma", 0.48, {"cost": 0.09, "benefit": 0.25, "risk": 0.14}),
]

# OAT result for tornado_plot tests.
_OAT_RESULT = {
    "baseline": [_result("A", 0.70, {"x": 0.40, "y": 0.30})],
    "x+delta":  [_result("A", 0.75, {"x": 0.45, "y": 0.30})],
    "x-delta":  [_result("A", 0.65, {"x": 0.35, "y": 0.30})],
    "y+delta":  [_result("A", 0.72, {"x": 0.40, "y": 0.32})],
    "y-delta":  [_result("A", 0.68, {"x": 0.40, "y": 0.28})],
}

# Monte Carlo result for heatmap tests.
_MC_RESULT = {
    "Alpha": {"1": 0.70, "2": 0.20, "3": 0.10},
    "Beta":  {"1": 0.20, "2": 0.55, "3": 0.25},
    "Gamma": {"1": 0.10, "2": 0.25, "3": 0.65},
}


# ---------------------------------------------------------------------------
# radar_chart
# ---------------------------------------------------------------------------

class TestRadarChart:
    def test_returns_figure(self):
        fig = radar_chart(_THREE_RESULTS)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_polar_axes(self):
        fig = radar_chart(_THREE_RESULTS)
        assert len(fig.axes) == 1
        ax = fig.axes[0]
        assert ax.name == "polar"

    def test_single_alternative(self):
        fig = radar_chart([_THREE_RESULTS[0]])
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_custom_criteria_names(self):
        """Custom criteria_names are set as tick labels on the polar axes."""
        names = ["Cost Score", "Benefit Score", "Risk Score"]
        fig = radar_chart(_THREE_RESULTS, criteria_names=names)
        ax = fig.axes[0]
        tick_labels = [t.get_text() for t in ax.get_xticklabels()]
        assert tick_labels == names

    def test_default_criteria_names_from_breakdown(self):
        """Without criteria_names, tick labels come from the breakdown keys."""
        fig = radar_chart(_THREE_RESULTS)
        ax = fig.axes[0]
        tick_labels = [t.get_text() for t in ax.get_xticklabels()]
        assert set(tick_labels) == {"cost", "benefit", "risk"}

    def test_title_set(self):
        fig = radar_chart(_THREE_RESULTS, title="My Chart")
        ax = fig.axes[0]
        assert "My Chart" in ax.get_title()

    def test_empty_results_raises(self):
        with pytest.raises(ValueError, match="empty"):
            radar_chart([])

    def test_number_of_lines_matches_alternatives(self):
        """Each alternative is drawn as one line on the polar axes."""
        fig = radar_chart(_THREE_RESULTS)
        ax = fig.axes[0]
        # Each alternative produces one Line2D.
        n_lines = len(ax.lines)
        assert n_lines == len(_THREE_RESULTS)


# ---------------------------------------------------------------------------
# tornado_plot
# ---------------------------------------------------------------------------

class TestTornadoPlot:
    def test_returns_figure(self):
        fig = tornado_plot(_OAT_RESULT, "A")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_axes(self):
        fig = tornado_plot(_OAT_RESULT, "A")
        assert len(fig.axes) >= 1

    def test_title_set(self):
        fig = tornado_plot(_OAT_RESULT, "A", title="Sensitivity")
        ax = fig.axes[0]
        assert "Sensitivity" in ax.get_title()

    def test_missing_baseline_raises(self):
        no_baseline = {k: v for k, v in _OAT_RESULT.items() if k != "baseline"}
        with pytest.raises(ValueError, match="baseline"):
            tornado_plot(no_baseline, "A")

    def test_missing_alternative_raises(self):
        with pytest.raises(ValueError, match="not found"):
            tornado_plot(_OAT_RESULT, "nonexistent")

    def test_number_of_bars_matches_criteria(self):
        """One horizontal bar group per criterion."""
        fig = tornado_plot(_OAT_RESULT, "A")
        ax = fig.axes[0]
        # Each barh call creates one Rectangle patch per bar; two criteria => 2 bars.
        n_bars = len(ax.patches)
        assert n_bars == 2  # "x" and "y"

    def test_multiple_alternatives_in_oat_selects_correct_one(self):
        """tornado_plot selects only the requested alternative's utility."""
        oat = {
            "baseline": [
                _result("A", 0.70, {"x": 0.40, "y": 0.30}),
                _result("B", 0.50, {"x": 0.25, "y": 0.25}),
            ],
            "x+delta": [
                _result("A", 0.75, {"x": 0.45, "y": 0.30}),
                _result("B", 0.55, {"x": 0.30, "y": 0.25}),
            ],
            "x-delta": [
                _result("A", 0.65, {"x": 0.35, "y": 0.30}),
                _result("B", 0.45, {"x": 0.20, "y": 0.25}),
            ],
            "y+delta": [
                _result("A", 0.72, {"x": 0.40, "y": 0.32}),
                _result("B", 0.52, {"x": 0.25, "y": 0.27}),
            ],
            "y-delta": [
                _result("A", 0.68, {"x": 0.40, "y": 0.28}),
                _result("B", 0.48, {"x": 0.25, "y": 0.23}),
            ],
        }
        fig_a = tornado_plot(oat, "A")
        fig_b = tornado_plot(oat, "B")
        # Both should return valid figures without error.
        assert isinstance(fig_a, matplotlib.figure.Figure)
        assert isinstance(fig_b, matplotlib.figure.Figure)
        # Titles should reference each alternative.
        assert "A" in fig_a.axes[0].get_title()
        assert "B" in fig_b.axes[0].get_title()


# ---------------------------------------------------------------------------
# rank_stability_heatmap
# ---------------------------------------------------------------------------

class TestRankStabilityHeatmap:
    def test_returns_figure(self):
        fig = rank_stability_heatmap(_MC_RESULT)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_axes(self):
        fig = rank_stability_heatmap(_MC_RESULT)
        assert len(fig.axes) >= 1

    def test_title_set(self):
        fig = rank_stability_heatmap(_MC_RESULT, title="Rank Stability Test")
        ax = fig.axes[0]
        assert "Rank Stability Test" in ax.get_title()

    def test_single_alternative(self):
        single = {"OnlyAlt": {"1": 1.0}}
        fig = rank_stability_heatmap(single)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_row_count_matches_alternatives(self):
        """Number of y-tick labels equals number of alternatives."""
        fig = rank_stability_heatmap(_MC_RESULT)
        ax = fig.axes[0]
        assert len(ax.get_yticks()) == len(_MC_RESULT)

    def test_col_count_matches_ranks(self):
        """Number of x-tick labels equals number of rank positions."""
        fig = rank_stability_heatmap(_MC_RESULT)
        ax = fig.axes[0]
        # The colorbar axis is a separate axes — only check the image axes.
        image_axes = [a for a in fig.axes if a.images]
        assert len(image_axes) == 1
        n_xticks = len(image_axes[0].get_xticks())
        expected_n_ranks = len(next(iter(_MC_RESULT.values())))
        assert n_xticks == expected_n_ranks

    def test_annotations_present(self):
        """Each cell should have a percentage text annotation."""
        fig = rank_stability_heatmap(_MC_RESULT)
        image_axes = [a for a in fig.axes if a.images]
        ax = image_axes[0]
        texts = ax.texts
        n_alts = len(_MC_RESULT)
        n_ranks = len(next(iter(_MC_RESULT.values())))
        assert len(texts) == n_alts * n_ranks

    def test_top_ranked_alternative_is_first_row(self):
        """Alternative with highest rank-1 frequency should appear first (top row)."""
        fig = rank_stability_heatmap(_MC_RESULT)
        image_axes = [a for a in fig.axes if a.images]
        ax = image_axes[0]
        # Alpha has rank-1 frequency 0.70, which is the highest.
        top_label = ax.get_yticklabels()[0].get_text()
        assert top_label == "Alpha"

    def test_empty_mc_result_returns_figure(self):
        """An empty mc_result should not crash — returns a figure."""
        fig = rank_stability_heatmap({})
        assert isinstance(fig, matplotlib.figure.Figure)


# ---------------------------------------------------------------------------
# ImportError guard tests (matplotlib not installed)
# ---------------------------------------------------------------------------

class TestImportErrorGuard:
    """Test that each function raises a helpful ImportError when matplotlib is absent."""

    def _builtins_import_raiser(self, name, *args, **kwargs):
        if name == "matplotlib":
            raise ImportError("No module named 'matplotlib'")
        return self._real_import(name, *args, **kwargs)

    def setup_method(self):
        import builtins
        self._real_import = builtins.__import__

    def test_radar_chart_missing_matplotlib(self):
        with patch("builtins.__import__", side_effect=self._builtins_import_raiser):
            with pytest.raises(ImportError, match="uv pip install"):
                radar_chart([_THREE_RESULTS[0]])

    def test_tornado_plot_missing_matplotlib(self):
        with patch("builtins.__import__", side_effect=self._builtins_import_raiser):
            with pytest.raises(ImportError, match="uv pip install"):
                tornado_plot(_OAT_RESULT, "A")

    def test_rank_stability_heatmap_missing_matplotlib(self):
        with patch("builtins.__import__", side_effect=self._builtins_import_raiser):
            with pytest.raises(ImportError, match="uv pip install"):
                rank_stability_heatmap(_MC_RESULT)
