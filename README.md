pyosm: library for building OSM tools
=====================================

Package pymetatile is the pythonic-way library for reading/writing metatile files, translating
Tile <-> Metatile coordinates.

For example, read specific tile data from metatile quite easy:

```python
>>> import pymetatile
>>> with pymetatile.open("tests/data/0.meta", "rb") as mt:
...     data = mt.readtile(1, 1)
...     print(len(data))
10439

```

MetatileFile
------------

**pymetatile.open(filename, mode)** opens file for reading ("rb" mode) or writing ("wb").

Support *with* statement, *in* statement, *iterating* over Points):

```python
>>> import pymetatile
>>> mt = pymetatile.open("tests/data/0.meta", "rb")
>>> # check if tile (1, 2) contains in metatile
>>> print((1, 2) in mt, (10, 10) in mt)
True False
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

Attributes:

* index: index table, dict {Point(x, y): Entry(offset, size), ...}
* header: header data, Header(count, x, y, z)
* size: square root of header.count

Methods:

* **readtile(x, y)** -> bytes
* **readtiles()** -> dict {Point(x, y): bytes, ...}
* **write(x, y, z, data)**, where z is the metatile zoom level, x, y is the lowest values,
  data is the dict {Point(x, y): bytes, ...}

Metatile
--------

Methods:

* **from_url(url)** -> Metatile
* **from_tile(Tile)** -> Metatile
* **filepath(basedir)** -> str

```python
>>> from pymetatile import Metatile, Tile
>>>
>>> tile = Tile(z=10, x=697, y=321, style="mapname", ext=".png")
>>> mt = Metatile.from_tile(tile)
>>> print(mt)
Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)
>>> print(len(mt))
8
>>> print(mt.filepath("/cache"))
/cache/mapname/10/0/0/33/180/128.meta

```

Tile
----

Methods:

* **from_url(url)** -> Tile
* **from_metatile(mt)** -> Tile
* **filepath(url)** -> str

```python
>>> from pymetatile import Metatile, Tile
>>>
>>> mt = Metatile.from_url("mapname/10/0/0/0/0/0.meta")
>>> tile = Tile.from_metatile(mt)
>>> print(tile)
Tile(z:10, x:0, y:0, style:mapname, ext:.png)
>>> print(tile.filepath("/cache"))
/cache/mapname/10/0/0.png

```

for more information, see info().

metatile format description
---------------------------

Can be found in [mod_tile][1] project:

[1]: https://github.com/openstreetmap/mod_tile/blob/master/includes/metatile.h
