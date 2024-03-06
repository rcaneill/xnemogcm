# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)
![python versions](https://img.shields.io/pypi/pyversions/xnemogcm.svg)
![ci](https://github.com/rcaneill/xnemogcm/actions/workflows/ci.yml/badge.svg)
![documentation status](https://readthedocs.org/projects/xnemogcm/badge/?version=latest)
![pypi](https://badge.fury.io/py/xnemogcm.svg)
![anaconda badge](https://anaconda.org/conda-forge/xnemogcm/badges/version.svg)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

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
