#!/usr/bin/env python
from setuptools import setup, find_packages

DISTNAME = "xnemogcm"
VERSION = "0.1.2"
LICENSE = "MIT"
AUTHOR = "Romain Caneill"
AUTHOR_EMAIL = "romain.caneill@gu.se"
URL = "https://github.com/rcaneill/xnemogcm"
#CLASSIFIERS =
INSTALL_REQUIRES = ["xarray", "netcdf4", "dask[array]"]

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
    packages=find_packages(),
)

