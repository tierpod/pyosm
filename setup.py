#!/usr/bin/python

# Always prefer setuptools over distutils
from setuptools import setup

setup(
    name="pymetatile",
    version="0.1",
    description="Metatile file encoder and decoder",
    url="https://github.com/tierpod/pymetatile",
    author="Pavel Podkorytov",
    authoer_email="pod.pavel@gmail.com",
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    packages=["pymetatile"],
    install_requires=["requests"],
    # entry_points={
    #     "console_script": [
    #         "",
    #     ],
    # },
)
