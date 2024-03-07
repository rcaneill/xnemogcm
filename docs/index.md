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

A full example of analysis of NEMO data with xgcm is provided on the [xgcm documentation website](https://xgcm.readthedocs.io/en/latest/xgcm-examples/04_nemo_idealized.html).


## Examples

#### 1. [Open and process NEMO output with Xarray](examples/open_process_files)
This example demonstrates how `xnemocgm` is able to open and process NEMO output as `xarray.Datasets` from an array of different storage locations. Its main ability is to provide multiple options for interpreting information about the variable grid points for use with `xgcm`.

#### 2. [Recombine NEMO output files](examples/recombing_mesh_mask_domain_cfg)
Two types of files related to the domain grid can be of use with NEMO: the `domain_cfg` files and the `mesh_mask` files. They are very similar, and any of them can be used by xnemogcm. If you are using a realistic (regional or global) configuration, they are provided as input files to NEMO so you should have these file. If you are using idealised configuration with analytical bathymetry, these files can be outputted by NEMO ([`ln_meshmask = .true.`](https://forge.nemo-ocean.eu/nemo/nemo/-/blob/4.2.0/cfgs/SHARED/namelist_ref?ref_type=tags#L80) or [`ln_write_cfg = .true.`](https://forge.nemo-ocean.eu/nemo/nemo/-/blob/4.2.0/cfgs/SHARED/namelist_ref?ref_type=tags#L92) in the namelist for the `mesh_mask` or the `domain_cfg`, respectively). 
If `mesh_mask` or `domain_cfg` files are outputted by NEMO, they will be split between each processor, i.e. each processor will output only a subset of the whole file that corresponds to the space domain that the processor is handling. A Fortran toolbox is provided in NEMO to recombine these split files into a unified one, however `xnemogcm` is able to recombine the `domain_cfg` and `mesh_mask` files. This removes the need to rely on the recombining tool from the Fortran NEMO toolbox.

#### 3. [Compute missing metrics](examples/compute_metrics)
This example showcases how `xnemogcm` can compute certain missing metrics (metrics are called scale factors in the NEMO community, and called metrics in the xgcm community).


## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

Installation via conda:
```bash
conda install -c conda-forge xnemogcm
```
