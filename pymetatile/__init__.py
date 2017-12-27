#!/usr/bin/python

"""Package pymetatile provides file-like object for reading and writing tiles in metatile format.

pymetatile.open() provides file-like interface for reading and writing metatiles.

pymetatile.Metatile provides interfaces for creating Metatile object.

pymetatile.Tile provides interfaces for creating Tile object.
"""

from pymetatile.filelike import open  # noqa: F401
from pymetatile.metatile import Metatile, META_SIZE  # noqa: F401
from pymetatile.tile import Tile  # noqa: F401
