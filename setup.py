#!/usr/bin/env python
from setuptools import setup, find_packages

DISTNAME = "xnemogcm"
VERSION = "0.2.3"
LICENSE = "MIT"
AUTHOR = "Romain Caneill"
AUTHOR_EMAIL = "romain.caneill@gu.se"
URL = "https://github.com/rcaneill/xnemogcm"
# CLASSIFIERS =
INSTALL_REQUIRES = ["xarray", "netcdf4", "dask[array]"]
EXTRAS_REQUIRE = {"namelist": ["f90nml"]}
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
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    url=URL,
    packages=find_packages(exclude=["docs", "tests"]),
)
