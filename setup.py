#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="pyosm",
    version="0.5",
    description="Library for building OSM tools",
    url="https://github.com/tierpod/pyosm",
    author="Pavel Podkorytov",
    authoer_email="pod.pavel@gmail.com",
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=["requests"],
    # entry_points={
    #     "console_script": [
    #         "",
    #     ],
    # },
)
