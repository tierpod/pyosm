#!/usr/bin/python

import pytest

import context  # noqa: F401
import pymetatile


@pytest.mark.parametrize("url,expected", [
    ("mapname/10/0/1/2/3/4.meta", "Metatile(z:10, hashes:[0, 1, 2, 3, 4], style:mapname)"),
    ("mapname/10/697/321.png", "Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)")
])
def test_metatile_from_url(url, expected):
    mt = pymetatile.Metatile.from_url(url)
    assert str(mt) == expected


@pytest.mark.parametrize("url", [
    ("10/0/1/2/3/4.meta"),
    ("mapname/10/0/1/2/3/4"),
    ("1/2/3.png"),
    ("1/2/3"),
    ("mapname/z/x/y.png"),
])
def test_metatile_from_url_raises(url):
    with pytest.raises(ValueError):
        pymetatile.Metatile.from_url(url)


@pytest.mark.parametrize("z,x,y,style,expected", [
    (1, 1, 1, "mapname", "Metatile(z:1, hashes:[0, 0, 0, 0, 0], style:mapname)"),
    (10, 697, 321, "mapname", "Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)"),
    (10, 697, 321, "", "Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:)"),
])
def test_metatile_from_tile(z, x, y, style, expected):
    mt = pymetatile.Metatile.from_tile(z=z, x=x, y=y, style=style)
    assert str(mt) == expected


@pytest.mark.parametrize("z,x,y,expected", [
    (1, 1, 1, 2),
    (2, 2, 2, 4),
    (4, 4, 4, 8),
])
def test_metatile_xy(z, x, y, expected):
    mt = pymetatile.Metatile.from_tile(z=z, x=x, y=y)
    assert mt.size() == expected


@pytest.mark.parametrize("basedir,z,x,y,style,expected", [
    ("/var/lib/mod_tile", 1, 1, 1, "mapname", "/var/lib/mod_tile/mapname/1/0/0/0/0/0.meta"),
    ("/cache", 10, 697, 321, "mapname", "/cache/mapname/10/0/0/33/180/128.meta"),
])
def test_metatile_filepath(basedir, z, x, y, style, expected):
    mt = pymetatile.Metatile.from_tile(z=z, x=x, y=y, style=style)
    assert mt.filepath(basedir) == expected
