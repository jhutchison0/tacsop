"""Tests for decision_science.visualization."""

import math
import random
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

matplotlib = pytest.importorskip("matplotlib")
import matplotlib.pyplot as plt  # noqa: E402

from src.myproject.decision_science.scorer import DecisionResult, MAUTScorer
from src.myproject.decision_science.visualization import (
    _spread,
    passage_chart,
    radar_chart,
    rank_stability_heatmap,
    slope_chart,
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
            with pytest.raises(ImportError, match=r"uv pip install --python \.venv"):
                radar_chart([_THREE_RESULTS[0]])

    def test_tornado_plot_missing_matplotlib(self):
        with patch("builtins.__import__", side_effect=self._builtins_import_raiser):
            with pytest.raises(ImportError, match=r"uv pip install --python \.venv"):
                tornado_plot(_OAT_RESULT, "A")

    def test_rank_stability_heatmap_missing_matplotlib(self):
        with patch("builtins.__import__", side_effect=self._builtins_import_raiser):
            with pytest.raises(ImportError, match=r"uv pip install --python \.venv"):
                rank_stability_heatmap(_MC_RESULT)


# ---------------------------------------------------------------------------
# passage_chart: raw measurement -> utility -> total, one panel per criterion
# ---------------------------------------------------------------------------

_PASSAGE_MODEL = Path(__file__).resolve().parents[1] / "fixtures" / "tour" / "depot_model.yaml"
_PASSAGE_SITES = {
    "Rail Yard": {"annual_cost": 780, "drive_minutes": 22, "storage_pallets": 4200, "flood_free_years": 27},
    "River Bend": {"annual_cost": 340, "drive_minutes": 18, "storage_pallets": 1800, "flood_free_years": 19},
}


def _texts(fig) -> str:
    return "\n".join(t.get_text() for t in fig.findobj(matplotlib.text.Text))


@pytest.mark.filterwarnings("ignore:Criterion .* has utility range")
class TestPassageChart:
    def _chart(self, **kwargs):
        scorer = MAUTScorer.from_yaml(_PASSAGE_MODEL)
        return scorer, passage_chart(scorer, _PASSAGE_SITES, **kwargs)

    def test_one_panel_per_criterion_and_one_for_the_total(self):
        scorer, fig = self._chart()
        assert len(fig.axes) == len(scorer.criteria) + 1

    def test_panel_width_is_the_weight(self):
        scorer, fig = self._chart()
        widths = [ax.get_position().width for ax in fig.axes[:-1]]
        weights = [c.weight for c in scorer.criteria]
        for width, weight in zip(widths, weights):
            assert width / widths[0] == pytest.approx(weight / weights[0], rel=0.02)

    def test_every_panel_shares_the_utility_scale(self):
        _, fig = self._chart()
        assert {ax.get_ylim() for ax in fig.axes} == {(-0.04, 1.04)}

    def test_each_site_is_marked_at_its_utility_in_each_panel(self):
        scorer, fig = self._chart()
        results = {r.alternative: r for r in scorer.rank(_PASSAGE_SITES)}
        for ax, criterion in zip(fig.axes, scorer.criteria):
            marked = sorted(float(y) for line in ax.lines if line.get_marker() == "o" for y in line.get_ydata())
            assert marked == pytest.approx(sorted(r.raw_utilities[criterion.name] for r in results.values()))
        totals = sorted(float(y) for line in fig.axes[-1].lines if line.get_marker() == "o" for y in line.get_ydata())
        assert totals == pytest.approx(sorted(r.utility for r in results.values()))

    def test_sites_are_labelled_on_the_figure_and_there_is_no_legend(self):
        _, fig = self._chart()
        assert all(ax.get_legend() is None for ax in fig.axes)
        assert "Rail Yard" in _texts(fig) and "River Bend" in _texts(fig)

    def test_title_units_and_source_are_on_the_figure(self):
        _, fig = self._chart(title="Two sites", source="depot_model.yaml, invented")
        text = _texts(fig)
        assert "Two sites" in text and "depot_model.yaml, invented" in text
        assert "weight 0.30" in text and "annual_cost" in text

    def test_no_alternatives_is_refused(self):
        with pytest.raises(ValueError, match="No alternatives"):
            passage_chart(MAUTScorer.from_yaml(_PASSAGE_MODEL), {})

    def test_no_mark_in_the_total_panel_covers_another(self):
        """River Bend (0.696) and Rail Yard (0.692) sit 0.6 pt apart; two marks too close make a third, so one moves."""
        sites = yaml.safe_load((_PASSAGE_MODEL.parent / "depot_sites.yaml").read_text())["alternatives"]
        fig = passage_chart(MAUTScorer.from_yaml(_PASSAGE_MODEL), sites)
        marks = [line for line in fig.axes[-1].lines if line.get_marker() == "o"]
        assert len(marks) == len(sites)
        centres = [line.get_transform().transform((float(line.get_xdata()[0]), float(line.get_ydata()[0]))) for line in marks]
        diameter = (marks[0].get_markersize() + marks[0].get_markeredgewidth()) * fig.dpi / 72
        for i, a in enumerate(centres):
            for b in centres[i + 1:]:
                assert math.dist(a, b) >= diameter - 1e-6, "two marks in the total panel overlap"
        for line in marks:  # the vertical position is the total itself: a mark moves sideways only
            assert float(line.get_ydata()[0]) in {r.utility for r in MAUTScorer.from_yaml(_PASSAGE_MODEL).rank(sites)}


# ---------------------------------------------------------------------------
# slope_chart: the same items under two or more conditions, panel beside panel
# ---------------------------------------------------------------------------

_SLOPE_PANELS = {
    "scaled to the sites present": {
        "four sites": {"Rail Yard": 0.605, "River Bend": 0.600, "Airport Road": 0.547, "Old Mill": 0.270},
        "Old Mill withdrawn": {"River Bend": 0.600, "Rail Yard": 0.575, "Airport Road": 0.417},
    },
    "scaled by the model": {
        "four sites": {"Airport Road": 0.763, "River Bend": 0.696, "Rail Yard": 0.692, "Old Mill": 0.640},
        "Old Mill withdrawn": {"Airport Road": 0.763, "River Bend": 0.696, "Rail Yard": 0.692},
    },
}


class TestSlopeChart:
    def test_one_panel_per_condition_on_one_scale(self):
        fig = slope_chart(_SLOPE_PANELS)
        assert len(fig.axes) == 2
        assert len({ax.get_ylim() for ax in fig.axes}) == 1

    def test_an_item_in_both_columns_gets_a_line_and_an_item_in_one_gets_a_point(self):
        fig = slope_chart(_SLOPE_PANELS)
        for ax in fig.axes:
            lengths = sorted(len(line.get_xdata()) for line in ax.lines)
            assert lengths == [1, 2, 2, 2]

    def test_every_item_is_labelled_with_its_value_at_both_ends(self):
        text = _texts(slope_chart(_SLOPE_PANELS))
        assert text.count("Rail Yard") == 4 and text.count("Old Mill") >= 2
        assert "0.605" in text and "0.575" in text and "0.763" in text

    def test_labels_in_one_column_never_overlap(self):
        fig = slope_chart(_SLOPE_PANELS)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        for ax in fig.axes:
            by_side: dict[str, list] = {}
            for label in ax.texts:
                by_side.setdefault(label.get_ha(), []).append(label.get_window_extent(renderer))
            for boxes in by_side.values():
                for i, a in enumerate(boxes):
                    for b in boxes[i + 1:]:
                        assert not a.overlaps(b), "two labels in one column overlap"

    def test_no_axis_ink_and_no_legend(self):
        fig = slope_chart(_SLOPE_PANELS)
        for ax in fig.axes:
            assert ax.get_legend() is None
            assert not any(spine.get_visible() for spine in ax.spines.values())
            assert len(ax.get_yticks()) == 0

    def test_title_and_source_are_on_the_figure(self):
        text = _texts(slope_chart(_SLOPE_PANELS, title="A withdrawal", source="depot fixtures, invented"))
        assert "A withdrawal" in text and "depot fixtures, invented" in text
        assert "scaled by the model" in text and "Old Mill withdrawn" in text

    def test_highlighted_items_are_drawn_darker_than_the_rest(self):
        fig = slope_chart(_SLOPE_PANELS, highlight=["Airport Road"])
        colors = {line.get_label(): line.get_color() for line in fig.axes[0].lines}
        assert colors["Airport Road"] != colors["Rail Yard"]

    def test_no_panels_is_refused(self):
        with pytest.raises(ValueError, match="panels must not be empty"):
            slope_chart({})


class TestSpread:
    def test_labels_already_apart_do_not_move(self):
        assert _spread([0.1, 0.5, 0.9], 0.05, 0.0, 1.0) == pytest.approx([0.1, 0.5, 0.9])

    def test_a_crowd_is_centred_on_the_values_it_names(self):
        placed = _spread([0.696, 0.692, 0.2], 0.06, 0.0, 1.0)
        assert placed[0] - placed[1] == pytest.approx(0.06)
        assert (placed[0] + placed[1]) / 2 == pytest.approx(0.694)
        assert placed[2] == pytest.approx(0.2)

    def test_a_crowd_at_the_top_stays_inside_the_bounds(self):
        placed = _spread([1.0, 0.99, 0.98], 0.05, 0.0, 1.0)
        assert max(placed) <= 1.0 and sorted(placed)[1] - sorted(placed)[0] == pytest.approx(0.05)

    def test_values_tied_at_a_bound_keep_the_gap(self):
        placed = _spread([0, 0, 0, 0.13], 0.06, 0.0, 1.0)
        assert min(b - a for a, b in zip(sorted(placed), sorted(placed)[1:])) >= 0.06 - 1e-9
        assert min(placed) >= 0.0 and max(placed) <= 1.0

    def test_any_crowd_the_range_can_hold_keeps_the_gap_and_the_bounds(self):
        rng = random.Random(0)
        for _ in range(2000):
            values = [rng.choice([0.0, 1.0, rng.random()]) for _ in range(rng.randint(2, 8))]
            placed = _spread(values, 0.06, 0.0, 1.0)  # 7 gaps of 0.06 fit in 0 to 1
            ordered = sorted(placed)
            assert min(b - a for a, b in zip(ordered, ordered[1:])) >= 0.06 - 1e-9, values
            assert ordered[0] >= -1e-9 and ordered[-1] <= 1.0 + 1e-9, values
            assert [placed[i] for i in sorted(range(len(values)), key=lambda i: values[i])] == pytest.approx(ordered)

    def test_a_crowd_the_range_cannot_hold_is_spaced_evenly_across_the_range_in_the_order_of_its_values(self):
        placed = _spread([0.5, 0.1, 0.5, 0.9], 0.4, 0.0, 1.0)  # 3 gaps of 0.4 need 1.2 of a range of 1.0
        assert placed[1] == pytest.approx(0.0) and placed[3] == pytest.approx(1.0)
        assert sorted(placed) == pytest.approx([0.0, 1 / 3, 2 / 3, 1.0])


class TestDisplayOptions:
    def test_slope_chart_formats_values_as_asked(self):
        text = _texts(slope_chart({"p": {"a": {"x": 1234.5}, "b": {"x": 1500.0}}}, value_format="{:,.0f}"))
        assert "1,234" in text and "1,500" in text and "1234.5" not in text

    def test_slope_chart_with_one_column_labels_each_item_once(self):
        fig = slope_chart({"p": {"only": {"x": 0.2, "y": 0.8}}})
        labels = [t.get_text() for t in fig.axes[0].texts]
        assert sum("x" in label for label in labels) == 1 and sum("y" in label and "only" not in label for label in labels) == 1

    @pytest.mark.filterwarnings("ignore:Criterion .* has utility range")
    def test_passage_chart_quiets_every_alternative_not_highlighted(self):
        fig = passage_chart(MAUTScorer.from_yaml(_PASSAGE_MODEL), _PASSAGE_SITES, highlight=["Rail Yard"])
        for ax in fig.axes:
            colors = {line.get_color() for line in ax.lines if line.get_marker() == "o"}
            assert len(colors) == 2, "one ink for the site followed, one for the rest"
