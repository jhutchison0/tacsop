"""Visualization helpers for MAUT decision results.

Three plot functions covering the most common decision science charts:
- radar_chart: spider/radar comparing alternatives across criteria
- tornado_plot: horizontal bars showing weight sensitivity range
- rank_stability_heatmap: annotated heatmap of Monte Carlo rank frequencies

matplotlib is an optional dependency. Each function guard-imports it and raises
a clear ImportError if it is not installed.
"""

import math

from src.myproject.decision_science.scorer import DecisionResult


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
            "Install it with: pip install -e '.[decision-science]'"
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
