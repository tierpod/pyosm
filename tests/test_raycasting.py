#!/usr/bin/python

import pytest
import context  # noqa: F401

from pyosm.point import LatLong
from pyosm.polygon.raycasting import ray_intersect_seg, is_point_inside


@pytest.mark.parametrize("p,a,b,expected", [
    (LatLong(1, 1), LatLong(0, 3), LatLong(3, 0), True),
    (LatLong(1, 1), LatLong(3.3, 0), LatLong(0, 3.3), True),
    (LatLong(1, 1), LatLong(0.5, 0), LatLong(0.5, 10), False)
])
def test_ray_intersect_seg(p, a, b, expected):
    assert ray_intersect_seg(p, a, b) == expected


def test_is_point_inside_few_points():
    p = LatLong(0, 0)
    poly = [LatLong(0, 0)]
    assert not is_point_inside(p, poly)


@pytest.mark.parametrize("p,expected", [
    (LatLong(1, 1), True),
    (LatLong(11, 11), False),
])
def test_is_point_inside_virtual_closed_polygon(p, expected):
    poly = [LatLong(0, 0), LatLong(10, 0), LatLong(10, 10), LatLong(0, 10), LatLong(0, 0)]
    assert is_point_inside(p, poly) == expected


@pytest.mark.parametrize("p,expected", [
    (LatLong(1, 1), True),
    (LatLong(11, 11), False),
])
def test_is_point_inside_virtual_not_closed_polygon(p, expected):
    poly = [LatLong(0, 0), LatLong(10, 0), LatLong(10, 10), LatLong(0, 10)]
    assert is_point_inside(p, poly) == expected


@pytest.mark.parametrize("p,expected", [
    # inside points
    (LatLong(55.4879, 65.2337), True),  # 12 2790 1285
    (LatLong(55.4416, 65.3003), True),  # 12 2790 1286
    (LatLong(55.4753, 65.3614), True),  # 12 2791 1286
    (LatLong(55.4953, 65.3775), True),  # 12 2791 1285
    (LatLong(55.4732, 65.3181), True),  # 12 2791 1286
    # outside points
    (LatLong(55.5340, 65.3116), False),
    (LatLong(55.4327, 65.1952), False),
    (LatLong(55.4250, 65.4812), False),
])
def test_is_point_inside_real_polygon(p, expected):
    poly = [LatLong(55.4903, 65.2110), LatLong(55.4066, 65.2275),
            LatLong(55.4329, 65.3573), LatLong(55.4969, 65.3878),
            LatLong(55.5169, 65.3113), LatLong(55.4903, 65.2110)]
    assert is_point_inside(p, poly) == expected
