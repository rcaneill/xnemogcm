# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)

Interface to open NEMO ocean global circulation model output dataset and create a xgcm grid.


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

See the [example](https://nbviewer.ipython.org/github/rcaneill/xnemogcm/blob/master/example/)
directory for some jupyter notebook examples.
xnemocgm is able to process xarray.Datasets (e.g. they could be retrieved from a remote server),
and can get information of the variables grid points with multiple options
(see [example/open_process_files.ipynb](https://nbviewer.ipython.org/github/rcaneill/xnemogcm/blob/master/example/open_process_files.ipynb).

### Note

`xnemogcm` is capable or recombining the domain_cfg and mesh_mask files outputted
by multiple processors,
the recombining tool from the NEMO toolbox is thus not needed here, see
the [example/recombing_mesh_mask_domain_cfg.ipynb](https://nbviewer.ipython.org/github/rcaneill/xnemogcm/blob/master/example/recombing_mesh_mask_domain_cfg.ipynb)

## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

Installation via conda:
```bash
conda install -c conda-forge xnemogcm
```

## Requirements for dev

We use *poetry* to set up a virtual environment containing all
needed packages to run xnemogcm and the tests.
To install all the dependencies, type `poetry install -E dev`
after cloning the directory. This will create a new virtual environment.
Typing `poetry shell` in the package directory will activate the virtual environment.

## What's new

### v0.4.0 (2022-12-08)
* Optimize speed
* Add option to decode grid type from attributes
* Shift from pipenv and setupy.py to poetry
* Refactor data test to allow testing of multiple version of NEMO

### v0.3.4 (2021-06-15)
* Adding some example
* Bug fixes
* Add option to compute extra scale factors

### v0.3.2 - v0.3.3 (2021-05-05)
* By default adds the lat/lon/depth variables of domcfg as coordinates

### v0.3.1 (2021-05-04)
* Minor bug fix when merging
* better squeezing of time in domcfg + nemo v3.6 compatibility

### v0.3.0 (2021-04-13)
* Cleaning the backend
* Removing the saving options (that were useless and confusing)
* Minor bug fixes
* Tested with realistic regional configuration

### v0.2.3 (2021-03-15)
* Support for surface only files
* Reshaping the data files for the tests (dev)
