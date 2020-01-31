#!/usr/bin/env python
from setuptools import setup

DISTNAME = "xnemogcm"
VERSION = "0.0.0"
LICENSE = "MIT"
AUTHOR = "Romain Caneill"
AUTHOR_EMAIL = "romain.caneill@gu.se"
URL = "https://github.com/rcaneill/xnemogcm"
#CLASSIFIERS =
INSTALL_REQUIRES = ["xarray", "dask", "numpy", "xgcm"]

DESCRIPTION = "Interface to open NEMO global circulation model output dataset and create a xgcm grid."



def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name=DISTNAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=readme(),
    install_requires=INSTALL_REQUIRES,
    url=URL,
    packages=[DISTNAME],
)

