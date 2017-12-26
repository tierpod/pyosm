#!/usr/bin/python

import os.path
import re

from pymetatile.objects import Point

# metatile size
META_SIZE = 8

RE_METATILE = re.compile(r"(\w+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)/(\d+)\.meta")
RE_TILE = re.compile(r"(\w+)/(\d+)/(\d+)/(\d+)(\.\w+)")


class Metatile(object):

    def __init__(self, z, hashes, style):
        self.z = z
        self.hashes = hashes
        self.style = style
        self.ext = ".meta"

    def __str__(self):
        return "Metatile(z:{}, hashes:{}, style:{})".format(self.z, self.hashes, self.style)

    def filepath(self, basedir=""):
        """Calculates metatile filepath using basedir (str).

        >>> mt = Metatile.from_tile(z=10, x=697, y=321, style="mapname")
        >>> print(mt.filepath("/var/lib/mod_tile"))
        /var/lib/mod_tile/mapname/10/0/0/33/180/128.meta

        >>> mt = Metatile.from_url("mapname/10/0/1/2/3/4.meta")
        >>> print(mt.filepath("/cache"))
        /cache/mapname/10/0/1/2/3/4.meta
        """

        h0 = str(self.hashes[0])
        h1 = str(self.hashes[1])
        h2 = str(self.hashes[2])
        h3 = str(self.hashes[3])
        h4 = str(self.hashes[4])
        return os.path.join(basedir, self.style, str(self.z), h0, h1, h2, h3, h4 + self.ext)

    def size(self):
        """Calculates min size of tiles with data inside metatile.

        >>> mt = Metatile.from_tile(z=1, x=1, y=1, style="mapname")
        >>> print(mt.size())
        2

        >>> mt = Metatile.from_tile(z=10, x=697, y=321, style="mapname")
        >>> print(mt.size())
        8
        """

        return min(META_SIZE, 1 << self.z)

    # def xy_box(self):
    #     x, y = self.xy()
    #     xx = range(x, x+self.size())
    #     yy = range(y, y+self.size())
    #
    #     return (xx, yy)

    def xy(self):
        """Calculates metatile coordinates. Returns namedtuple of int (x, y).

        >>> mt = Metatile.from_tile(z=10, x=697, y=321)
        >>> print(mt.xy())
        Point(x=696, y=320)
        """

        x = 0
        y = 0

        for i in range(5):
            x <<= 4
            y <<= 4
            x |= (self.hashes[i] & 0xf0) >> 4
            y |= (self.hashes[i] & 0x0f)

        return Point(x, y)

    @classmethod
    def from_url(cls, url):
        """Creates new Metatile from tile or metatile url. Parse url as metatile if ends with
        ".meta".

        >>> print(Metatile.from_url("mapname/10/697/321.topojson"))
        Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)

        >>> print(Metatile.from_url("mapname/10/0/1/2/3/4.meta"))
        Metatile(z:10, hashes:[0, 1, 2, 3, 4], style:mapname)
        """

        if url.endswith(".meta"):
            return _from_metatile_url(url)

        return _from_tile_url(url)

    @classmethod
    def from_tile(cls, z, x, y, style=""):
        """Create new Metatile from tile coordinates: z, x, y (int) and style (str).

        >>> print(Metatile.from_tile(z=10, x=697, y=321, style="mapname"))
        Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)
        """

        mask = META_SIZE - 1
        hashes = []

        x = x & ~mask
        y = y & ~mask

        for _ in range(5):
            hashes.append(((x & 0x0f) << 4) | (y & 0x0f))
            x >>= 4
            y >>= 4
        hashes.reverse()

        return Metatile(z=z, hashes=hashes, style=style)


def _from_metatile_url(url):
    """Parse url as metatile and return Metatile."""

    match = RE_METATILE.search(url)
    if not match:
        raise ValueError("unable to covert uri to Metatile")

    style, z, h0, h1, h2, h3, h4 = match.groups()
    hashes = [int(h0), int(h1), int(h2), int(h3), int(h4)]

    return Metatile(z=int(z), hashes=hashes, style=style)


def _from_tile_url(url):
    """Parse url as tile and return Metatile."""

    match = RE_TILE.search(url)
    if not match:
        raise ValueError("unable to covert uri to Tile")

    style, z, x, y, _ = match.groups()

    return Metatile.from_tile(z=int(z), x=int(x), y=int(y), style=style)
