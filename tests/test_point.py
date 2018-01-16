#!/usr/bin/python

import pytest
import context  # noqa: F401
from pyosm import LatLong, ZXY, zxy_to_latlong, latlong_to_zxy


@pytest.mark.parametrize("z,x,y,expected", [
    (10, 697, 321, LatLong(55.5783, 65.0391))
])
def test_zxy_to_latlong(z, x, y, expected):
    assert zxy_to_latlong(z, x, y) == expected


@pytest.mark.parametrize("lat,lng,expected", [
    (55.5783, 65.0391, ZXY(10, 697, 321))
])
def test_latlong_to_zxy(lat, lng, expected):
    assert latlong_to_zxy(lat, lng, 10) == expected
