"""Combinatorics utilities.

Note: Python 3.8+ provides ``math.comb(n, k)`` in the standard library.
These functions are kept for educational reference and backwards compatibility.
"""

import math
from fractions import Fraction
from functools import reduce
from operator import mul


def nCr(n: int, r: int) -> int:
    """Compute n-choose-r using factorials.

    Args:
        n: Total number of items.
        r: Number of items to choose.

    Returns:
        Number of combinations.
    """
    f = math.factorial
    return f(n) // f(r) // f(n - r)


def nCk(n: int, k: int) -> int:
    """Compute n-choose-k using multiplicative formula (avoids large intermediates).

    Args:
        n: Total number of items.
        k: Number of items to choose.

    Returns:
        Number of combinations.
    """
    return int(reduce(mul, (Fraction(n - i, i + 1) for i in range(k)), 1))
