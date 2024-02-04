# xnemogcm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5724577.svg)](https://doi.org/10.5281/zenodo.5724577)
![ci](https://github.com/rcaneill/xnemogcm/actions/workflows/ci.yml/badge.svg)
![pypi](https://badge.fury.io/py/xnemogcm.svg)
![anaconda badge](https://anaconda.org/conda-forge/xnemogcm/badges/version.svg)

Interface to open NEMO ocean global circulation model output dataset and create a xgcm grid.
NEMO 3.6, 4.0, and 4.2.0 are tested and supported. Any version between 3.6 and 4.2.0 should work,
but in case of trouble, [please open an issue](https://github.com/rcaneill/xnemogcm/issues).

This repository is mirrored at https://gitlab.com/open-ocean/xnemogcm.
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

See the [example](https://nbviewer.ipython.org/github/rcaneill/xnemogcm/blob/master/example/)
directory for some jupyter notebook examples.
xnemocgm is able to process xarray.Datasets (e.g. they could be retrieved from a remote server),
and can get information of the variables grid points with multiple options
(see [example/open_process_files.ipynb](https://nbviewer.ipython.org/github/rcaneill/xnemogcm/blob/master/example/open_process_files.ipynb).

### Note

`xnemogcm` is capable or recombining the domain_cfg and mesh_mask files output
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
To install all the dependencies, type `poetry install --with test,dev`
after cloning the directory. This will create a new virtual environment.
Typing `poetry shell` in the package directory will activate the virtual environment.

### About test data

Test data are based on the GYRE configuration, and produced by another repository:
[rcaneill/xnemogcm_test_data](https://github.com/rcaneill/xnemogcm_test_data).
Testing is built in a way that it is quite easy to add other nemo version to test.

### About notebooks examples

Sources for the notebooks are located in `src_example`. This is where to add / modify the
examples. A github action is set to automatically build the notebook according to
the latest version of the code, and publish them to `example` when commiting to master branch.


