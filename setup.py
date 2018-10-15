#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="pyosm",
    version="0.10",
    description="Library for building OSM tools",
    url="https://github.com/tierpod/pyosm",
    author="Pavel Podkorytov",
    author_email="pod.pavel@gmail.com",
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    scripts=["bin/osmtool_convert_path", "bin/osmtool_unpack_metatile",
             "bin/osmtool_convert_latlong", "bin/osmtool_unpack_mbtile"],
)
