pyosmkit: library for building OSM tools
========================================

This package contains helpers for building tools around OSM tiles.

**Since 0.11** package name was changed from **pyosm** to **pyosmkit** to avoid pypi conflicts.

Installation
------------

```bash
# from pypi
pip install --user pyosmkit

# or from github where ${TAG} is the git version tag, eg v0.6
pip install --user git+https://github.com/tierpod/pyosmkit.git@${TAG}#egg=pyosmkit
```

Developing
----------

```bash
git clone https://github.com/tierpod/pyosmkit.git && cd pyosmkit
make venv
source ./venv/bin/activate
make init-dev
```

pyosmkit.point
--------------

Create points, convert coordinates.

* **zxy_to_latlong(z, x, y)** -> LatLong
* **latlong_to_zxy(lat, lng, zoom)** -> ZXY

```python
>>> import pyosmkit.point
>>> p = pyosmkit.point.ZXY(z=10, x=697, y=321)
>>> pyosmkit.point.zxy_to_latlong(p.z, p.x, p.y)
LatLong(lat=55.5783, long=65.0391)

```

pyosmkit.tile
-------------

Create [osm][2] tile, get filename.

* **Tile.from_url(url)** -> Tile
* **Tile.from_metatile(mt)** -> Tile
* **Tile.filepath(url)** -> str

```python
>>> from pyosmkit.tile import Tile
>>> t = Tile.from_url("/style/1/1/1.png")
>>> print(t)
Tile(z:1, x:1, y:1, style:style, ext:.png)
>>> t.filepath("/cache")
'/cache/style/1/1/1.png'

```

pyosmkit.polygon
----------------

List of tiles can be grouped to the *closed* polygon. You can check if LatLong point inside this
polygon or not (using [ray-casting][3] algorithm):

```python
>>> from pyosmkit.point import LatLong
>>> from pyosmkit.polygon import Polygon
>>> polygon = Polygon([LatLong(0, 0), LatLong(10, 0), LatLong(10, 10),
...                    LatLong(0, 10), LatLong(0, 0)])
>>> LatLong(1, 2) in polygon
True
>>> LatLong(11, 12) in polygon
False

```

Also, a list of polygons can be grouped to Region (support *in* statement).

pyosmkit.metatile
-----------------

### Metatile

Create metatile coordinates, get filename:

* **Metatile.from_url(url)** -> Metatile
* **Metatile.from_tile(Tile)** -> Metatile
* **Metatile.filepath(basedir)** -> str

```python
>>> from pyosmkit.tile import Tile
>>> from pyosmkit.metatile import Metatile
>>> tile = Tile(z=10, x=697, y=321, style="mapname", ext=".png")
>>> mt = Metatile.from_tile(tile)
>>> print(mt)
Metatile(z:10, x:696-703, y:320-327, style:mapname)
>>> mt.filepath("/cache")
'/cache/mapname/10/0/0/33/180/128.meta'

```

### MetatileFile

Try to implement metatile file encoder/decoder in pythonic way (inspired by Raymond Hettinger
videos).

* **pyosmkit.metatile.open(filename, mode)** -> MetatileFile: opens file for reading ("rb" mode) or
  writing ("wb"). Returns file-like object.

Support *with* statement, *in* statement, *iterating* over points:

```python
>>> import pyosmkit.metatile
>>> mt = pyosmkit.metatile.open("tests/data/0.meta", "rb")
>>> # check if tile (1, 2) contains in metatile
>>> (1, 2) in mt
True
>>> (10, 10) in mt
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
...         # do something with point(z, x, y) or data (bytes)
...         pass
>>> mt.close()

```

* **MetatileFile.readtile(x, y)** -> bytes
* **MetatileFile.readtiles()** -> dict {Point(x, y): bytes, ...}
* **MetatileFile.write(x, y, z, data)**, where z is the metatile zoom level, x, y is the lowest
  values, data is the dict {Point(x, y): bytes, ...}

metatile format description
---------------------------

Can be found in [mod_tile][1] project:

pyosmkit.mbtile
---------------

Decode mbtiles file, read tile from mbtiles file. Support *with*, *in* statements.

```python
>>> import pyosmkit.mbtile
>>> from pyosmkit.point import ZXY
>>> point = ZXY(z=1, x=1, y=0)
>>> with pyosmkit.mbtile.open("tests/data/0.mbtiles") as mb:
...   print(point in mb)
...   print(len(mb.readtile(point.z, point.x, point.y)))
True
26298

```

* **pyosmkit.mbtile.open(file, mode, flip_y)** -> MBTileFile: open file for reading. Returns
  file-like object.

* **MBTileFile.readtile(z, x, y)** -> buffer

[1]: https://github.com/openstreetmap/mod_tile/blob/master/includes/metatile.h
[2]: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
[3]: http://rosettacode.org/wiki/Ray-casting_algorithm
