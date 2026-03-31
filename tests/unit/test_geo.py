"""Tests for src/myproject/utils/geo.py."""

import math

import pytest

from src.myproject.utils.geo import EARTH_RADIUS_KM, get_bearing, get_distance


class TestGetDistance:
    def test_new_york_to_london(self):
        dist = get_distance(40.7128, -74.0060, 51.5074, -0.1278)
        assert dist == pytest.approx(5570, abs=20)

    def test_sydney_to_tokyo(self):
        dist = get_distance(-33.8688, 151.2093, 35.6762, 139.6503)
        assert dist == pytest.approx(7823, abs=30)

    def test_same_point_returns_zero(self):
        assert get_distance(40.7128, -74.0060, 40.7128, -74.0060) == 0.0

    def test_antipodal_points(self):
        half_circumference = math.pi * EARTH_RADIUS_KM
        dist = get_distance(90, 0, -90, 0)
        assert dist == pytest.approx(half_circumference, abs=1)

    def test_symmetry(self):
        d1 = get_distance(40.7128, -74.0060, 51.5074, -0.1278)
        d2 = get_distance(51.5074, -0.1278, 40.7128, -74.0060)
        assert d1 == d2

    def test_quarter_circumference_on_equator(self):
        quarter = 2 * math.pi * EARTH_RADIUS_KM / 4
        dist = get_distance(0, 0, 0, 90)
        assert dist == pytest.approx(quarter, abs=5)


class TestGetBearing:
    def test_due_north(self):
        bearing = get_bearing(0, 0, 10, 0)
        assert bearing == pytest.approx(0.0, abs=0.1)

    def test_due_east_on_equator(self):
        bearing = get_bearing(0, 0, 0, 10)
        assert bearing == pytest.approx(90.0, abs=0.1)

    def test_new_york_to_london(self):
        bearing = get_bearing(40.7128, -74.0060, 51.5074, -0.1278)
        assert bearing == pytest.approx(51, abs=2)

    def test_same_point(self):
        assert get_bearing(40.7128, -74.0060, 40.7128, -74.0060) == 0.0
