"""Tests for decision_science.value_functions."""

import math

import pytest

from src.myproject.decision_science.value_functions import (
    exponential,
    gaussian,
    linear,
    logarithmic,
    logistic,
    piecewise_linear,
    step,
)


class TestLinear:
    def test_low_maps_to_zero(self):
        assert linear(0.0, low=0.0, high=10.0) == pytest.approx(0.0)

    def test_high_maps_to_one(self):
        assert linear(10.0, low=0.0, high=10.0) == pytest.approx(1.0)

    def test_midpoint(self):
        assert linear(5.0, low=0.0, high=10.0) == pytest.approx(0.5)

    def test_clamp_below(self):
        assert linear(-5.0, low=0.0, high=10.0) == pytest.approx(0.0)

    def test_clamp_above(self):
        assert linear(15.0, low=0.0, high=10.0) == pytest.approx(1.0)

    def test_inverted_scale(self):
        # low > high: higher raw = lower utility
        assert linear(0.0, low=10.0, high=0.0) == pytest.approx(1.0)
        assert linear(10.0, low=10.0, high=0.0) == pytest.approx(0.0)
        assert linear(5.0, low=10.0, high=0.0) == pytest.approx(0.5)

    def test_default_range(self):
        assert linear(0.5) == pytest.approx(0.5)

    def test_equal_low_high_raises(self):
        with pytest.raises(ValueError):
            linear(5.0, low=3.0, high=3.0)

    def test_output_always_in_unit_interval(self):
        for x in [-100, 0, 50, 100, 200]:
            result = linear(float(x), low=0.0, high=100.0)
            assert 0.0 <= result <= 1.0


class TestExponential:
    def test_low_maps_to_zero(self):
        assert exponential(0.0, low=0.0, high=1.0, rate=1.0) == pytest.approx(0.0)

    def test_high_maps_to_one(self):
        assert exponential(1.0, low=0.0, high=1.0, rate=1.0) == pytest.approx(1.0)

    def test_concave_shape_midpoint_above_half(self):
        # Concave (rate > 0): midpoint utility > 0.5
        mid = exponential(0.5, low=0.0, high=1.0, rate=2.0)
        assert mid > 0.5

    def test_convex_shape_midpoint_below_half(self):
        # Convex (rate < 0): midpoint utility < 0.5
        mid = exponential(0.5, low=0.0, high=1.0, rate=-2.0)
        assert mid < 0.5

    def test_clamps_below(self):
        result = exponential(-1.0, low=0.0, high=1.0, rate=1.0)
        assert result == pytest.approx(0.0)

    def test_clamps_above(self):
        result = exponential(2.0, low=0.0, high=1.0, rate=1.0)
        assert result == pytest.approx(1.0)

    def test_zero_rate_raises(self):
        with pytest.raises(ValueError):
            exponential(0.5, low=0.0, high=1.0, rate=0.0)

    def test_equal_low_high_raises(self):
        with pytest.raises(ValueError):
            exponential(0.5, low=2.0, high=2.0)

    def test_output_in_unit_interval(self):
        for x in [0.0, 0.25, 0.5, 0.75, 1.0]:
            assert 0.0 <= exponential(x, low=0.0, high=1.0, rate=3.0) <= 1.0

    def test_overflow_extreme_rate_does_not_crash(self):
        # rate=-800 is a very large exponent; must not raise OverflowError.
        result = exponential(0.5, 0, 1, rate=-800)
        assert 0.0 <= result <= 1.0


class TestLogarithmic:
    def test_low_maps_to_zero(self):
        assert logarithmic(0.0, low=0.0, high=100.0) == pytest.approx(0.0)

    def test_high_maps_to_one(self):
        assert logarithmic(100.0, low=0.0, high=100.0) == pytest.approx(1.0)

    def test_diminishing_returns(self):
        # Gain from 0-50 should exceed gain from 50-100
        gain_first_half = logarithmic(50.0, low=0.0, high=100.0) - logarithmic(0.0, low=0.0, high=100.0)
        gain_second_half = logarithmic(100.0, low=0.0, high=100.0) - logarithmic(50.0, low=0.0, high=100.0)
        assert gain_first_half > gain_second_half

    def test_clamp_below(self):
        assert logarithmic(-10.0, low=0.0, high=100.0) == pytest.approx(0.0)

    def test_clamp_above(self):
        assert logarithmic(200.0, low=0.0, high=100.0) == pytest.approx(1.0)

    def test_equal_low_high_raises(self):
        with pytest.raises(ValueError):
            logarithmic(5.0, low=3.0, high=3.0)

    def test_output_in_unit_interval(self):
        for x in [0, 10, 50, 90, 100]:
            result = logarithmic(float(x), low=0.0, high=100.0)
            assert 0.0 <= result <= 1.0


class TestLogistic:
    def test_midpoint_returns_half(self):
        assert logistic(0.5, midpoint=0.5) == pytest.approx(0.5)

    def test_above_midpoint_above_half(self):
        assert logistic(0.9, midpoint=0.5, steepness=5.0) > 0.5

    def test_below_midpoint_below_half(self):
        assert logistic(0.1, midpoint=0.5, steepness=5.0) < 0.5

    def test_high_steepness_approaches_step(self):
        high = logistic(1.0, midpoint=0.5, steepness=100.0)
        low = logistic(0.0, midpoint=0.5, steepness=100.0)
        assert high > 0.999
        assert low < 0.001

    def test_zero_steepness_raises(self):
        with pytest.raises(ValueError):
            logistic(0.5, midpoint=0.5, steepness=0.0)

    def test_output_in_open_unit_interval(self):
        for x in [-10.0, 0.0, 0.5, 1.0, 10.0]:
            result = logistic(x, midpoint=0.5, steepness=2.0)
            assert 0.0 < result < 1.0

    def test_overflow_large_positive_exponent_returns_zero(self):
        # steepness=1000 on x far below midpoint: z > 700 → result ≈ 0
        result = logistic(49, 50, 1000)
        assert result == pytest.approx(0.0)

    def test_overflow_large_negative_exponent_returns_one(self):
        # steepness=1000 on x far above midpoint: z < -700 → result ≈ 1
        result = logistic(51, 50, 1000)
        assert result == pytest.approx(1.0)

    def test_overflow_does_not_crash(self):
        # No OverflowError raised for extreme inputs.
        result = logistic(49, 50, 1000)
        assert 0.0 <= result <= 1.0


class TestStep:
    def test_at_threshold_returns_above(self):
        assert step(5.0, threshold=5.0) == pytest.approx(1.0)

    def test_above_threshold_returns_above(self):
        assert step(6.0, threshold=5.0) == pytest.approx(1.0)

    def test_below_threshold_returns_below(self):
        assert step(4.0, threshold=5.0) == pytest.approx(0.0)

    def test_custom_below_above(self):
        assert step(3.0, threshold=5.0, below=0.2, above=0.8) == pytest.approx(0.2)
        assert step(7.0, threshold=5.0, below=0.2, above=0.8) == pytest.approx(0.8)

    def test_invalid_below_raises(self):
        with pytest.raises(ValueError):
            step(1.0, threshold=5.0, below=-0.1)

    def test_invalid_above_raises(self):
        with pytest.raises(ValueError):
            step(1.0, threshold=5.0, above=1.5)


class TestGaussian:
    def test_center_returns_one(self):
        assert gaussian(0.0, center=0.0, sigma=1.0) == pytest.approx(1.0)

    def test_symmetric_around_center(self):
        left = gaussian(-1.0, center=0.0, sigma=2.0)
        right = gaussian(1.0, center=0.0, sigma=2.0)
        assert left == pytest.approx(right)

    def test_falls_off_with_distance(self):
        near = gaussian(1.0, center=0.0, sigma=2.0)
        far = gaussian(3.0, center=0.0, sigma=2.0)
        assert near > far

    def test_one_sigma_value(self):
        # At x = center ± sigma, value = e^(-0.5) ≈ 0.6065
        result = gaussian(1.0, center=0.0, sigma=1.0)
        assert result == pytest.approx(math.exp(-0.5))

    def test_zero_sigma_raises(self):
        with pytest.raises(ValueError):
            gaussian(1.0, center=0.0, sigma=0.0)

    def test_output_in_unit_interval(self):
        for x in [-10, -1, 0, 1, 10]:
            result = gaussian(float(x), center=0.0, sigma=2.0)
            assert 0.0 < result <= 1.0


class TestPiecewiseLinear:
    _bp = [(0.0, 0.0), (50.0, 0.5), (100.0, 1.0)]

    def test_at_first_breakpoint(self):
        assert piecewise_linear(0.0, self._bp) == pytest.approx(0.0)

    def test_at_last_breakpoint(self):
        assert piecewise_linear(100.0, self._bp) == pytest.approx(1.0)

    def test_interpolation_midpoint(self):
        assert piecewise_linear(25.0, self._bp) == pytest.approx(0.25)

    def test_clamp_below_range(self):
        assert piecewise_linear(-10.0, self._bp) == pytest.approx(0.0)

    def test_clamp_above_range(self):
        assert piecewise_linear(200.0, self._bp) == pytest.approx(1.0)

    def test_unsorted_breakpoints_accepted(self):
        unsorted = [(100.0, 1.0), (0.0, 0.0), (50.0, 0.5)]
        assert piecewise_linear(25.0, unsorted) == pytest.approx(0.25)

    def test_nonlinear_shape(self):
        # Flat then steep
        bp = [(0.0, 0.0), (80.0, 0.1), (100.0, 1.0)]
        assert piecewise_linear(40.0, bp) == pytest.approx(0.05)
        assert piecewise_linear(90.0, bp) == pytest.approx(0.55)

    def test_fewer_than_two_breakpoints_raises(self):
        with pytest.raises(ValueError):
            piecewise_linear(1.0, [(0.0, 0.0)])

    def test_empty_breakpoints_raises(self):
        with pytest.raises(ValueError):
            piecewise_linear(1.0, [])

    def test_y_out_of_range_raises(self):
        with pytest.raises(ValueError):
            piecewise_linear(1.0, [(0.0, 0.0), (1.0, 1.5)])

    def test_output_in_unit_interval(self):
        for x in [0, 10, 25, 50, 75, 100]:
            result = piecewise_linear(float(x), self._bp)
            assert 0.0 <= result <= 1.0
