#!/usr/bin/python
"""Contains functions for converting point coordinates.
"""

import math
from collections import namedtuple

# LatLong represents latitude and longtitude (float) coordinates.
LatLong = namedtuple("LatLong", "lat, long")
# ZXY represents point with z, x, y (int) coordinates.
ZXY = namedtuple("ZXY", "z, x, y")

Point = namedtuple("Point", "x, y")


def zxy_to_latlong(z, x, y):
    """Takes z, x, y and convert to LatLong (float values rounded to 4 digits).

    >>> from pygeopoint.convert import zxy_to_latlong
    >>> print(zxy_to_latlong(10, 697, 321))
    LatLong(lat=55.5783, long=65.0391)
    """

    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return LatLong(round(lat_deg, 4), round(lon_deg, 4))


def latlong_to_zxy(lat, lng, zoom):
    """Takes lat, lng, zoom and convert to ZXY.

    >>> from pygeopoint.convert import latlong_to_zxy
    >>> print(latlong_to_zxy(55.5783, 65.0391, 10))
    ZXY(z=10, x=697, y=321)
    """

    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lng + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return ZXY(zoom, x, y)
