#!/usr/bin/python

from collections import namedtuple


# Header is the namedtuple represents metatile header with fileds: count, x, y, z (int).
Header = namedtuple("Header", "count x y z")

# Metadata is the namedtuple represents metatile metadata items with fields: offset, size (int)
Metadata = namedtuple("Metadata", "offset size")

# Point is the namedtuple represents point with x, y (int) coordinates.
Point = namedtuple("Point", "x y")
