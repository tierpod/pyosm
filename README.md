pyosm: library for building OSM tools
=====================================

This package contains helpers for building tools around OSM tiles.

pyosm.point
-----------

Create points, convert coordinates.

* **zxy_to_latlong(z, x, y)** -> LatLong
* **latlong_to_zxy(lat, lng, zoom)** -> ZXY

```python
>>> import pyosm.point
>>> p = pyosm.point.ZXY(z=10, x=697, y=321)
>>> print(pyosm.point.zxy_to_latlong(p.z, p.x, p.y))
LatLong(lat=55.5783, long=65.0391)

```

pyosm.tile
----------

Create [osm][2] tile, get filename.

* **Tile.from_url(url)** -> Tile
* **Tile.from_metatile(mt)** -> Tile
* **Tile.filepath(url)** -> str

```python
>>> import pyosm.tile
>>> t = pyosm.tile.Tile.from_url("/style/1/1/1.png")
>>> print(t)
Tile(z:1, x:1, y:1, style:style, ext:.png)
>>> print(t.filepath("/cache"))
/cache/style/1/1/1.png

```

pyosm.polygon
-------------

List of tiles can be grouped to the *closed* polygon. You can check if LatLong point inside this
polygon or not (using [ray-casting][3] algorithm):

```python
>>> from pyosm.point import LatLong
>>> from pyosm.polygon import Polygon
>>> polygon = Polygon([LatLong(0, 0), LatLong(10, 0), LatLong(10, 10),
...                    LatLong(0, 10), LatLong(0, 0)])
>>> print(LatLong(1, 2) in polygon)
True
>>> print(LatLong(11, 12) in polygon)
False

```

Also, a list of polygons can be grouped to Region (support *in* statement).

pyosm.metatile
--------------

### Metatile

Create metatile coordinates, get filename:

* **Metatile.from_url(url)** -> Metatile
* **Metatile.from_tile(Tile)** -> Metatile
* **Metatile.filepath(basedir)** -> str

```python
>>> from pyosm.tile import Tile
>>> from pyosm.metatile import Metatile
>>> tile = Tile(z=10, x=697, y=321, style="mapname", ext=".png")
>>> mt = Metatile.from_tile(tile)
>>> print(mt)
Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)
>>> print(mt.filepath("/cache"))
/cache/mapname/10/0/0/33/180/128.meta

```

### MetatileFile

Try to implement metatile file encoder/decoder in pythonic way (inspired by Raymond Hettinger
videos).

* **pyosm.metatile.open(filename, mode)** -> MetatileFile: opens file for reading ("rb" mode) or
  writing ("wb"). Returns file-like object.

Support *with* statement, *in* statement, *iterating* over points:

```python
>>> import pyosm.metatile
>>> mt = pyosm.metatile.open("tests/data/0.meta", "rb")
>>> # check if tile (1, 2) contains in metatile
>>> print((1, 2) in mt)
True
>>> print((10, 10) in mt)
False
>>> # iterate over Points and print only points with x == 7
>>> for point in mt:
...     if point.x == 7:
...         print(point)
Point(x=7, y=0)
Point(x=7, y=1)
Point(x=7, y=2)
Point(x=7, y=3)
Point(x=7, y=4)
Point(x=7, y=5)
Point(x=7, y=6)
Point(x=7, y=7)
>>> # read all tiles data, iterate over Points and print only none-empty data:
>>> tiles_data = mt.readtiles()
>>> for point, data in tiles_data.items():
...     if data:
...         print(point, len(data))
Point(x=0, y=0) 25093
Point(x=0, y=1) 11330
Point(x=1, y=0) 26298
Point(x=1, y=1) 10439
>>> mt.close()

```

* **MetatileFile.readtile(x, y)** -> bytes
* **MetatileFile.readtiles()** -> dict {Point(x, y): bytes, ...}
* **MetatileFile.write(x, y, z, data)**, where z is the metatile zoom level, x, y is the lowest values,
  data is the dict {Point(x, y): bytes, ...}

metatile format description
---------------------------

Can be found in [mod_tile][1] project:

pyosm.mbtile
------------

Decode mbtiles file, read tile from mbtiles file. Support *with*, *in* statements.

```python
>>> import pyosm.mbtile
>>> from pyosm.point import ZXY
>>> point = ZXY(z=1, x=1, y=0)
>>> with pyosm.mbtile.open("tests/data/0.mbtiles") as mb:
...   print(point in mb)
...   print(len(mb.readtile(point.z, point.x, point.y)))
True
26298

```

* **pyosm.mbtile.open(file, mode, flip_y)** -> MBTileFile: open file for reading. Returns file-like object.

* **MBTileFile.readtile(z, x, y)** -> buffer

[1]: https://github.com/openstreetmap/mod_tile/blob/master/includes/metatile.h
[2]: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
[3]: http://rosettacode.org/wiki/Ray-casting_algorithm
