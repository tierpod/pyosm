#!/usr/bin/python

"""Package pymetatile provides file-like object for reading and writing tiles in metatile format.

pymetatile.open() provides file-like interface for reading and writing metatiles.

pymetatile.Metatile provides interfaces for creating Metatile object.

pymetatile.Tile provides interfaces for creating Tile object.

struct entry {
    int offset;
    int size;
};

struct meta_layout {
    char magic[4];
    int count; // METATILE ^ 2
    int x, y, z; // lowest x,y of this metatile, plus z
    struct entry index[]; // count entries
    // Followed by the tile data
    // The index offsets are measured from the start of the file
};
"""

from pymetatile.filelike import open  # noqa: F401
from pymetatile.metatile import Metatile, META_SIZE  # noqa: F401
from pymetatile.tile import Tile  # noqa: F401
