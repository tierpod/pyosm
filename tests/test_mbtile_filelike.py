#!/usr/bin/python

import context  # noqa: F401
import pyosmkit.mbtile
from pyosmkit.mbtile.filelike import Metadata
from pyosmkit.point import Bounds


def test_metadata():
    with pyosmkit.mbtile.open("tests/data/0.mbtiles") as mb:
        metadata = mb.metadata

    assert metadata == Metadata(center='108.4003,52.03223,9', format='png',
                                bounds='108.3703,52.01723,108.4303,52.04723',
                                minzoom=0, maxzoom=17)


def test_bounds():
    with pyosmkit.mbtile.open("tests/data/0.mbtiles") as mb:
        bounds = mb.bounds

    assert isinstance(bounds, pyosmkit.point.Bounds)


def test_bounds_zooms():
    with pyosmkit.mbtile.open("tests/data/0.mbtiles") as mb:
        bounds = mb.bounds

    ok = True
    for b in bounds:
        if b.max_x < b.min_x:
            ok = False
        if b.max_y < b.min_y:
            ok = False

    assert ok


def test_readtile():
    with pyosmkit.mbtile.open("tests/data/0.mbtiles") as mb:
        data = mb.readtile(1, 1, 0)

    assert len(data) == 26298
