#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyosmkit",
    version="0.11",
    description="Library for building OSM tools",
    url="https://github.com/tierpod/pyosmkit",
    author="Pavel Podkorytov",
    author_email="pod.pavel@gmail.com",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    scripts=["bin/osmtool_convert_path", "bin/osmtool_unpack_metatile",
             "bin/osmtool_convert_latlong", "bin/osmtool_unpack_mbtile"],
)
