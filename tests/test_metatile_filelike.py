#!/usr/bin/python

import filecmp

import pytest

import context  # noqa: F401
import pyosmkit
from pyosmkit.point import Point
from data.index_table import test_index, test_file


def test_open_unsupported_modes():
    with pytest.raises(IOError):
        pyosmkit.metatile.open(test_file, "r")
        pyosmkit.metatile.open(test_file, "w")


def test_open_not_found():
    with pytest.raises(IOError):
        pyosmkit.metatile.open("notfound")


def test_metatile_open():
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        assert isinstance(mt, pyosmkit.metatile.filelike.MetatileFile)


def test_metatile_header():
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        assert str(mt.header) == "Header(count=64, x=0, y=0, z=1)"


def test_metatile_index():
    errors = []
    with pyosmkit.metatile.open(test_file) as mt:
        for x in range(mt.header.x, pyosmkit.metatile.META_SIZE):
            for y in range(mt.header.y, pyosmkit.metatile.META_SIZE):
                if (x, y) not in mt.index:
                    errors.append(x, y)

        p = Point(10, 10)
        if p in mt.index:
            errors.append(p)

    assert not errors


def test_metatile_index_0_meta():
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        index = mt.index

    assert test_index == index


def test_metatile_read():
    with pytest.raises(NotImplementedError):
        with pyosmkit.metatile.open(test_file, "rb") as mt:
            mt.read()


def test_metatile_readtile():
    entry = test_index[(1, 0)]
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        data = mt.readtile(1, 0)

    assert len(data) == entry.size


def test_metatile_readtiles():
    size = 0
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        data = mt.readtiles()

        for p in mt:
            size += len(data[p])

    valid_size = 0
    for m in test_index.values():
        valid_size += m.size

    assert size == valid_size


def test_metatile_write():
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        header = mt.header
        data = mt.readtiles()

    with pyosmkit.metatile.open(test_file + ".tmp", "wb") as mt:
        mt.write(x=header.x, y=header.y, z=header.z, data=data)

    diff = filecmp.cmp(test_file, test_file + ".tmp")
    assert diff


def test_metatile_write_short():
    with pyosmkit.metatile.open(test_file, "rb") as mt:
        header = mt.header
        data = mt.readtiles()

    data_none_empty = {}
    for p, d in data.items():
        if d:
            data_none_empty[p] = d

    with pyosmkit.metatile.open(test_file + ".tmp", "wb") as mt:
        mt.write(x=header.x, y=header.y, z=header.z, data=data_none_empty)

    diff = filecmp.cmp(test_file, test_file + ".tmp")
    assert diff
