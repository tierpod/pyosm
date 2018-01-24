#!/usr/bin/python
"""Contains basic points description and functions for converting between them.
"""

import math
from collections import namedtuple

# Point represents point with x, y (int) coordinates.
Point = namedtuple("Point", "x, y")
# LatLong represents latitude and longtitude (float) coordinates.
LatLong = namedtuple("LatLong", "lat, long")
# ZXY represents point with z, x, y (int) coordinates.
ZXY = namedtuple("ZXY", "z, x, y")


def zxy_to_latlong(z, x, y):
    """Takes z, x, y (int) and convert to LatLong (float values rounded to 4 digits).

    >>> from pyosm.point import zxy_to_latlong
    >>> print(zxy_to_latlong(10, 697, 321))
    LatLong(lat=55.5783, long=65.0391)
    """

    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return LatLong(round(lat_deg, 4), round(lon_deg, 4))


def latlong_to_zxy(lat, lng, zoom):
    """Takes lat, lng (float), zoom (int) and convert to ZXY.

    >>> from pyosm.point import latlong_to_zxy
    >>> print(latlong_to_zxy(55.5783, 65.0391, 10))
    ZXY(z=10, x=697, y=321)
    """

    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lng + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return ZXY(zoom, x, y)


class Bound(object):
    """Represents square bound of ZXY points.

    Args:
        z (int): zoom level
        min_x, max_x (int): minimum and maximum x coordinates
        min_y, max_y (int): minimum and maximym y coordinates
        flip_y (bool): flip y coordinate?
    """

    def __init__(self, z, min_x, max_x, min_y, max_y, flip_y=False):
        self.z = z
        self.min_x = min_x
        self.max_x = max_x
        if flip_y:
            self.min_y = flip_y_coord(z, min_y)
            self.max_y = flip_y_coord(z, max_y)
        else:
            self.min_y = min_y
            self.max_y = max_y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Bound(z:{} x:{}-{} y:{}-{})".format(self.z,
                                                    self.min_x, self.max_x,
                                                    self.min_y, self.max_y)

    def __contains__(self, item):
        """Returns True if item (point.ZXY) contains inside Bound.

        >>> bound = Bound(z=15, min_x=26248, max_x=26253, min_y=10821, max_y=10816)
        >>> print(ZXY(z=15, x=26248, y=10821) in bound)
        True
        >>> print(ZXY(z=15, x=26249, y=10822) in bound)
        True
        >>> print(ZXY(z=15, x=26247, y=10820) in bound)
        False
        """

        if item.z != self.z:
            return False

        if item.x < self.min_x and item.x > self.max_x:
            return False

        if item.y < self.min_y and item.y > self.max_y:
            return False

        return True


class Bounds(object):
    """Represends a list of Bound.
    """

    def __init__(self, bounds):
        """Args:
            bounds: list of Bound
        """

        self.bounds = bounds

    def __str__(self):
        return str(self.bounds)

    def for_zoom(self, z):
        """Return bound for given z (int). Raises ValueError if bound for given zoom does
        not exist in Bounds.
        """

        for bound in self.bounds:
            if bound.z == z:
                return bound

        raise ValueError("bound for given zoom not found")

    def __contains__(self, item):
        """Returns True if item (point.ZXY) inside Bounds.

        >>> bounds = Bounds([
        ...     Bound(z=12, min_x=3281, max_x=3281, min_y=1352, max_y=1352),
        ...     Bound(z=15, min_x=26248, max_x=26253, min_y=10821, max_y=10816),
        ... ])
        >>> print(ZXY(z=12, x=3281, y=1352) in bounds)
        True
        >>> print(ZXY(z=15, x=26249, y=10822) in bounds)
        True
        >>> print(ZXY(z=15, x=26247, y=10820) in bounds)
        False
        """

        for bound in self.bounds:
            if item in bound:
                return True

        return False


def flip_y_coord(zoom, y):
    """Flips y (int) coordinate for given zoom (int)."""

    return (2**zoom-1) - y
