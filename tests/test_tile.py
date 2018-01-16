#!/usr/bin/python

import pytest

import context  # noqa: F401
from pyosm import Tile, Metatile


@pytest.mark.parametrize("basedir,tile,expected", [
    ("/cache", Tile(10, 1, 2, "mapname", ".topojson"), "/cache/mapname/10/1/2.topojson"),
    ("", Tile(10, 1, 2), "10/1/2.png"),
])
def test_tile_filepath(basedir, tile, expected):
    assert str(tile.filepath(basedir)) == expected


def test_tile_from_metatile():
    mt = Metatile(z=10, hashes=[0, 0, 0, 0, 0], style="mapname")
    expected = "Tile(z:10, x:0, y:0, style:mapname, ext:.png)"
    assert str(Tile.from_metatile(mt)) == expected


def test_tile_from_url():
    url = "mapname/1/2/3.png"
    expected = "Tile(z:1, x:2, y:3, style:mapname, ext:.png)"
    t = Tile.from_url(url)
    assert str(t) == expected


@pytest.mark.parametrize("url", [
    ("1/2/3.png"),
    ("style/1/2/3"),
    ("style/z/2/3.png"),
])
def test_tile_from_url_raises(url):
    with pytest.raises(ValueError):
        Tile.from_url(url)
