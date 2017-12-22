#!/usr/bin/python

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
