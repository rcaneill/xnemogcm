# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)
![python versions](https://img.shields.io/pypi/pyversions/xnemogcm.svg)
![ci](https://github.com/rcaneill/xnemogcm/actions/workflows/ci.yml/badge.svg)
![documentation status](https://readthedocs.org/projects/xnemogcm/badge/?version=latest)
![pypi](https://badge.fury.io/py/xnemogcm.svg)
![anaconda badge](https://anaconda.org/conda-forge/xnemogcm/badges/version.svg)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![pyOpenSci](https://tinyurl.com/y22nb8up)](https://github.com/pyOpenSci/software-review/issues/155)

Interface to open NEMO ocean global circulation model output as an [Xarray](https://docs.xarray.dev/en/stable/) Dataset and create a [xgcm](https://xgcm.readthedocs.io/en/latest/) grid. 
NEMO 3.6, 4.0, and 4.2.0 are tested and supported. Any version between 3.6 and 4.2.0 should work,
but in case of trouble, [please open an issue](https://github.com/rcaneill/xnemogcm/issues).

If you wish to contribute but don't have a github account, send me an email with your questions or comments: `romain [dot] caneill [at] ens-lyon [.] org`

## Installation

For `conda`

```shell
conda install --channel conda-forge xnemogcm
```

for `pip`

```shell
pip install xnemogcm
```


## Usage

```python
from pathlib import Path
from xnemogcm import open_nemo_and_domain_cfg

ds = open_nemo_and_domain_cfg(
    nemo_files='/path/to/output/files',
    domcfg_files='/path/to/domain_cfg/mesh_mask/files'
)

# Interface with xgcm
from xnemogcm import get_metrics
import xgcm
grid = xgcm.Grid(ds, metrics=get_metrics(ds), periodic=False)
```

The full documentation is hosted online:
[https://xnemogcm.readthedocs.io/](https://xnemogcm.readthedocs.io/)

## Differences with existing tools

There exist tools in Fortran that ship with NEMO that are used to create domain files,
input fields, etc. They are however more used to produce configurations with the
necessary input files, than to analyse the outputs. So there is only one overlap with
xnemogcm, which is recombining the mesh_mask / domaincfg files,
when they have been outputted by different processors.

NEMO output files are outputted as netcdf so they can directly be opened by xarray.
However, what is missing is all grid information in the shape needed by
xgcm (COMODO convention). To solve this problem, another python package
exists: xorca. However, xorca is not developed any more and is less flexible than xnemogcm.
xnemogcm is meant to replace xorca, in addition to extending its functionality.
