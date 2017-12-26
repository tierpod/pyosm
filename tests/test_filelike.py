#!/usr/bin/python

import filecmp

import pytest

import context  # noqa: F401
import pymetatile
from pymetatile.objects import Point
from valid_metadata import valid_metadata, test_file


def test_open_unsupported_modes():
    with pytest.raises(IOError):
        pymetatile.open(test_file, "r")
        pymetatile.open(test_file, "w")


def test_open_not_found():
    with pytest.raises(IOError):
        pymetatile.open("notfound")


def test_metatile_open():
    with pymetatile.open(test_file, "rb") as mt:
        assert isinstance(mt, pymetatile.filelike.MetatileFile)


def test_metatile_header():
    with pymetatile.open(test_file, "rb") as mt:
        assert str(mt.header) == "Header(count=64, x=0, y=0, z=1)"


def test_metatile_metadata():
    errors = []
    with pymetatile.open(test_file) as mt:
        for x in range(mt.header.x, pymetatile.META_SIZE):
            for y in range(mt.header.y, pymetatile.META_SIZE):
                if (x, y) not in mt.metadata:
                    errors.append(x, y)

        p = Point(10, 10)
        if p in mt.metadata:
            errors.append(p)

    assert not errors


def test_metatile_metadata_dict():
    with pymetatile.open(test_file, "rb") as mt:
        metadata = mt.metadata

    assert valid_metadata == metadata


def test_metatile_read():
    with pytest.raises(NotImplementedError):
        with pymetatile.open(test_file, "rb") as mt:
            mt.read()


def test_metatile_readtile():
    metadata = valid_metadata[(1, 0)]
    with pymetatile.open(test_file, "rb") as mt:
        data = mt.readtile(1, 0)

    assert len(data) == metadata.size


def test_metatile_readtiles():
    size = 0
    with pymetatile.open(test_file, "rb") as mt:
        data = mt.readtiles()

        for p in mt:
            size += len(data[p])

    valid_size = 0
    for m in valid_metadata.values():
        valid_size += m.size

    assert size == valid_size


def test_metatile_write():
    with pymetatile.open(test_file, "rb") as mt:
        header = mt.header
        data = mt.readtiles()

    with pymetatile.open(test_file + ".tmp", "wb") as mt:
        mt.write(x=header.x, y=header.y, z=header.z, data=data)

    diff = filecmp.cmp(test_file, test_file + ".tmp")
    assert diff
