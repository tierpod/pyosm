#!/usr/bin/python
"""Provides Region object.
"""


class Region(object):
    """Region contains a list of pyosmkit.polygon.Polygon."""

    def __init__(self, polygons):
        self._polygons = polygons

    def __len__(self):
        return len(self._polygons)

    def __str__(self):
        return "{0}".format(self._polygons)

    def __contains__(self, item):
        """Returns True if LatLong item inside region.
        """

        for polygon in self._polygons:
            if item in polygon:
                return True

        return False
