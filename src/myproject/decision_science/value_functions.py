"""Value functions for MAUT: map raw attribute scores to utility in [0, 1]."""

import math


def linear(x: float, low: float = 0.0, high: float = 1.0) -> float:
    """Normalize x from [low, high] to [0, 1], clamped.

    When low > high, higher raw values produce lower utility (inverted scale).

    Args:
        x: Raw input value.
        low: Raw value corresponding to utility 0 (or 1 when inverted).
        high: Raw value corresponding to utility 1 (or 0 when inverted).

    Returns:
        Utility in [0, 1].

    Raises:
        ValueError: If low == high.
    """
    if low == high:
        raise ValueError(f"low and high must differ; got low={low}, high={high}")
    return max(0.0, min(1.0, (x - low) / (high - low)))


def exponential(x: float, low: float, high: float, rate: float = 1.0) -> float:
    """Exponential value function with diminishing or increasing returns.

    Formula: (1 - e^(-rate*t)) / (1 - e^(-rate)) where t = (x - low) / (high - low).
    rate > 0: concave (diminishing returns).
    rate < 0: convex (increasing returns).

    Args:
        x: Raw input value.
        low: Raw value mapped to utility 0.
        high: Raw value mapped to utility 1.
        rate: Shape parameter; nonzero. Defaults to 1.0.

    Returns:
        Utility in [0, 1].

    Raises:
        ValueError: If low == high or rate == 0.
    """
    if low == high:
        raise ValueError(f"low and high must differ; got low={low}, high={high}")
    if rate == 0.0:
        raise ValueError("rate must be nonzero; use linear() for rate=0 behavior")

    t = max(0.0, min(1.0, (x - low) / (high - low)))
    # Clamp exponents to avoid OverflowError for extreme rate values.
    exp_t = 0.0 if -rate * t < -700 else (1e308 if -rate * t > 700 else math.exp(-rate * t))
    exp_1 = 0.0 if -rate < -700 else (1e308 if -rate > 700 else math.exp(-rate))
    return (1.0 - exp_t) / (1.0 - exp_1)


def logarithmic(x: float, low: float, high: float) -> float:
    """Logarithmic value function with diminishing marginal returns.

    Formula: ln(1 + c*t) / ln(1 + c) where t = (x - low) / (high - low), c = 9.

    Args:
        x: Raw input value.
        low: Raw value mapped to utility 0.
        high: Raw value mapped to utility 1.

    Returns:
        Utility in [0, 1].

    Raises:
        ValueError: If low == high.
    """
    if low == high:
        raise ValueError(f"low and high must differ; got low={low}, high={high}")

    _C = 9.0
    t = max(0.0, min(1.0, (x - low) / (high - low)))
    return math.log(1.0 + _C * t) / math.log(1.0 + _C)


def logistic(x: float, midpoint: float, steepness: float = 1.0) -> float:
    """Logistic S-curve value function.

    Formula: 1 / (1 + e^(-steepness*(x - midpoint))).
    Output approaches 0 and 1 asymptotically; not clamped.

    Args:
        x: Raw input value.
        midpoint: x value at which utility = 0.5.
        steepness: Controls slope at midpoint. Defaults to 1.0.

    Returns:
        Utility in (0, 1) open interval.

    Raises:
        ValueError: If steepness == 0.
    """
    if steepness == 0.0:
        raise ValueError("steepness must be nonzero")
    z = -steepness * (x - midpoint)
    if z > 700:
        return 0.0  # e^700 overflows; 1/(1+huge) ≈ 0
    if z < -700:
        return 1.0  # 1/(1+tiny) ≈ 1
    return 1.0 / (1.0 + math.exp(z))


def step(
    x: float, threshold: float, below: float = 0.0, above: float = 1.0
) -> float:
    """Binary step value function.

    Args:
        x: Raw input value.
        threshold: Value at which the step occurs. At or above yields `above`.
        below: Utility returned when x < threshold. Defaults to 0.0.
        above: Utility returned when x >= threshold. Defaults to 1.0.

    Returns:
        Utility equal to `below` or `above`.

    Raises:
        ValueError: If below or above are outside [0, 1].
    """
    if not (0.0 <= below <= 1.0):
        raise ValueError(f"below must be in [0, 1]; got {below}")
    if not (0.0 <= above <= 1.0):
        raise ValueError(f"above must be in [0, 1]; got {above}")
    return above if x >= threshold else below


def gaussian(x: float, center: float, sigma: float) -> float:
    """Gaussian (bell-curve) value function, peaked at center.

    Formula: e^(-((x - center)^2) / (2*sigma^2)).

    Args:
        x: Raw input value.
        center: x value with maximum utility (1.0).
        sigma: Standard deviation; controls width of peak.

    Returns:
        Utility in (0, 1].

    Raises:
        ValueError: If sigma == 0.
    """
    if sigma == 0.0:
        raise ValueError("sigma must be nonzero")
    return math.exp(-((x - center) ** 2) / (2.0 * sigma**2))


def piecewise_linear(x: float, breakpoints: list[tuple[float, float]]) -> float:
    """Piecewise linear value function interpolated between breakpoints.

    Clamps to the first/last y value outside the breakpoint range.

    Args:
        x: Raw input value.
        breakpoints: List of (x, y) pairs defining the function. Must have at
            least two points. Sorted by x ascending internally.

    Returns:
        Interpolated utility, clamped at endpoints.

    Raises:
        ValueError: If fewer than 2 breakpoints are provided or any y is outside [0, 1].
    """
    if len(breakpoints) < 2:
        raise ValueError(
            f"piecewise_linear requires at least 2 breakpoints; got {len(breakpoints)}"
        )

    pts = sorted(breakpoints, key=lambda p: p[0])

    for _x, y in pts:
        if not (0.0 <= y <= 1.0):
            raise ValueError(f"All breakpoint y-values must be in [0, 1]; got {y}")

    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]

    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)

    return pts[-1][1]
