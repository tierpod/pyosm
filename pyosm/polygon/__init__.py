#!/usr/bin/python
"""A list of the LatLong points can be grouped to closed Polygon object. You can check if LatLong
point inside this polygon or not (using ray-casting algorithm).
"""

from pyosm.polygon import raycasting


class Polygon(object):
    """Polygon contains a list of LatLong points.
    """

    def __init__(self, points):
        self._points = points

    def __str__(self):
        return "{}".format(self._points)

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


class Region(object):
    """Region contains a list of Polygon."""

    def __init__(self, polygons):
        self._polygons = polygons

    def __len__(self):
        return len(self._polygons)

    def __str__(self):
        return "{}".format(self._polygons)

    def __contains__(self, item):
        """Returns True if LatLong item inside region.
        """

        for polygon in self._polygons:
            if item in polygon:
                return True

        return False
