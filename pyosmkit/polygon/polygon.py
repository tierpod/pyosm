#!/usr/bin/python
"""Provides Polygon object.
"""


from pyosmkit.polygon import raycasting


class Polygon(object):
    """Polygon contains a list of LatLong points.
    """

    def __init__(self, points):
        self._points = points

    def __str__(self):
        return "{0}".format(self._points)

    def __len__(self):
        return len(self._points)

    def __contains__(self, item):
        """Returns True if LatLong item inside polygon.
        """

        # too few points for polygon
        if len(self) < 3:
            return False

        # if polygon is not closed, add last point to the start
        if self._points[0] != self._points[-1]:
            self._points.insert(0, self._points[-1])

        return raycasting.is_point_inside(item, self._points)
