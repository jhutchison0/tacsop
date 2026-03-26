"""MAUTScorer: additive multi-attribute utility aggregation."""

import functools
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import yaml

from src.myproject.decision_science import value_functions as vf


@dataclass
class Criterion:
    """A single decision criterion with its weight and value function.

    Attributes:
        name: Unique identifier for this criterion.
        weight: Contribution weight; all weights must sum to 1.0.
        value_fn: Callable that maps a raw score to utility in [0, 1].
    """

    name: str
    weight: float
    value_fn: Callable[[float], float]


@dataclass
class DecisionResult:
    """Scored outcome for one alternative.

    Attributes:
        alternative: Name of the alternative.
        utility: Aggregate utility U = sum(w_i * u_i).
        breakdown: Per-criterion weighted contributions {name: w_i * u_i}.
        raw_utilities: Per-criterion unweighted utilities {name: u_i}.
    """

    alternative: str
    utility: float
    breakdown: dict[str, float] = field(default_factory=dict)
    raw_utilities: dict[str, float] = field(default_factory=dict)

    def explain(self) -> dict:
        """Structured explanation of this result.

        Returns:
            Dict with keys: alternative, utility, criteria (list of per-criterion
            dicts with name, raw_utility, weighted_contribution, pct_of_total).
        """
        total = self.utility or 1.0
        criteria_detail = []
        for name, weighted in self.breakdown.items():
            raw = self.raw_utilities.get(name, 0.0)
            criteria_detail.append({
                "name": name,
                "raw_utility": round(raw, 4),
                "weighted_contribution": round(weighted, 4),
                "pct_of_total": round(weighted / total, 4) if total > 0 else 0.0,
            })
        criteria_detail.sort(key=lambda c: c["weighted_contribution"], reverse=True)
        return {
            "alternative": self.alternative,
            "utility": round(self.utility, 4),
            "criteria": criteria_detail,
        }


class MAUTScorer:
    """Additive MAUT scorer.

    Computes U = sum(w_i * u_i(raw_i)) for each alternative and ranks them.
    """

    def __init__(self, criteria: list[Criterion] | None = None) -> None:
        """Initialize with an optional list of criteria.

        Args:
            criteria: Starting criteria. More can be added via add_criterion().
        """
        self._criteria: list[Criterion] = list(criteria) if criteria else []

    @property
    def criteria(self) -> list[Criterion]:
        """Read-only view of the scorer's criteria."""
        return list(self._criteria)

    def add_criterion(self, criterion: Criterion) -> None:
        """Append a criterion to the scorer.

        Args:
            criterion: The criterion to add.
        """
        self._criteria.append(criterion)

    def validate_weights(self) -> None:
        """Assert that criteria weights are valid.

        Raises:
            ValueError: If there are no criteria, any weight is negative,
                or weights do not sum to 1.0 within ±0.01 tolerance.
        """
        if not self._criteria:
            raise ValueError("Scorer has no criteria defined")

        for c in self._criteria:
            if c.weight < 0.0:
                raise ValueError(
                    f"Criterion '{c.name}' has negative weight {c.weight}"
                )

        total = sum(c.weight for c in self._criteria)
        if abs(total - 1.0) > 0.01:
            raise ValueError(
                f"Weights must sum to 1.0 (±0.01); got {total:.4f}"
            )

    def score(self, alternative: str, raw_scores: dict[str, float]) -> DecisionResult:
        """Score a single alternative.

        Args:
            alternative: Name label for this alternative.
            raw_scores: Mapping of criterion name to raw attribute value.

        Returns:
            DecisionResult with aggregate utility and per-criterion breakdown.

        Raises:
            ValueError: If weights are invalid, a criterion name is missing
                from raw_scores, or a value function returns outside [0, 1].
        """
        self.validate_weights()

        missing = [c.name for c in self._criteria if c.name not in raw_scores]
        if missing:
            raise ValueError(
                f"raw_scores is missing criterion values: {missing}"
            )

        breakdown: dict[str, float] = {}
        raw_utilities: dict[str, float] = {}
        for c in self._criteria:
            u = c.value_fn(raw_scores[c.name])
            if not (0.0 <= u <= 1.0):
                raise ValueError(
                    f"Value function for '{c.name}' returned {u}, "
                    f"which is outside [0, 1] (input was {raw_scores[c.name]})"
                )
            raw_utilities[c.name] = u
            breakdown[c.name] = c.weight * u

        return DecisionResult(
            alternative=alternative,
            utility=sum(breakdown.values()),
            breakdown=breakdown,
            raw_utilities=raw_utilities,
        )

    def rank(
        self, alternatives: dict[str, dict[str, float]]
    ) -> list[DecisionResult]:
        """Score and rank all alternatives, highest utility first.

        Emits a warning for any criterion whose utility range across alternatives
        is less than 0.2 — such a criterion may be effectively deweighted.

        Args:
            alternatives: Mapping of alternative name to its raw_scores dict.

        Returns:
            List of DecisionResult sorted descending by utility.

        Raises:
            ValueError: If weights are invalid or any alternative is missing
                criterion values.
        """
        if not alternatives:
            raise ValueError("No alternatives to rank")

        results = [self.score(name, scores) for name, scores in alternatives.items()]
        results.sort(key=lambda r: r.utility, reverse=True)

        for crit in self._criteria:
            if crit.weight <= 0:
                continue
            contributions = [r.raw_utilities.get(crit.name, 0.0) for r in results]
            if contributions:
                util_range = max(contributions) - min(contributions)
                if util_range < 0.2:
                    warnings.warn(
                        f"Criterion '{crit.name}' has utility range {util_range:.3f} "
                        f"across alternatives — it may be effectively deweighted",
                        stacklevel=2,
                    )

        return results

    @classmethod
    def from_yaml(cls, path: str | Path) -> "MAUTScorer":
        """Load a MAUTScorer from a YAML decision model file.

        Expected schema::

            criteria:
              - name: damage_output
                weight: 0.35
                value_fn: linear
                params: {low: 0, high: 100}

        Args:
            path: Path to the YAML file.

        Returns:
            Configured MAUTScorer with weights validated.

        Raises:
            ValueError: If required fields are missing, an unknown value
                function is named, params are invalid, or weights are invalid.
            FileNotFoundError: If the path does not exist.
        """
        yaml_path = Path(path)
        with yaml_path.open() as f:
            doc = yaml.safe_load(f)

        if not isinstance(doc, dict) or "criteria" not in doc:
            raise ValueError("YAML must contain a top-level 'criteria' key")

        builtin_fns: dict[str, Callable[..., float]] = {
            "linear": vf.linear,
            "exponential": vf.exponential,
            "logarithmic": vf.logarithmic,
            "logistic": vf.logistic,
            "step": vf.step,
            "gaussian": vf.gaussian,
            "piecewise_linear": vf.piecewise_linear,
        }

        criteria: list[Criterion] = []
        for entry in doc["criteria"]:
            for required_key in ("name", "weight", "value_fn"):
                if required_key not in entry:
                    raise ValueError(
                        f"Criterion entry missing required field '{required_key}': {entry}"
                    )

            fn_name: str = entry["value_fn"]
            if fn_name not in builtin_fns:
                raise ValueError(
                    f"Unknown value_fn '{fn_name}'. "
                    f"Valid options: {sorted(builtin_fns)}"
                )

            params: dict = entry.get("params", {})
            bound_fn = functools.partial(builtin_fns[fn_name], **params)

            try:
                bound_fn(0.0)  # smoke-test the partial binding
            except TypeError as e:
                raise ValueError(
                    f"Invalid params for criterion '{entry['name']}' "
                    f"with value_fn '{fn_name}': {e}"
                ) from e

            criteria.append(
                Criterion(
                    name=entry["name"],
                    weight=float(entry["weight"]),
                    value_fn=bound_fn,
                )
            )

        scorer = cls(criteria)
        scorer.validate_weights()
        return scorer

    @classmethod
    def from_weights(
        cls,
        weights_df: "pd.DataFrame",
        value_fns: dict[str, Callable[[float], float]],
        method: str = "SMARTER",
    ) -> "MAUTScorer":
        """Build a MAUTScorer from generate_weights() output.

        Args:
            weights_df: DataFrame from weights.generate_weights() with columns
                including the named method. Index contains attribute names.
            value_fns: Mapping of attribute name (DataFrame index) to value function.
            method: Column name to use for weights. Defaults to "SMARTER".

        Returns:
            Configured MAUTScorer with weights from the specified method.

        Raises:
            ValueError: If method column doesn't exist, or value_fns doesn't
                cover all attributes.
        """
        try:
            import pandas as pd  # noqa: F401 — guard-import; pandas is optional
        except ImportError:
            raise ImportError(
                "pandas is required for from_weights(). "
                "Install it with: pip install -e '.[excel]'"
            )

        if method not in weights_df.columns:
            raise ValueError(
                f"Method column '{method}' not found in weights_df. "
                f"Available columns: {list(weights_df.columns)}"
            )

        attribute_names = list(weights_df.index)
        missing_fns = [name for name in attribute_names if name not in value_fns]
        if missing_fns:
            raise ValueError(
                f"value_fns is missing entries for attributes: {missing_fns}"
            )

        criteria = [
            Criterion(
                name=name,
                weight=float(weights_df.loc[name, method]),
                value_fn=value_fns[name],
            )
            for name in attribute_names
        ]

        scorer = cls(criteria)
        scorer.validate_weights()
        return scorer


def dominance_check(results: list[DecisionResult]) -> list[tuple[str, str]]:
    """Find dominated alternatives (weight-independent).

    Alternative A dominates B if A's raw utility >= B's raw utility on
    every criterion and strictly > on at least one.

    Args:
        results: List of DecisionResult (must have raw_utilities populated).

    Returns:
        List of (dominator, dominated) tuples. Empty if no dominance found.
    """
    dominated_pairs: list[tuple[str, str]] = []

    for i, a in enumerate(results):
        for j, b in enumerate(results):
            if i == j:
                continue
            criteria_keys = set(a.raw_utilities.keys()) & set(b.raw_utilities.keys())
            if not criteria_keys:
                continue
            all_ge = all(a.raw_utilities[k] >= b.raw_utilities[k] for k in criteria_keys)
            any_gt = any(a.raw_utilities[k] > b.raw_utilities[k] for k in criteria_keys)
            if all_ge and any_gt:
                dominated_pairs.append((a.alternative, b.alternative))

    return dominated_pairs
