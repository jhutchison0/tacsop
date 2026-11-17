"""Visualization helpers for MAUT decision results.

Five plot functions:
- radar_chart: spider/radar comparing alternatives across criteria
- tornado_plot: horizontal bars showing weight sensitivity range
- rank_stability_heatmap: annotated heatmap of Monte Carlo rank frequencies
- passage_chart: every alternative from raw measurement to utility to total
- slope_chart: the same items under two conditions, one panel per rule

matplotlib is an optional dependency. Each function guard-imports it and raises
a clear ImportError if it is not installed.
"""

import math

from src.myproject.decision_science.scorer import DecisionResult, MAUTScorer


def _require_matplotlib():
    """Guard-import matplotlib, raising a helpful error if missing.

    Returns:
        The matplotlib module.

    Raises:
        ImportError: If matplotlib is not installed.
    """
    try:
        import matplotlib
        return matplotlib
    except ImportError:
        raise ImportError(
            "matplotlib is required for visualization. "
            "Install it with: uv pip install --python .venv -e '.[decision-science]'"
        )


def radar_chart(
    results: list[DecisionResult],
    criteria_names: list[str] | None = None,
    title: str = "Decision Comparison",
):
    """Radar/spider chart comparing alternatives across criteria.

    Each alternative is a colored polygon on the radar. Each spoke represents
    one criterion; values are the weighted contributions (w_i * u_i) drawn
    directly from the DecisionResult breakdown dict.

    Args:
        results: List of DecisionResult from scorer.rank() or scorer.score().
        criteria_names: Override criterion display names. If None, uses
            breakdown keys from the first result.
        title: Chart title.

    Returns:
        matplotlib.figure.Figure with the radar chart.

    Raises:
        ValueError: If results is empty.
    """
    _require_matplotlib()
    import matplotlib.pyplot as plt

    if not results:
        raise ValueError("results must not be empty")

    criteria = criteria_names if criteria_names is not None else list(results[0].breakdown.keys())
    n = len(criteria)

    # Compute evenly spaced angles, one per criterion.
    angles = [2 * math.pi * i / n for i in range(n)]
    # Close the polygon.
    angles_closed = angles + [angles[0]]

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(6, 6))

    for result in results:
        values = [result.breakdown.get(c, 0.0) for c in criteria]
        values_closed = values + [values[0]]
        ax.plot(angles_closed, values_closed, linewidth=1.5, label=result.alternative)
        ax.fill(angles_closed, values_closed, alpha=0.15)

    ax.set_xticks(angles)
    ax.set_xticklabels(criteria)
    ax.set_title(title, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    return fig


def tornado_plot(
    oat_result: dict[str, list[DecisionResult]],
    alternative: str,
    title: str = "Sensitivity Analysis",
):
    """Tornado diagram showing how each criterion's weight perturbation affects utility.

    Takes output from sensitivity.one_at_a_time(). For the specified alternative,
    shows horizontal bars for each criterion: left bar = utility at -delta,
    right bar = utility at +delta, centered on the baseline utility.
    Criteria are sorted by range (widest bar at top).

    Args:
        oat_result: Output from one_at_a_time(). Must contain a "baseline" key.
        alternative: Name of the alternative to plot sensitivity for.
        title: Chart title.

    Returns:
        matplotlib.figure.Figure with the tornado diagram.

    Raises:
        ValueError: If "baseline" key is missing from oat_result, or if the
            specified alternative is not found in the baseline results.
    """
    _require_matplotlib()
    import matplotlib.pyplot as plt

    if "baseline" not in oat_result:
        raise ValueError('oat_result must contain a "baseline" key')

    def _find_utility(results: list[DecisionResult], name: str) -> float:
        for r in results:
            if r.alternative == name:
                return r.utility
        raise ValueError(
            f'Alternative "{name}" not found in results. '
            f"Available: {[r.alternative for r in results]}"
        )

    baseline_utility = _find_utility(oat_result["baseline"], alternative)

    # Collect all criterion names from keys like "criterion+delta" / "criterion-delta".
    criterion_names: set[str] = set()
    for key in oat_result:
        if key == "baseline":
            continue
        if key.endswith("+delta"):
            criterion_names.add(key[: -len("+delta")])
        elif key.endswith("-delta"):
            criterion_names.add(key[: -len("-delta")])

    # Build rows: (criterion, low_utility, high_utility, range).
    rows = []
    for crit in criterion_names:
        low_key = f"{crit}-delta"
        high_key = f"{crit}+delta"
        low_util = _find_utility(oat_result[low_key], alternative) if low_key in oat_result else baseline_utility
        high_util = _find_utility(oat_result[high_key], alternative) if high_key in oat_result else baseline_utility
        rows.append((crit, low_util, high_util, abs(high_util - low_util)))

    # Sort widest range at top (tornado convention).
    rows.sort(key=lambda r: r[3], reverse=True)

    criteria_sorted = [r[0] for r in rows]
    y_pos = list(range(len(criteria_sorted)))

    fig, ax = plt.subplots(figsize=(8, max(3, len(criteria_sorted) * 0.6 + 1)))

    for i, (crit, low_util, high_util, _) in enumerate(rows):
        left = min(low_util, high_util) - baseline_utility
        right = max(low_util, high_util) - baseline_utility
        ax.barh(i, right - left, left=left, height=0.5, align="center")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(criteria_sorted)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Change in utility from baseline")
    ax.set_title(f"{title}\n({alternative}, baseline = {baseline_utility:.3f})")

    fig.tight_layout()
    return fig


def rank_stability_heatmap(
    mc_result: dict[str, dict[str, float]],
    title: str = "Rank Stability",
):
    """Heatmap showing rank frequency from Monte Carlo sensitivity analysis.

    Takes output from sensitivity.monte_carlo(). Rows are alternatives, columns
    are rank positions. Cell values are frequencies (0.0 to 1.0), annotated
    with percentage text.

    Rows are sorted by most frequent rank-1 frequency, descending.

    Args:
        mc_result: Output from monte_carlo(). {alternative: {rank_str: frequency}}.
        title: Chart title.

    Returns:
        matplotlib.figure.Figure with the annotated heatmap.
    """
    _require_matplotlib()
    import matplotlib.pyplot as plt

    alternatives = list(mc_result.keys())
    if not alternatives:
        # Return an empty figure for the degenerate case.
        fig, ax = plt.subplots()
        ax.set_title(title)
        return fig

    # Determine rank positions from the first alternative's keys.
    first_ranks = mc_result[alternatives[0]]
    n_ranks = len(first_ranks)
    rank_labels = [str(i + 1) for i in range(n_ranks)]

    # Sort alternatives by rank-1 frequency, descending.
    alternatives_sorted = sorted(
        alternatives,
        key=lambda a: mc_result[a].get("1", 0.0),
        reverse=True,
    )

    # Build the 2D data matrix: rows = alternatives, cols = ranks.
    data = [
        [mc_result[alt].get(rank, 0.0) for rank in rank_labels]
        for alt in alternatives_sorted
    ]

    n_alts = len(alternatives_sorted)
    fig_height = max(3, n_alts * 0.6 + 1.5)
    fig_width = max(4, n_ranks * 0.8 + 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    im = ax.imshow(data, aspect="auto", cmap="Blues", vmin=0.0, vmax=1.0)

    ax.set_xticks(range(n_ranks))
    ax.set_xticklabels([f"Rank {r}" for r in rank_labels])
    ax.set_yticks(range(n_alts))
    ax.set_yticklabels(alternatives_sorted)
    ax.set_title(title)

    # Annotate each cell with percentage.
    for row_idx in range(n_alts):
        for col_idx in range(n_ranks):
            value = data[row_idx][col_idx]
            pct_text = f"{value:.0%}"
            # Use dark text on light cells, light text on dark cells.
            text_color = "white" if value > 0.6 else "black"
            ax.text(
                col_idx,
                row_idx,
                pct_text,
                ha="center",
                va="center",
                color=text_color,
                fontsize=9,
            )

    fig.colorbar(im, ax=ax, label="Frequency")
    fig.tight_layout()
    return fig


_INK = "#333333"  # marks and labels
_QUIET = "#9a9a9a"  # curves, frames, and items the reader is not asked to follow
_NOTE = "#666666"  # units, sources, column heads


def _spread(values: list[float], gap: float, low: float, high: float) -> list[float]:
    """Move label positions apart until each is `gap` from the next, kept inside [low, high].

    Labels that would collide form a group, and the group is centred on the mean of the
    values it names, so no label drifts further from its mark than the crowd requires.
    Returns the positions in the order given. Labels move; the marks they name do not.
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    groups: list[list[float]] = []  # each: [sum of values, count]
    for i in order:
        groups.append([values[i], 1])
        while len(groups) > 1:
            (below_sum, below_n), (above_sum, above_n) = groups[-2], groups[-1]
            top_of_below = below_sum / below_n + (below_n - 1) * gap / 2
            bottom_of_above = above_sum / above_n - (above_n - 1) * gap / 2
            if bottom_of_above - top_of_below >= gap:
                break
            groups[-2:] = [[below_sum + above_sum, below_n + above_n]]
    placed: list[float] = []
    for total, count in groups:
        span = (count - 1) * gap
        start = min(max(total / count - span / 2, low), max(low, high - span))
        placed.extend(start + n * gap for n in range(count))
    out = [0.0] * len(values)
    for position, i in zip(placed, order):
        out[i] = position
    return out


def passage_chart(
    scorer: MAUTScorer,
    alternatives: dict[str, dict[str, float]],
    title: str = "From a raw measurement to a utility to a total",
    source: str | None = None,
    highlight: list[str] | None = None,
):
    """The passage of every alternative through the model: raw value, utility, total.

    One panel per criterion, in the model's order. The horizontal axis is the raw
    measurement in its own unit; the curve is the criterion's value function; each
    alternative is a point on it. Every panel shares the vertical scale, utility from
    0 to 1, and a panel's width is its weight, so the last panel (the total, the sum
    of weight times utility) can be read against the panels that feed it. An axis
    whose value function falls is drawn reversed, so better is up and to the right
    in every panel.

    Args:
        scorer: The model.
        alternatives: Mapping of alternative name to its raw scores.
        title: Figure title.
        source: Where the numbers come from, printed under the figure.
        highlight: Alternatives to draw in full ink; the rest go quiet. None draws all in full.

    Returns:
        matplotlib.figure.Figure with len(scorer.criteria) + 1 axes.

    Raises:
        ValueError: If alternatives is empty, or the scorer refuses them.
    """
    _require_matplotlib()
    import matplotlib.pyplot as plt

    results = scorer.rank(alternatives)
    criteria = scorer.criteria
    loud = set(highlight) if highlight else {r.alternative for r in results}

    fig = plt.figure(figsize=(11.5, 4.0))
    grid = fig.add_gridspec(
        1, len(criteria) + 1, width_ratios=[c.weight for c in criteria] + [0.14],
        left=0.05, right=0.88, top=0.74, bottom=0.17, wspace=0.16,
    )
    gap = 0.06  # utility units between two label baselines at this figure height

    for column, criterion in enumerate(criteria):
        ax = fig.add_subplot(grid[0, column])
        raws = [alternatives[r.alternative][criterion.name] for r in results]
        low, high = min(raws), max(raws)
        pad = (high - low) * 0.12 or 1.0
        xs = [low - pad + (high - low + 2 * pad) * step / 100 for step in range(101)]
        curve = [min(1.0, max(0.0, criterion.value_fn(x))) for x in xs]
        ax.plot(xs, curve, color=_QUIET, linewidth=0.9, zorder=1)
        falls = curve[0] > curve[-1]
        ax.set_xlim((xs[-1], xs[0]) if falls else (xs[0], xs[-1]))

        spans = xs[-1] - xs[0]
        on_the_right = [((x - xs[0]) / spans > 0.5) != falls for x in raws]  # where the point sits in the panel
        utilities = [r.raw_utilities[criterion.name] for r in results]
        heights = _spread(utilities, gap, 0.0, 1.0)
        for result, x, y, height, right in zip(results, raws, utilities, heights, on_the_right):
            ink = _INK if result.alternative in loud else _QUIET
            ax.plot([x], [y], marker="o", markersize=4.2, linestyle="none", color=ink, zorder=3)
            ax.annotate(
                result.alternative, (x, height), xytext=(-6 if right else 6, 0), textcoords="offset points",
                ha="right" if right else "left", va="center", fontsize=7, color=ink, zorder=4,
            )

        ax.set_ylim(-0.04, 1.04)
        ax.set_xticks([low, high])
        ax.set_xticklabels([f"{low:,g}", f"{high:,g}"], fontsize=7, color=_NOTE)
        ax.tick_params(axis="x", length=2, color=_QUIET)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_bounds(low, high)  # the frame spans the data and no further
        ax.spines["bottom"].set_color(_QUIET)
        if column == 0:
            ax.set_yticks([0, 0.5, 1])
            ax.set_yticklabels(["0", "0.5", "1"], fontsize=7, color=_NOTE)
            ax.set_ylabel("utility", fontsize=7, color=_NOTE)
            ax.spines["left"].set_bounds(0, 1)
            ax.spines["left"].set_color(_QUIET)
            ax.tick_params(axis="y", length=2, color=_QUIET)
        else:
            ax.set_yticks([])
            ax.spines["left"].set_visible(False)
        ax.set_title(f"{criterion.name}\nweight {criterion.weight:.2f}", fontsize=8, loc="left", color=_INK)

    ax = fig.add_subplot(grid[0, -1])
    totals = [r.utility for r in results]
    for result, y, height in zip(results, totals, _spread(totals, gap, 0.0, 1.0)):
        ink = _INK if result.alternative in loud else _QUIET
        ax.plot([0], [y], marker="o", markersize=4.2, linestyle="none", color=ink, zorder=3)
        ax.annotate(
            f"{result.alternative}  {y:.3f}", (0, height), xytext=(7, 0), textcoords="offset points",
            ha="left", va="center", fontsize=7.5, color=ink,
        )
    ax.set_ylim(-0.04, 1.04)
    ax.set_xlim(-0.5, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("total\nsum of weight × utility", fontsize=8, loc="left", color=_INK)

    fig.suptitle(title, x=0.05, y=0.97, ha="left", fontsize=11, color=_INK)
    fig.text(
        0.05, 0.035,
        "Each panel: raw measurement across, utility up, one point per alternative on the criterion's value function. "
        "Panel width is the weight." + (f"  Source: {source}" if source else ""),
        fontsize=7, color=_NOTE, ha="left",
    )
    return fig


def slope_chart(
    panels: dict[str, dict[str, dict[str, float]]],
    title: str = "",
    source: str | None = None,
    highlight: list[str] | None = None,
    value_format: str = "{:.3f}",
):
    """The same items under two conditions, one panel per rule, every panel on one scale.

    Each panel is a slopegraph: a column per condition, a point per item at its value, a
    line joining an item's points, and the item's name and value written at both ends.
    An item present in one column only is a point with no line. There is no axis, no
    grid and no legend: the labels are the scale.

    Args:
        panels: {panel title: {column label: {item: value}}}. Panels are drawn left to
            right and columns in the order given.
        title: Figure title.
        source: Where the numbers come from and their unit, printed under the figure.
        highlight: Items to draw in full ink; the rest go quiet. None draws all in full.
        value_format: Format string for a value in a label.

    Returns:
        matplotlib.figure.Figure with one axes per panel.

    Raises:
        ValueError: If panels is empty.
    """
    _require_matplotlib()
    import matplotlib.pyplot as plt

    if not panels:
        raise ValueError("panels must not be empty")

    values = [v for columns in panels.values() for column in columns.values() for v in column.values()]
    low, high = min(values), max(values)
    margin = (high - low) * 0.08 or 0.5
    height_in = 4.4
    fig, axes = plt.subplots(1, len(panels), sharey=True, figsize=(5.2 * len(panels), height_in), squeeze=False)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.78, bottom=0.10, wspace=0.05)
    gap = (high - low + 2 * margin) * (8 * 1.45 / 72) / (height_in * 0.68)  # one label line, in data units

    for ax, (panel, columns) in zip(axes[0], panels.items()):
        heads = list(columns)
        items = list(dict.fromkeys(item for column in columns.values() for item in column))
        for item in items:
            points = [(x, columns[head][item]) for x, head in enumerate(heads) if item in columns[head]]
            loud = highlight is None or item in highlight
            ax.plot(
                [x for x, _ in points], [y for _, y in points], label=item, marker="o", markersize=3.6,
                linewidth=1.5 if loud and highlight else 1.0, color=_INK if loud else _QUIET,
                zorder=3 if loud else 2,
            )
        for x, ha, template in ((0, "right", "{name}  {value}"), (len(heads) - 1, "left", "{value}  {name}")):
            column = columns[heads[x]]
            names = list(column)
            for name, y in zip(names, _spread([column[n] for n in names], gap, low - margin, high + margin)):
                ax.text(
                    x + (-0.07 if ha == "right" else 0.07), y,
                    template.format(name=name, value=value_format.format(column[name])),
                    ha=ha, va="center", fontsize=8, color=_INK if highlight is None or name in highlight else _QUIET,
                )
            if len(heads) == 1:
                break
        for x, head in enumerate(heads):
            ax.text(x, high + margin * 2.2, head, ha="center", va="bottom", fontsize=8, color=_NOTE)
        ax.set_xlim(-1.25, len(heads) - 1 + 1.25)
        ax.set_ylim(low - margin, high + margin * 3.4)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(panel, fontsize=9.5, loc="center", color=_INK, pad=10)

    if title:
        fig.suptitle(title, x=0.03, y=0.97, ha="left", fontsize=11, color=_INK)
    if source:
        fig.text(0.03, 0.03, source, fontsize=7, color=_NOTE, ha="left")
    return fig
