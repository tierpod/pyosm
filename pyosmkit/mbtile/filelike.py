#!/usr/bin/python

from collections import namedtuple
import sqlite3

from pyosmkit.point import Bound, Bounds

Metadata = namedtuple("Metadata", "center, format, bounds, minzoom, maxzoom")


class MBTileFile(object):
    """
    zoom_level = z
    tile_column = x
    tile_row = y
    """

    def __init__(self, filename, mode="rb", flip_y=True):
        if mode not in ("rb"):
            raise IOError("mode not supported:", mode)

        self.filename = filename
        self._conn = sqlite3.connect(filename)
        self._conn.row_factory = sqlite3.Row
        self.flip_y = flip_y

        if mode == "rb":
            self.metadata = self._get_metadata()
            self.bounds = self._get_bounds()

    def _get_metadata(self):
        cur = self._conn.cursor()
        cur.execute("SELECT name, value FROM metadata")
        res = cur.fetchall()
        for row in res:
            if "center" in row:
                center = row["value"]
            if "format" in row:
                format_ = row["value"]
            if "bounds" in row:
                bounds = row["value"]
            if "minzoom" in row:
                minzoom = row["value"]
            if "maxzoom" in row:
                maxzoom = row["value"]

        # TODO: parse metadata values to float and int
        return Metadata(str(center), str(format_), str(bounds), int(minzoom), int(maxzoom))

    def _get_bounds(self):
        result = []
        cur = self._conn.cursor()
        for z in range(self.metadata.minzoom, self.metadata.maxzoom + 1):
            cur.execute("SELECT min(tile_column) as min_x, max(tile_column) as max_x, "
                        "min(tile_row) as min_y, max(tile_row) as max_y "
                        "FROM tiles WHERE zoom_level=?", (z,))
            res = cur.fetchone()

            if self.flip_y:
                min_y = flip_y_coord(z, int(res["max_y"]))
                max_y = flip_y_coord(z, int(res["min_y"]))
            else:
                min_y = int(res["min_y"])
                max_y = int(res["max_y"])

            result.append(Bound(z=z,
                                min_x=int(res["min_x"]), max_x=int(res["max_x"]),
                                min_y=min_y, max_y=max_y))

        return Bounds(result)

    def __str__(self):
        return str(self.metadata)

    # with statement
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __contains__(self, item):
        return item in self.bounds

    def close(self):
        self._conn.close()

    def readtile(self, z, x, y):
        """Read tile data for z, x, y (int) coordinates from mbtiles file. Return bytes (str).

        >>> mb = open("tests/data/0.mbtiles")
        >>> data = mb.readtile(1, 1, 0)
        >>> print(len(data))
        26298
        >>> data = mb.readtile(12, 999, 999)
        Traceback (most recent call last):
            ...
        ValueError: data not found for given (z, x, y)
        """

        if self.flip_y:
            y = flip_y_coord(z, y)

        cur = self._conn.cursor()
        cur.execute("SELECT tile_data FROM tiles "
                    "WHERE zoom_level=? AND tile_column=? AND tile_row=?;", (z, x, y))
        res = cur.fetchone()
        if not res:
            raise ValueError("data not found for given (z, x, y)")

        # TODO: return str or bytes?
        return res["tile_data"]


def open(file, mode="rb", flip_y=True):
    """Wrapper around sqlite3.connect() functions. Returns MBTile file-like object.

    Available modes:
    - "rb": open for reading (default)

    Args:
        file (str): path to the file
        mode (str): mode in which the file is opened
        flip_y (bool): flip y coordinate?

    >>> from pyosmkit.point import ZXY
    >>> with open("tests/data/0.mbtiles") as mb:
    ...     print(mb)
    ...     print(mb.bounds.for_zoom(12))
    Metadata(center='108.4003,52.03223,9', format='png', \
bounds='108.3703,52.01723,108.4303,52.04723', minzoom=0, maxzoom=17)
    Bound(z:12 x:3281-3281 y:1352-1352)
    """

    return MBTileFile(file, mode, flip_y)


def flip_y_coord(zoom, y):
    """Flips y (int) coordinate for given zoom (int).

    >>> flip_y_coord(12, 3281)
    814
    >>> flip_y_coord(12, 814)
    3281
    """

    return (2**zoom-1) - y
