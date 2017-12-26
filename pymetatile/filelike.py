#!/usr/bin/python

import builtins
import struct
import math
from collections import OrderedDict

from pymetatile.objects import Header, Metadata, Point
from pymetatile.convert import META_SIZE

# metatile header magic value
META_MAGIC = b"META"  # in python3 bytes and str different


class MetatileFile(object):
    """MetatileFile is the file-like object.

    Attributes:
        filename (str): path to the file
        mode (str): mode in which the file is opened

    Attributes (only for "rb" mode):
        header (namedtuple Header): metatile header data, contains count of tiles, x, y, z
            coordinates.
        size (int): square root from Header.count
        metadata (namedtuple Metadata): metatile metadata, contains offset and size for tile data.

    Raises:
        IOError
    """

    def __init__(self, filename, mode="rb"):
        if mode not in ("rb", "wb"):
            raise IOError("mode not supported:", mode)

        self._file = builtins.open(filename, mode)
        self.filename = filename

        if mode == "rb":
            self.header = self._decode_header()
            self.size = round(math.sqrt(self.header.count))
            self.metadata = self._decode_metadata()
            self._iter = iter(self.metadata)

    def _decode_header(self):
        """Reads header data from file and returns Header."""

        size = len(META_MAGIC) + 4 * 4
        magic, count, x, y, z = struct.unpack("4s4i", self._file.read(size))
        if magic != META_MAGIC:
            raise IOError("wrong metatile magic header")

        return Header(count, x, y, z)

    def _decode_metadata(self):
        """Reads metadata from file and returns metadata as OrderedDict:
            {
                Point(x, y): Metadata(offset, size),
                ....
            }
        """

        metadata = OrderedDict()

        for x in range(self.header.x, self.size):
            for y in range(self.header.y, self.size):
                data = self._file.read(2 * 4)
                offset, size = struct.unpack("2i", data)
                metadata[Point(x, y)] = Metadata(offset, size)

        return metadata

    def __repr__(self):
        return "{}.{}({})".format(self.__class__.__module__, self.__class__.__qualname__,
                                  self.header)

    def __str__(self):
        return str(self.header)

    def __len__(self):
        """Return count of tiles from header.

        >>> with open("tests/data/0.meta", "rb") as mt:
        ...     print(len(mt))
        64
        """

        return self.header.count

    def __contains__(self, item):
        """Checks if tuple or namedtuple Point(x, y) contains it metadata."""

        return item in self.metadata

    def read(self):
        """Default file-like read() method. Not implemented, use readtile() or readtiles() instead.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError("use readtile() or readtiles() instead")

    def write(self, x, y, z, data):
        """Writes tiles data to opened meatatile file. Use x, y, z (int) as metatile header values.

        Args:
            x, y, z (int): coordinates for metatile header (start Point(x, y), end
                Point(x + META_SIZE, y + META_SIZE)). Metatile contains META_SIZE * META_SIZE.
            data: dict of tiles data with tuple (x, y) as key and bytes as value:
                {
                    (x, y): bytes (str),
                    (x, y + 1): bytes (str),
                    ...
                    (x + META_SIZE, y + META_SIZE): bytes (str),
                }
        """

        # write header data
        count = META_SIZE * META_SIZE
        self._file.write(struct.pack("4s4i", META_MAGIC, count, x, y, z))
        size = round(math.sqrt(count))

        offset = len(META_MAGIC) + 4 * 4
        # need to pre-compensate the offsets for the size of the offset/size
        # table we are about to write
        offset += (2 * 4) * count

        # collect all the tiles offset/sizes
        # metadata = {}
        metadata = []
        size_ = 0
        for x_ in range(x, x+size):
            for y_ in range(y, y+size):
                if (x_, y_) in data:
                    size_ = len(data[x_, y_])
                    metadata.append(Metadata(offset, size_))
                else:
                    metadata.append(Metadata(0, 0))
                offset += size_

        # write out metadata
        for m in metadata:
            self._file.write(struct.pack("2i", m.offset, m.size))

        # write out data
        for x_ in range(x, x+size):
            for y_ in range(y, y+size):
                self._file.write(data[(x_, y_)])

    def readtile(self, x, y):
        """Read tile data with x, y (int) coordinates from metatile file. Return bytes (str).

        >>> with open("tests/data/0.meta", "rb") as mt:
        ...     data = mt.readtile(1, 1)
        ...     print(len(data))
        10439
        """

        offset, size = self.metadata[Point(x, y)]
        self._file.seek(offset)
        data = self._file.read(size)

        return data

    def readtiles(self):
        """Read all tiles data from metatile file.

        Returns: dict with tuple (x, y) as key and tile data as value:
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
        for p in self.metadata:
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
        return self

    def __next__(self):
        p = next(self._iter)
        return Point(p.x, p.y)


def open(file, mode="rb"):
    """Is the wrapper around builtin open() function. Returns Metatile file-like object.

    Available modes:
    - "rb": open for reading (default)
    - "wb": open for writing (rewrite file if exist)

    Args:
        file (str): path to the file
        mode (str): mode in which the file is opened

    >>> import pymetatile
    >>> with pymetatile.open("tests/data/0.meta") as mt:
    ...     print(mt)
    Header(count=64, x=0, y=0, z=1)
    """

    return MetatileFile(file, mode)
