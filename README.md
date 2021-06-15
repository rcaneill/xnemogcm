# xnemogcm

Interface to open NEMO ocean global circulation model output dataset and create a xgcm grid.

One can be interested by the [XORCA](https://github.com/willirath/xorca)
python package, that does a similar work for
all NEMO output grid. xnemogcm is designed to be more simple
and adapted to a simple idealized configuration.

## Usage

`xnemogcm` is capable or recombining the domain_cfg and mesh_mask files,
the recombining tool from the NEMO toolbox is thus not needed here.

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

## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

## Requirements for dev

We use *pipenv* to set up a virtual environment containing all
needed packages to run xnemogcm and the tests.
To install all the dependencies, type `pipenv install --dev`
after cloning the directory. This will create a new virtual environment.
Typing `pipenv shell` in the package directory will activate the virtual environment.

## What's new

### v0.3.4 (2021-06-15)
* Adding some exemple
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