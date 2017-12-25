pymetatile
==========

Metatile file encoder and decoder implemented in pythonic way. With this library, you can:

*open* metatile with **pymetatile.open(filename, mode)** function:

```python
>>> mt = pymetatile.open("/path/to/metatile")
>>> # ...
>>> mt.close()

>>> # with statement also supported!
>>> with pymetatile.open("/path/to/metatile", "rb") as mt:
...     # ...
```

*read* metatile header and metadata in human-friendly form:

```python
>>> print(mt.header)
Header(count=64, x=0, y=0, z=1)

>>> print(mt.metadata)  # print(mt) is the same
OrderedDict([(Point(x=0, y=0), Metadata(offset=532, size=25093)) ... ])

>>> print(mt.metadata[(1, 1)])  # print metadata for Point(1, 1)
Metadata(offset=63253, size=10439)
```

*read* specific tile data or all tiles data (use "rb" mode):

```python
# read data for tile with x=1, y=1 coordinates
>>> d = mt.readtile(1, 1)

# read data for all tiles
>>> data = mt.readtiles()

# you can now use it by key
>>> print(data[(1, 2)]))

# or you can iterate over it and print only none-empty tile data
>>> for point, data in data.items():
...     if data:
...         print(point, data)
```

*write* tiles data to new metatile (use "wb" mode). data must be dict of 64 items with key =
Point(x, y) and value = bytes (str):

```python
>>> data = {
...     (x, y): bytes,
...     (x + 1, y): bytes,
...     # ...
...     (x + MAX_SIZE, y + MAX_SIZE): bytes,
... }
>>> with pymetatile.open("/path/to/metatile", "wb") as mt:
...     mt.write(data)
```

*iterate* over metadata and use *in* statement:

```python
# print tiles with coordinate x = 7
>>> for p in mt:
...     if p.x == 7:
...        print(p)

# checks if tile with coordinates Point(x=1, y=2) contains in opened metatile
>>> print (1, 2) in mt
True
```

*len()* returns count of tiles (Header.count).


metatile format description
---------------------------

Can be found in [mod_tile][1] project:


[1]: https://github.com/openstreetmap/mod_tile/blob/master/includes/metatile.h
