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

    >>> from pyosmkit.point import zxy_to_latlong
    >>> zxy_to_latlong(10, 697, 321)
    LatLong(lat=55.5783, long=65.0391)
    """

    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return LatLong(round(lat_deg, 4), round(lon_deg, 4))


def latlong_to_zxy(lat, lng, zoom):
    """Takes lat, lng (float), zoom (int) and convert to ZXY.

    >>> from pyosmkit.point import latlong_to_zxy
    >>> latlong_to_zxy(55.5783, 65.0391, 10)
    ZXY(z=10, x=697, y=321)
    """

    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lng + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return ZXY(zoom, x, y)


def str_to_range(s, delim=":", output=float):
    """Converts string `s` like "S1:S2" to pair (S1, S2) (S1 and S2 has type `output`).

    >>> str_to_range("10")
    (10.0, 10.0)
    >>> str_to_range("10:20")
    (10.0, 20.0)
    >>> str_to_range("20:10", output=int)
    (10, 20)
    >>> str_to_range("10:20:30")
    Traceback (most recent call last):
    ...
    ValueError: wrong range value
    """

    items = s.split(delim)

    if len(items) == 1:
        items = [items[0], items[0]]

    if len(items) != 2:
        raise ValueError("wrong range value")

    items = [output(i) for i in items]
    return min(items), max(items)


class Bound(object):
    """Represents square bound of ZXY points.

    Args:
        z (int): zoom level
        min_x, max_x (int): minimum and maximum x coordinates
        min_y, max_y (int): minimum and maximym y coordinates
    """

    def __init__(self, z, min_x, max_x, min_y, max_y):
        self.z = z
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Bound(z:{z} x:{min_x}-{max_x} y:{min_y}-{max_y})".format(**self.__dict__)

    def __contains__(self, item):
        """Returns True if item (point.ZXY) contains inside Bound.

        >>> bound = Bound(z=15, min_x=26248, max_x=26253, min_y=10816, max_y=10821)
        >>> ZXY(z=15, x=26248, y=10821) in bound
        True
        >>> ZXY(z=15, x=26249, y=10817) in bound
        True
        >>> ZXY(z=15, x=26247, y=10820) in bound
        False
        >>> bound = Bound(z=1, min_x=1, max_x=1, min_y=0, max_y=0)
        >>> ZXY(z=1, x=2, y=3) in bound
        False
        """

        if item.z != self.z:
            return False

        if item.x < self.min_x or item.x > self.max_x:
            return False

        if item.y < self.min_y or item.y > self.max_y:
            return False

        return True

    def points(self):
        """Returns generator of ZXY points inside Bound.

        >>> bound = Bound(z=4, min_x=9, max_x=10, min_y=6, max_y=6)
        >>> for b in bound.points():
        ...     print(b)
        ZXY(z=4, x=9, y=6)
        ZXY(z=4, x=10, y=6)
        """

        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                yield ZXY(z=self.z, x=x, y=y)

    @classmethod
    def from_latlong_bound(cls, b):
        """Creates Bound from LatLongBound.

        >>> ll_bound = LatLongBound(10, 55.6992, 55.2031, 64.9662, 66.3121)
        >>> bound = Bound.from_latlong_bound(ll_bound)
        >>> print(bound)
        Bound(z:10 x:696-700 y:320-322)
        """

        p_start = latlong_to_zxy(lat=b.start_ll.lat, lng=b.start_ll.long, zoom=b.z)
        p_end = latlong_to_zxy(lat=b.end_ll.lat, lng=b.end_ll.long, zoom=b.z)
        return cls(z=b.z, min_x=p_start.x, max_x=p_end.x, min_y=p_start.y, max_y=p_end.y)


class Bounds(object):
    """Represends a list of Bound.
    """

    def __init__(self, bounds):
        """Args:
            bounds: list of Bound
        """

        self.bounds = bounds

    def __repr__(self):
        return self.__str__()

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
        ...     Bound(z=15, min_x=26248, max_x=26253, min_y=10816, max_y=10821),
        ... ])
        >>> ZXY(z=12, x=3281, y=1352) in bounds
        True
        >>> ZXY(z=15, x=26248, y=10821) in bounds
        True
        >>> ZXY(z=15, x=26247, y=10820) in bounds
        False
        >>> for b in bounds:
        ...     print(b)
        Bound(z:12 x:3281-3281 y:1352-1352)
        Bound(z:15 x:26248-26253 y:10816-10821)
        """

        for bound in self.bounds:
            if item in bound:
                return True

        return False

    def __iter__(self):
        return iter(self.bounds)

    def __next__(self):
        return self.next()

    def next(self):
        return next(self)

    def append(self, bound):
        """Append bound (Bound) to Bounds."""

        self.bounds.append(bound)

    def points(self):
        """"Returns generator of ZXY points inside Bounds."""

        for bound in self.bounds:
            for point in bound.points():
                yield point


class LatLongBound(object):
    """Represents square bound of LatLongs.

    Args:
        lat1, lat2 (float): pair of latitude coordinates
        lng1, lng2 (float): pair of langtitude coordinates
        start_ll (LatLong): start point of bound
        end_ll (LatLong): end point of bound
    """

    def __init__(self, z, lat1, lat2, lng1, lng2):
        """
        >>> ll_bound = LatLongBound(10, 55.6992, 55.2031, 64.9662, 66.3121)
        >>> print(ll_bound)
        LatLongBound(z:10 LatLong(lat=55.6992, long=64.9662)-LatLong(lat=55.2031, long=66.3121)
        >>> ll_bound = LatLongBound(10, 55.2031, 55.6992, 66.3121, 64.9662)
        >>> print(ll_bound)
        LatLongBound(z:10 LatLong(lat=55.6992, long=64.9662)-LatLong(lat=55.2031, long=66.3121)
        """

        self.z = z
        start_lat = max(lat1, lat2)
        start_lng = min(lng1, lng2)
        end_lat = min(lat1, lat2)
        end_lng = max(lng1, lng2)
        self.start_ll = LatLong(lat=start_lat, long=start_lng)
        self.end_ll = LatLong(lat=end_lat, long=end_lng)

    def __str__(self):
        return "LatLongBound(z:{z} {start_ll}-{end_ll}".format(**self.__dict__)
