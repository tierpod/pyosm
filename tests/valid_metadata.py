#!/usr/bin/python

import context
from pymetatile import Point, Metadata


test_file = "tests/data/0.meta"

valid_metadata = {
    Point(x=0, y=0): Metadata(offset=532, size=25093),
    Point(x=0, y=1): Metadata(offset=25625, size=11330),
    Point(x=0, y=2): Metadata(offset=36955, size=0),
    Point(x=0, y=3): Metadata(offset=36955, size=0),
    Point(x=0, y=4): Metadata(offset=36955, size=0),
    Point(x=0, y=5): Metadata(offset=36955, size=0),
    Point(x=0, y=6): Metadata(offset=36955, size=0),
    Point(x=0, y=7): Metadata(offset=36955, size=0),
    Point(x=1, y=0): Metadata(offset=36955, size=26298),
    Point(x=1, y=1): Metadata(offset=63253, size=10439),
    Point(x=1, y=2): Metadata(offset=73692, size=0),
    Point(x=1, y=3): Metadata(offset=73692, size=0),
    Point(x=1, y=4): Metadata(offset=73692, size=0),
    Point(x=1, y=5): Metadata(offset=73692, size=0),
    Point(x=1, y=6): Metadata(offset=73692, size=0),
    Point(x=1, y=7): Metadata(offset=73692, size=0),
    Point(x=2, y=0): Metadata(offset=73692, size=0),
    Point(x=2, y=1): Metadata(offset=73692, size=0),
    Point(x=2, y=2): Metadata(offset=73692, size=0),
    Point(x=2, y=3): Metadata(offset=73692, size=0),
    Point(x=2, y=4): Metadata(offset=73692, size=0),
    Point(x=2, y=5): Metadata(offset=73692, size=0),
    Point(x=2, y=6): Metadata(offset=73692, size=0),
    Point(x=2, y=7): Metadata(offset=73692, size=0),
    Point(x=3, y=0): Metadata(offset=73692, size=0),
    Point(x=3, y=1): Metadata(offset=73692, size=0),
    Point(x=3, y=2): Metadata(offset=73692, size=0),
    Point(x=3, y=3): Metadata(offset=73692, size=0),
    Point(x=3, y=4): Metadata(offset=73692, size=0),
    Point(x=3, y=5): Metadata(offset=73692, size=0),
    Point(x=3, y=6): Metadata(offset=73692, size=0),
    Point(x=3, y=7): Metadata(offset=73692, size=0),
    Point(x=4, y=0): Metadata(offset=73692, size=0),
    Point(x=4, y=1): Metadata(offset=73692, size=0),
    Point(x=4, y=2): Metadata(offset=73692, size=0),
    Point(x=4, y=3): Metadata(offset=73692, size=0),
    Point(x=4, y=4): Metadata(offset=73692, size=0),
    Point(x=4, y=5): Metadata(offset=73692, size=0),
    Point(x=4, y=6): Metadata(offset=73692, size=0),
    Point(x=4, y=7): Metadata(offset=73692, size=0),
    Point(x=5, y=0): Metadata(offset=73692, size=0),
    Point(x=5, y=1): Metadata(offset=73692, size=0),
    Point(x=5, y=2): Metadata(offset=73692, size=0),
    Point(x=5, y=3): Metadata(offset=73692, size=0),
    Point(x=5, y=4): Metadata(offset=73692, size=0),
    Point(x=5, y=5): Metadata(offset=73692, size=0),
    Point(x=5, y=6): Metadata(offset=73692, size=0),
    Point(x=5, y=7): Metadata(offset=73692, size=0),
    Point(x=6, y=0): Metadata(offset=73692, size=0),
    Point(x=6, y=1): Metadata(offset=73692, size=0),
    Point(x=6, y=2): Metadata(offset=73692, size=0),
    Point(x=6, y=3): Metadata(offset=73692, size=0),
    Point(x=6, y=4): Metadata(offset=73692, size=0),
    Point(x=6, y=5): Metadata(offset=73692, size=0),
    Point(x=6, y=6): Metadata(offset=73692, size=0),
    Point(x=6, y=7): Metadata(offset=73692, size=0),
    Point(x=7, y=0): Metadata(offset=73692, size=0),
    Point(x=7, y=1): Metadata(offset=73692, size=0),
    Point(x=7, y=2): Metadata(offset=73692, size=0),
    Point(x=7, y=3): Metadata(offset=73692, size=0),
    Point(x=7, y=4): Metadata(offset=73692, size=0),
    Point(x=7, y=5): Metadata(offset=73692, size=0),
    Point(x=7, y=6): Metadata(offset=73692, size=0),
    Point(x=7, y=7): Metadata(offset=73692, size=0),
}
