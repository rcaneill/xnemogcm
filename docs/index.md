# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)
![ci](https://github.com/rcaneill/xnemogcm/actions/workflows/ci.yml/badge.svg)
![pypi](https://badge.fury.io/py/xnemogcm.svg)
![anaconda badge](https://anaconda.org/conda-forge/xnemogcm/badges/version.svg)

Interface to open NEMO ocean global circulation model output dataset and create a xgcm grid.
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

`xnemocgm` is able to process xarray.Datasets (e.g. they could be retrieved from a remote server),
and can get information of the variables grid points with multiple options:
see [examples/open_process_files](examples/open_process_files).

`xnemogcm` is capable or recombining the domain_cfg and mesh_mask files output
by multiple processors,
the recombining tool from the NEMO toolbox is thus not needed here: see
[examples/recombing_mesh_mask_domain_cfg](examples/recombing_mesh_mask_domain_cfg).

`xnemogcm` has a minimum capability of computing missing metrics
(scale factors): see [examples/compute_metrics](examples/compute_metrics).


## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

Installation via conda:
```bash
conda install -c conda-forge xnemogcm
```
