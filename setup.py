#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup

setup(
    name="pyosm",
    version="0.4",
    description="Library for building OSM tools",
    url="https://github.com/tierpod/pyosm",
    author="Pavel Podkorytov",
    authoer_email="pod.pavel@gmail.com",
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    packages=["pyosm"],
    install_requires=["requests"],
    # entry_points={
    #     "console_script": [
    #         "",
    #     ],
    # },
)
