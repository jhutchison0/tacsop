"""Sensitivity analysis for MAUT decisions.

Three analysis methods for understanding how robust a ranking is:
- one_at_a_time: vary each criterion weight by ±delta, observe rank changes
- monte_carlo: sample weight vectors from Dirichlet distribution
- scenario_compare: evaluate alternatives under named weight profiles
"""

from dataclasses import dataclass

import numpy as np

from src.myproject.decision_science.scorer import Criterion, DecisionResult, MAUTScorer


def _rescored(
    scorer: MAUTScorer,
    weights: dict[str, float],
    alternatives: dict[str, dict[str, float]],
) -> list[DecisionResult]:
    """Build a temporary scorer with new weights and rank all alternatives.

    The value functions are preserved from the original scorer. This helper
    never mutates the input scorer.

    Args:
        scorer: Original scorer; provides criterion order and value functions.
        weights: Mapping of criterion name to new weight. Must cover all
            criteria in the scorer.
        alternatives: Mapping of alternative name to raw_scores dict.

    Returns:
        List of DecisionResult sorted descending by utility.
    """
    new_criteria = [
        Criterion(
            name=c.name,
            weight=weights[c.name],
            value_fn=c.value_fn,
        )
        for c in scorer.criteria
    ]
    tmp = MAUTScorer(new_criteria)
    return tmp.rank(alternatives)


def one_at_a_time(
    scorer: MAUTScorer,
    alternatives: dict[str, dict[str, float]],
    delta: float = 0.1,
) -> dict[str, list[DecisionResult]]:
    """Vary each criterion weight by ±delta, renormalize remaining weights proportionally.

    For each criterion, two perturbations are created: weight + delta and
    weight - delta. The perturbed weight is clamped to [0, 1]. The remaining
    criteria weights are scaled proportionally so all weights still sum to 1.0.

    Args:
        scorer: Configured MAUTScorer with valid weights and value functions.
        alternatives: Mapping of alternative name to raw_scores dict.
        delta: Amount to add or subtract from each criterion weight. Defaults
            to 0.1.

    Returns:
        Dict keyed by "{criterion_name}+delta" and "{criterion_name}-delta"
        for each criterion, plus "baseline" for the unperturbed ranking. Each
        value is a list of DecisionResult sorted descending by utility.

    Raises:
        ValueError: If the scorer has invalid weights or alternatives is empty.
    """
    scorer.validate_weights()

    criteria = scorer.criteria
    baseline_weights = {c.name: c.weight for c in criteria}
    results: dict[str, list[DecisionResult]] = {
        "baseline": _rescored(scorer, baseline_weights, alternatives)
    }

    # With a single criterion there are no other criteria to absorb weight
    # changes, so perturbation is meaningless — return only the baseline.
    if len(criteria) == 1:
        return results

    for criterion in criteria:
        for sign, label_suffix in [(+1, f"+delta"), (-1, f"-delta")]:
            perturbed = min(1.0, max(0.0, criterion.weight + sign * delta))
            remaining_original = {
                c.name: c.weight
                for c in criteria
                if c.name != criterion.name
            }
            remaining_total = sum(remaining_original.values())

            new_weights: dict[str, float] = {criterion.name: perturbed}

            if remaining_total == 0.0:
                # All weight is on the one criterion being perturbed; distribute
                # leftover evenly among remaining criteria (edge case).
                leftover = 1.0 - perturbed
                n_others = len(criteria) - 1
                for name in remaining_original:
                    new_weights[name] = leftover / n_others if n_others > 0 else 0.0
            else:
                # Scale remaining weights so the full budget is 1.0.
                scale = (1.0 - perturbed) / remaining_total
                for name, w in remaining_original.items():
                    new_weights[name] = w * scale

            key = f"{criterion.name}{label_suffix}"
            results[key] = _rescored(scorer, new_weights, alternatives)

    return results


def monte_carlo(
    scorer: MAUTScorer,
    alternatives: dict[str, dict[str, float]],
    n_samples: int = 1000,
    seed: int | None = None,
) -> dict[str, dict[str, float]]:
    """Sample weight vectors from Dirichlet distribution, score alternatives under each.

    The Dirichlet alpha vector uses the current weights as concentration
    parameters scaled by the number of criteria, so the distribution clusters
    near the original weights while still exploring the simplex.

    Args:
        scorer: Configured MAUTScorer with valid weights and value functions.
        alternatives: Mapping of alternative name to raw_scores dict.
        n_samples: Number of Dirichlet samples to draw. Defaults to 1000.
        seed: Optional random seed for reproducibility. Defaults to None.

    Returns:
        Rank frequency matrix: {alternative_name: {rank_str: frequency}} where
        frequency is the proportion of samples (0.0 to 1.0) in which that
        alternative achieved that rank position. rank_str is "1", "2", etc.
        (1 = best).

    Raises:
        ValueError: If the scorer has invalid weights or alternatives is empty.
    """
    scorer.validate_weights()
    if not alternatives:
        raise ValueError("No alternatives to rank")

    criteria = scorer.criteria
    criterion_names = [c.name for c in criteria]
    original_weights = np.array([c.weight for c in criteria], dtype=float)
    n_criteria = len(criterion_names)
    alt_names = list(alternatives.keys())
    n_alts = len(alt_names)

    # Scale alpha so samples cluster near the original weights.
    alpha = original_weights * n_criteria

    rng = np.random.default_rng(seed)
    weight_samples = rng.dirichlet(alpha, size=n_samples)

    # rank_counts[alt_index][rank_index] = number of samples at that rank
    rank_counts: list[list[int]] = [[0] * n_alts for _ in range(n_alts)]

    for sample_weights in weight_samples:
        weights_dict = {name: float(w) for name, w in zip(criterion_names, sample_weights)}
        ranked = _rescored(scorer, weights_dict, alternatives)
        for rank_idx, result in enumerate(ranked):
            alt_idx = alt_names.index(result.alternative)
            rank_counts[alt_idx][rank_idx] += 1

    freq_matrix: dict[str, dict[str, float]] = {}
    for alt_idx, alt_name in enumerate(alt_names):
        freq_matrix[alt_name] = {
            str(rank_pos + 1): rank_counts[alt_idx][rank_pos] / n_samples
            for rank_pos in range(n_alts)
        }

    return freq_matrix


def scenario_compare(
    scorer: MAUTScorer,
    alternatives: dict[str, dict[str, float]],
    scenarios: dict[str, dict[str, float]],
) -> dict[str, list[DecisionResult]]:
    """Evaluate alternatives under named weight profiles (scenarios).

    Each scenario is a complete weight vector that replaces the scorer's
    current weights. Value functions are preserved from the original scorer.

    Args:
        scorer: Configured MAUTScorer; provides criterion names and value
            functions. Its weights are not used — scenario weights replace them.
        alternatives: Mapping of alternative name to raw_scores dict.
        scenarios: Mapping of scenario name to {criterion_name: weight} dict.
            Each scenario must cover exactly the same criterion names as the
            scorer, and each weight dict must sum to 1.0 within ±0.01.

    Returns:
        Dict keyed by scenario name, each value being a list of DecisionResult
        sorted descending by utility.

    Raises:
        ValueError: If any scenario has wrong criterion names or weights that
            do not sum to 1.0 within ±0.01.
    """
    scorer_criterion_names = {c.name for c in scorer.criteria}

    for scenario_name, weights in scenarios.items():
        scenario_names = set(weights.keys())
        if scenario_names != scorer_criterion_names:
            missing = scorer_criterion_names - scenario_names
            extra = scenario_names - scorer_criterion_names
            parts = []
            if missing:
                parts.append(f"missing criteria: {sorted(missing)}")
            if extra:
                parts.append(f"unknown criteria: {sorted(extra)}")
            raise ValueError(
                f"Scenario '{scenario_name}' has wrong criterion names — "
                + "; ".join(parts)
            )

        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(
                f"Scenario '{scenario_name}' weights sum to {total:.4f}; "
                f"must be 1.0 ±0.01"
            )

    return {
        name: _rescored(scorer, weights, alternatives)
        for name, weights in scenarios.items()
    }


@dataclass
class RobustnessReport:
    """Summary of Monte Carlo sensitivity results as a single confidence metric.

    Attributes:
        winner: Alternative with the highest rank-1 frequency.
        winner_frequency: Proportion of samples where winner ranked first.
        runner_up: Alternative with the second-highest rank-1 frequency.
        runner_up_frequency: Proportion of samples where runner_up ranked first.
        margin: Difference between winner_frequency and runner_up_frequency.
        is_robust: True when margin exceeds the robustness threshold.
    """

    winner: str
    winner_frequency: float
    runner_up: str
    runner_up_frequency: float
    margin: float
    is_robust: bool


def robustness_report(
    mc_result: dict[str, dict[str, float]],
    threshold: float = 0.2,
) -> RobustnessReport:
    """Summarize Monte Carlo results into a single confidence metric.

    Args:
        mc_result: Output from monte_carlo(). {alternative: {rank_str: frequency}}.
        threshold: Margin required for is_robust to be True. Defaults to 0.2.

    Returns:
        RobustnessReport with winner, runner_up, margin, and is_robust flag.

    Raises:
        ValueError: If mc_result is empty or has fewer than two alternatives.
    """
    if len(mc_result) < 2:
        raise ValueError(
            f"robustness_report requires at least 2 alternatives; got {len(mc_result)}"
        )

    rank1_freqs = {alt: freqs.get("1", 0.0) for alt, freqs in mc_result.items()}
    sorted_alts = sorted(rank1_freqs, key=lambda a: rank1_freqs[a], reverse=True)

    winner = sorted_alts[0]
    runner_up = sorted_alts[1]
    winner_freq = rank1_freqs[winner]
    runner_up_freq = rank1_freqs[runner_up]
    margin = winner_freq - runner_up_freq

    return RobustnessReport(
        winner=winner,
        winner_frequency=winner_freq,
        runner_up=runner_up,
        runner_up_frequency=runner_up_freq,
        margin=margin,
        is_robust=margin > threshold,
    )
