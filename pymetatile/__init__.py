#!/usr/bin/python

import builtins
import struct
import math
from collections import namedtuple


OPEN_VALID_MODES = ("rb", "wb")
META_MAGIC = b"META"  # in python3 bytes and str different
META_SIZE = 8


Header = namedtuple("MetatileHeader", "magic count x y z")
Metadata = namedtuple("Metadata", "offset size")
Point = namedtuple("Point", "x y")
PointData = namedtuple("Point", "x y data")


class Metatile(object):
    def __init__(self, filename, mode="rb"):
        if mode not in OPEN_VALID_MODES:
            raise IOError("mode not supported:", mode)

        self._file = builtins.open(filename, mode)
        self.filename = filename
        self.header = self._decode_header()
        self.metadata = self._decode_metadata()
        self._iter = iter(self.metadata)

    def _decode_header(self):
        size = len(META_MAGIC) + 4 * 4
        magic, count, x, y, z = struct.unpack("4s4i", self._file.read(size))
        if magic != META_MAGIC:
            raise IOError("wrong metatile magic header")
        
        return Header(magic, count, x, y, z)

    def _decode_metadata(self):
        metadata = {}
        size = round(math.sqrt(self.header.count))
      
        for x in range(size):
            for y in range(size):
                data = self._file.read(2 * 4)
                offset, size_ = struct.unpack("2i", data)
                metadata[Point(x+size, y+size)] = Metadata(offset, size_)

        return metadata

    def __repr__(self):
        return "{}.{}({})".format(self.__class__.__module__, self.__class__.__qualname__,
                                  self.header)
    
    def __str__(self):
        return str(self.header)

    def read(self):
        raise NotImplementedError("use readtile() or readtiles() instead")

    def write(self):
        raise NotImplementedError
    
    def readtile(self, x, y):
        offset, size = self.metadata[Point(x, y)]
        self._file.seek(offset)
        data = self._file.read(size)

        return data

    def readtiles(self):
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

    # iterator throw tiles data
    def __iter__(self):
        return self

    def __next__(self):
        p = next(self._iter)
        data = self.readtile(p.x, p.y)
        #return p, data
        return PointData(p.x, p.y, data)


def open(filename, mode="rb"):
    return Metatile(filename, mode)

#def xy_to_offset(x, y):
#    mask = SIZE - 1
#    offset = (x & mask) * SIZE + (y & mask)
#    return offset
