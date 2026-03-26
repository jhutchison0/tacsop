"""MAUTScorer: additive multi-attribute utility aggregation."""

import functools
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
    """

    alternative: str
    utility: float
    breakdown: dict[str, float] = field(default_factory=dict)


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
            ValueError: If weights are invalid or a criterion name is missing
                from raw_scores.
        """
        self.validate_weights()

        missing = [c.name for c in self._criteria if c.name not in raw_scores]
        if missing:
            raise ValueError(
                f"raw_scores is missing criterion values: {missing}"
            )

        breakdown: dict[str, float] = {}
        for c in self._criteria:
            u = c.value_fn(raw_scores[c.name])
            breakdown[c.name] = c.weight * u

        return DecisionResult(
            alternative=alternative,
            utility=sum(breakdown.values()),
            breakdown=breakdown,
        )

    def rank(
        self, alternatives: dict[str, dict[str, float]]
    ) -> list[DecisionResult]:
        """Score and rank all alternatives, highest utility first.

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
                function is named, or weights are invalid.
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
