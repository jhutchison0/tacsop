"""Tests for math_utils module."""

import math

from src.myproject.utils.math_utils import nCr, nCk


class TestNCr:
    def test_basic(self):
        assert nCr(7, 5) == 21

    def test_symmetry(self):
        assert nCr(10, 3) == nCr(10, 7)

    def test_choose_zero(self):
        assert nCr(5, 0) == 1

    def test_choose_all(self):
        assert nCr(5, 5) == 1

    def test_matches_stdlib(self):
        assert nCr(20, 8) == math.comb(20, 8)


class TestNCk:
    def test_basic(self):
        assert nCk(7, 5) == 21

    def test_symmetry(self):
        assert nCk(10, 3) == nCk(10, 7)

    def test_choose_zero(self):
        assert nCk(5, 0) == 1

    def test_agrees_with_nCr(self):
        for n in range(1, 15):
            for k in range(n + 1):
                assert nCr(n, k) == nCk(n, k), f"Mismatch at n={n}, k={k}"
