#!/usr/bin/python
"""Provides file-like reader and writer object.

Metatile layout description from mod_tile project:

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

import math
import struct
from collections import OrderedDict, namedtuple
from io import open as builtin_open

from pyosmkit.point import Point
from pyosmkit.metatile.metatile import META_SIZE

# metatile header magic value
META_MAGIC = b"META"  # in python3 bytes and str different
# Entry represents entry struct: offset (int) and size (int).
Entry = namedtuple("Entry", "offset size")
# Header includes metatile struct fields except index[]: magic (bytes), count, x, y, z (int).
Header = namedtuple("Header", "count x y z")


class MetatileFile(object):
    """MetatileFile is the file-like object.

    Attributes:
        filename (str): path to the file
        mode (str): mode in which the file is opened

    Attributes (only for "rb" mode):
        header (namedtuple Header): metatile header, includes magic (bytes), count, x, y
            (int, lowest values), z (int).
        size (int): square root from Header.count
        index (OrderedDict): metatile index[], includes offsets from start of the file (int)
            and sizes (int), represents as OrderedDict starting from lowest Point:

            {
                Point(x, y): Entry(offset, size)
                ...
            }

    Raises:
        IOError
    """

    def __init__(self, filename, mode="rb"):
        if mode not in ("rb", "wb"):
            raise IOError("mode not supported:", mode)

        self._file = builtin_open(filename, mode)
        self.filename = filename

        if mode == "rb":
            self.header = self._decode_header()
            self.size = int(round(math.sqrt(self.header.count)))
            self.index = self._decode_index()

    def _decode_header(self):
        size = len(META_MAGIC) + 4 * 4
        magic, count, x, y, z = struct.unpack("4s4i", self._file.read(size))
        if magic != META_MAGIC:
            raise IOError("wrong metatile magic header")

        return Header(count, x, y, z)

    def _decode_index(self):
        index = OrderedDict()

        for x in range(self.header.x, self.header.x + self.size):
            for y in range(self.header.y, self.header.y + self.size):
                data = self._file.read(2 * 4)
                offset, size = struct.unpack("2i", data)
                index[Point(x, y)] = Entry(offset, size)

        return index

    def __repr__(self):
        return "{0}.{1}({2})".format(self.__class__.__module__, self.__class__.__name__,
                                     self.header)

    def __str__(self):
        return str(self.header)

    def __len__(self):
        """Return Header.count.

        >>> with open("tests/data/0.meta", "rb") as mt:
        ...     print(len(mt))
        64
        """

        return self.header.count

    def __contains__(self, item):
        """Checks if tuple or namedtuple Point(x, y) contains it index."""

        return item in self.index

    def read(self):
        """Default file-like read() method. Not implemented, use readtile() or readtiles() instead.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError("use readtile() or readtiles() instead")

    def write(self, x, y, z, data):
        """Writes tiles data to opened metatile file. Use x, y, z (int) as metatile header values.

        Args:
            x, y (int): lowest values for this metatile
            z (int): zoom level
            data: dict with tuple (x, y) as key and bytes as value with a length of Header.count:

                {
                    (x (int), y (int)): bytes,
                    ...
                    (x + count, y + count ): bytes,
                }
        """

        # write header data
        count = META_SIZE * META_SIZE
        self._file.write(struct.pack("4s4i", META_MAGIC, count, x, y, z))
        size = int(round(math.sqrt(count)))

        offset = len(META_MAGIC) + 4 * 4
        # need to pre-compensate the offsets for the size of the offset/size
        # table we are about to write
        offset += (2 * 4) * count

        # collect all the tiles offset/sizes
        index = []
        size_ = 0
        for x_ in range(x, x+size):
            for y_ in range(y, y+size):
                if (x_, y_) in data:
                    size_ = len(data[x_, y_])
                else:
                    size_ = 0
                index.append(Entry(offset, size_))
                offset += size_

        # write out index table
        for entry in index:
            self._file.write(struct.pack("2i", entry.offset, entry.size))

        # write out data
        for x_ in range(x, x+size):
            for y_ in range(y, y+size):
                if (x_, y_) in data:
                    self._file.write(data[(x_, y_)])

    def readtile(self, x, y):
        """Read tile data with x, y (int) coordinates from metatile file. Return bytes (str).

        >>> with open("tests/data/0.meta", "rb") as mt:
        ...     data = mt.readtile(1, 1)
        ...     print(len(data))
        10439
        """

        offset, size = self.index[Point(x, y)]
        self._file.seek(offset)
        data = self._file.read(size)

        return data

    def readtiles(self):
        """Read all tiles data from metatile file.

        Returns: dict with tuple (x, y) as key and tile data as value of length Header.count:
            {
                Point(x, y): bytes (str),
                ...
            }

        >>> with open("tests/data/0.meta", "rb") as mt:
        ...     data = mt.readtiles()
        ...     tile = data[(1, 1)]
        ...     print(len(tile))
        10439
        """

        data = {}
        for p in self.index:
            data[p] = self.readtile(p.x, p.y)

        return data

    def close(self):
        self._file.close()

    # with statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._file.close()

    # iteratate over metadata
    def __iter__(self):
        return iter(self.index)

    # python3
    def __next__(self):
        return self.next()

    # python2
    def next(self):
        return next(self)


def open(file, mode="rb"):
    """Is the wrapper around builtin open() function. Returns Metatile file-like object.

    Available modes:
    - "rb": open for reading (default)
    - "wb": open for writing (rewrite file if exist)

    Args:
        file (str): path to the file
        mode (str): mode in which the file is opened

    >>> with open("tests/data/0.meta") as mt:
    ...     print(mt)
    Header(count=64, x=0, y=0, z=1)
    """

    return MetatileFile(file, mode)
