#!/usr/bin/python
"""Implements ray-casting algorithm http://rosettacode.org/wiki/Ray-casting_algorithm#Python for
polygon with LatLong coordinates.
"""


# lat=x, long=y
def ray_intersect_seg(p, a, b):
    """Checks if points p (LatLong) intersect edge with points a, b (LatLong). Returns bool.
    """

    return (a.long > p.long) != (b.long > p.long) and \
        p.lat < (b.lat - a.lat) * (p.long - a.long) / (b.long - a.long) + a.lat


def is_point_inside(p, poly):
    """Checks if point p (LatLong) inside closed poly (list of points LatLong). Returns bool.
    """

    if len(poly) < 3:
        return False

    inside = ray_intersect_seg(p, poly[-1], poly[0])

    for i in range(1, len(poly)):
        if ray_intersect_seg(p, poly[i-1], poly[i]):
            inside = not inside

    return inside
