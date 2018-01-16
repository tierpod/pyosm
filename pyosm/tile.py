#!/usr/bin/python

import os.path
import re

RE_TILE = re.compile(r"(\w+)/(\d+)/(\d+)/(\d+)(\.\w+)")


class Tile(object):
    """Attributes:
        z, x, y (int): zoom, x, y coordinates
        style (str): style name (optional, default="")
        ext (str): tile file extension (optional, default=".png")
    """

    def __init__(self, z, x, y, style="", ext=".png"):
        self.z = z
        self.x = x
        self.y = y
        self.ext = ext
        self.style = style

    def __str__(self):
        return "Tile(z:{}, x:{}, y:{}, style:{}, ext:{})".format(self.z, self.x, self.y, self.style,
                                                                 self.ext)

    def filepath(self, basedir=""):
        """Calculates tile filepath using basedir (str).

        >>> t = Tile(z=1, x=2, y=3, style="mapname", ext=".png")
        >>> print(t.filepath("/cache"))
        /cache/mapname/1/2/3.png
        """

        return os.path.join(basedir, self.style, str(self.z), str(self.x), str(self.y) + self.ext)

    @classmethod
    def from_metatile(cls, mt, ext=".png"):
        """Creates new Tile instance from pymetatile.Metatile object, use ext (str) as extension.

        >>> from pymetatile import Metatile
        >>> mt = Metatile.from_url("mapname/10/0/0/0/0/0.meta")
        >>> print(Tile.from_metatile(mt))
        Tile(z:10, x:0, y:0, style:mapname, ext:.png)
        """

        x = 0
        y = 0

        for h in mt.hashes:
            x <<= 4
            y <<= 4
            x |= (h & 0xf0) >> 4
            y |= (h & 0x0f)

        return Tile(x=x, y=y, z=mt.z, style=mt.style, ext=ext)

    @classmethod
    def from_url(cls, url):
        """Creates new Tile instance from url (str).

        >>> print(Tile.from_url("mapname/1/2/3.png"))
        Tile(z:1, x:2, y:3, style:mapname, ext:.png)
        """

        match = RE_TILE.search(url)
        if not match:
            raise ValueError("unable to covert uri to Tile")

        style, z, x, y, ext = match.groups()

        return Tile(style=style, z=int(z), x=int(x), y=int(y), ext=ext)
