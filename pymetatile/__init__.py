#!/usr/bin/python

import builtins
import struct
import math
from collections import namedtuple, OrderedDict


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

        if mode == "rb":
            self.header = self._decode_header()
            self.size = round(math.sqrt(self.header.count))
            self.metadata = self._decode_metadata()
            self._iter = iter(self.metadata)

    def _decode_header(self):
        size = len(META_MAGIC) + 4 * 4
        magic, count, x, y, z = struct.unpack("4s4i", self._file.read(size))
        if magic != META_MAGIC:
            raise IOError("wrong metatile magic header")
        
        return Header(magic, count, x, y, z)

    def _decode_metadata(self):
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
        return self.header.count

    def __contains__(self, item):
        return item in self.metadata

    def read(self):
        raise NotImplementedError("use readtile() or readtiles() instead")

    def write(self, count, x, y, z, data):
        # data is the {(x, y): bytes}
        # write header data
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
