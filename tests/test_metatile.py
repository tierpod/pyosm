#!/usr/bin/python

import pytest

import context  # noqa: F401
from pyosm import Tile, Metatile


def test_metatile_from_url():
    url = "mapname/10/0/1/2/3/4.meta"
    expected = "Metatile(z:10, hashes:[0, 1, 2, 3, 4], style:mapname)"
    mt = Metatile.from_url(url)
    assert str(mt) == expected


@pytest.mark.parametrize("url", [
    ("10/0/1/2/3/4.meta"),
    ("mapname/10/0/1/2/3/4"),
])
def test_metatile_from_url_raises(url):
    with pytest.raises(ValueError):
        Metatile.from_url(url)


@pytest.mark.parametrize("tile,expected", [
    (Tile(1, 1, 1, "mapname"), "Metatile(z:1, hashes:[0, 0, 0, 0, 0], style:mapname)"),
    (Tile(10, 697, 321, "mapname"), "Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:mapname)"),
    (Tile(10, 697, 321, ""), "Metatile(z:10, hashes:[0, 0, 33, 180, 128], style:)"),
])
def test_metatile_from_tile(tile, expected):
    mt = Metatile.from_tile(tile)
    assert str(mt) == expected


@pytest.mark.parametrize("tile,expected", [
    (Tile(1, 1, 1), 2),
    (Tile(2, 2, 2), 4),
    (Tile(4, 4, 4), 8),
])
def test_metatile_len(tile, expected):
    mt = Metatile.from_tile(tile)
    assert len(mt) == expected


@pytest.mark.parametrize("basedir,tile,expected", [
    ("/var/lib/mod_tile", Tile(1, 1, 1, "mapname"), "/var/lib/mod_tile/mapname/1/0/0/0/0/0.meta"),
    ("/cache", Tile(10, 697, 321, "mapname"), "/cache/mapname/10/0/0/33/180/128.meta"),
])
def test_metatile_filepath(basedir, tile, expected):
    mt = Metatile.from_tile(tile)
    assert mt.filepath(basedir) == expected


@pytest.mark.parametrize("url,expected", [
    ("mapname/10/0/0/33/180/128.meta", 64),
    ("mapname/1/0/0/0/0/0.meta", 4)
])
def test_metatile_iter_len(url, expected):
    mt = Metatile.from_url(url)
    count = 0
    for __ in mt:
        count += 1

    assert count == expected


@pytest.mark.parametrize("url", [
    ("mapname/10/0/0/33/180/128.meta"),
    ("mapname/1/0/0/0/0/0.meta"),
])
def test_metatile_points_order(url):
    mt = Metatile.from_url(url)
    points = []
    for p in mt:
        points.append(p)

    assert points == mt.points()
