#!/usr/bin/python

import context  # noqa: F401
from pyosm import Point
from pyosm.metatile.filelike import Entry


test_file = "tests/data/0.meta"

test_index = {
    Point(x=0, y=0): Entry(offset=532, size=25093),
    Point(x=0, y=1): Entry(offset=25625, size=11330),
    Point(x=0, y=2): Entry(offset=36955, size=0),
    Point(x=0, y=3): Entry(offset=36955, size=0),
    Point(x=0, y=4): Entry(offset=36955, size=0),
    Point(x=0, y=5): Entry(offset=36955, size=0),
    Point(x=0, y=6): Entry(offset=36955, size=0),
    Point(x=0, y=7): Entry(offset=36955, size=0),
    Point(x=1, y=0): Entry(offset=36955, size=26298),
    Point(x=1, y=1): Entry(offset=63253, size=10439),
    Point(x=1, y=2): Entry(offset=73692, size=0),
    Point(x=1, y=3): Entry(offset=73692, size=0),
    Point(x=1, y=4): Entry(offset=73692, size=0),
    Point(x=1, y=5): Entry(offset=73692, size=0),
    Point(x=1, y=6): Entry(offset=73692, size=0),
    Point(x=1, y=7): Entry(offset=73692, size=0),
    Point(x=2, y=0): Entry(offset=73692, size=0),
    Point(x=2, y=1): Entry(offset=73692, size=0),
    Point(x=2, y=2): Entry(offset=73692, size=0),
    Point(x=2, y=3): Entry(offset=73692, size=0),
    Point(x=2, y=4): Entry(offset=73692, size=0),
    Point(x=2, y=5): Entry(offset=73692, size=0),
    Point(x=2, y=6): Entry(offset=73692, size=0),
    Point(x=2, y=7): Entry(offset=73692, size=0),
    Point(x=3, y=0): Entry(offset=73692, size=0),
    Point(x=3, y=1): Entry(offset=73692, size=0),
    Point(x=3, y=2): Entry(offset=73692, size=0),
    Point(x=3, y=3): Entry(offset=73692, size=0),
    Point(x=3, y=4): Entry(offset=73692, size=0),
    Point(x=3, y=5): Entry(offset=73692, size=0),
    Point(x=3, y=6): Entry(offset=73692, size=0),
    Point(x=3, y=7): Entry(offset=73692, size=0),
    Point(x=4, y=0): Entry(offset=73692, size=0),
    Point(x=4, y=1): Entry(offset=73692, size=0),
    Point(x=4, y=2): Entry(offset=73692, size=0),
    Point(x=4, y=3): Entry(offset=73692, size=0),
    Point(x=4, y=4): Entry(offset=73692, size=0),
    Point(x=4, y=5): Entry(offset=73692, size=0),
    Point(x=4, y=6): Entry(offset=73692, size=0),
    Point(x=4, y=7): Entry(offset=73692, size=0),
    Point(x=5, y=0): Entry(offset=73692, size=0),
    Point(x=5, y=1): Entry(offset=73692, size=0),
    Point(x=5, y=2): Entry(offset=73692, size=0),
    Point(x=5, y=3): Entry(offset=73692, size=0),
    Point(x=5, y=4): Entry(offset=73692, size=0),
    Point(x=5, y=5): Entry(offset=73692, size=0),
    Point(x=5, y=6): Entry(offset=73692, size=0),
    Point(x=5, y=7): Entry(offset=73692, size=0),
    Point(x=6, y=0): Entry(offset=73692, size=0),
    Point(x=6, y=1): Entry(offset=73692, size=0),
    Point(x=6, y=2): Entry(offset=73692, size=0),
    Point(x=6, y=3): Entry(offset=73692, size=0),
    Point(x=6, y=4): Entry(offset=73692, size=0),
    Point(x=6, y=5): Entry(offset=73692, size=0),
    Point(x=6, y=6): Entry(offset=73692, size=0),
    Point(x=6, y=7): Entry(offset=73692, size=0),
    Point(x=7, y=0): Entry(offset=73692, size=0),
    Point(x=7, y=1): Entry(offset=73692, size=0),
    Point(x=7, y=2): Entry(offset=73692, size=0),
    Point(x=7, y=3): Entry(offset=73692, size=0),
    Point(x=7, y=4): Entry(offset=73692, size=0),
    Point(x=7, y=5): Entry(offset=73692, size=0),
    Point(x=7, y=6): Entry(offset=73692, size=0),
    Point(x=7, y=7): Entry(offset=73692, size=0),
}

test_index_short = {
    Point(x=0, y=0): Entry(offset=532, size=25093),
    Point(x=0, y=1): Entry(offset=25625, size=11330),
    Point(x=1, y=0): Entry(offset=36955, size=26298),
    Point(x=1, y=1): Entry(offset=63253, size=10439),
}
