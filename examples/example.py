#!/usr/bin/python

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pymetatile

FILE = "/mnt/d/Tmp/1.meta"
MODE = "rb"

# mt = pymetatile.open("/mnt/d/Tmp/1.meta", "rb")
# mt.metadata()
# mt.close()
with pymetatile.open(FILE, MODE) as mt:
    print(mt)
    #print(mt.metadata[])
    #print(len(mt.readtile(1, 1)))
    #print(mt.readtiles())
    for tile in mt:
        if tile.x == 9:
            print(tile)
