#!/usr/bin/python

import argparse

from pyosm import Tile, Metatile


def parse_args():
    parser = argparse.ArgumentParser(description="Convert filepath between tile and metatile.")
    parser.add_argument("-d", "--basedir", default="", help="output basedir prefix")
    parser.add_argument("-e", "--ext", default=".png", help="output extension")
    parser.add_argument("PATH", nargs="+", help="intput filepath")
    return parser.parse_args()


def main():
    args = parse_args()
    for path in args.PATH:
        if path.endswith(".meta"):
            mt = Metatile.from_url(path)
            t = Tile.from_metatile(mt, ext=args.ext)
            print(t.filepath(args.basedir))
        else:
            t = Tile.from_url(path)
            mt = Metatile.from_tile(t)
            print(mt.filepath(args.basedir))


if __name__ == "__main__":
    main()
