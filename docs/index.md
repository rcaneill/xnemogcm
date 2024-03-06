# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)
![ci](https://github.com/rcaneill/xnemogcm/actions/workflows/ci.yml/badge.svg)
![pypi](https://badge.fury.io/py/xnemogcm.svg)
![anaconda badge](https://anaconda.org/conda-forge/xnemogcm/badges/version.svg)

Interface to open NEMO ocean global circulation model output as an [Xarray](https://docs.xarray.dev/en/stable/) Dataset and create a [xgcm](https://xgcm.readthedocs.io/en/latest/) grid. 
NEMO 3.6, 4.0, and 4.2.0 are tested and supported. Any version between 3.6 and 4.2.0 should work,
but in case of trouble, [please open an issue](https://github.com/rcaneill/xnemogcm/issues).

If you wish to contribute but don't have a github account, send me an email with your questions or comments: `romain [dot] caneill [at] ens-lyon [.] org`

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

## Examples

#### 1. [Open and process NEMO output with Xarray](examples/open_process_files)
This example demonstrates how `xnemocgm` is able to open and process NEMO output as `xarray.Datasets` from an array of different storage locations. It also has multiple options for interpreting information about the variable grid points for use with `xgcm`. 

#### 2. [Recombine NEMO output files](examples/recombing_mesh_mask_domain_cfg)
The NEMO model outputs two files related to the domain grid that are relevant for interpretation by `xgcm`: the domain configuration file (`domain_cfg`) and the model mesh (`mesh_mask`). For most processing, it is necessary to combine these two files. This example shows how `xnemogcm` is able to recombine the `domain_cfg` and `mesh_mask` files, which removes the need to rely on the recombining tool from the Fortran NEMO toolbox.

#### 3. [Compute missing metrics](examples/compute_metrics)
This example showcases how `xnemogcm` can compute certain missing metrics related to scale factors.


## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

Installation via conda:
```bash
conda install -c conda-forge xnemogcm
```
