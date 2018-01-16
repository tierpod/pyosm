#!/usr/bin/python

"""Package pymetatile is the pythonic-way library for reading/writing metatile files, translating
Tile <-> Metatile coordinates. Provides:

* file-like object with readtile(x, y), readtiles(), write(x, y, z, data) methods (support: with
statement, Point(x, y) in  statement, iterating over Points):

>>> import pymetatile
>>> with pymetatile.open("tests/data/0.meta", "rb") as mt:
...     data = mt.readtile(1, 1)
...     print(len(data))
10439


you can also use MetatileFile attributes: index, header, size.

* pymetatile.Metatile object with from_url, from_tile methods for creating.

* pymetatile.Tile object with from_url, from_metatile methods for creating.

for more information, see info().
"""

from pyosm.metatile import Metatile, META_SIZE  # noqa: F401
from pyosm.metatile.filelike import open  # noqa: F401
from pyosm.point import Point, ZXY, LatLong, zxy_to_latlong, latlong_to_zxy  # noqa: F401
from pyosm.polygon import Polygon, Region  # noqa: F401
from pyosm.tile import Tile  # noqa: F401
