# xnemogcm

Interface to open NEMO ocean global circulation model output dataset and create a xgcm grid.

One can be interested by the [XORCA](https://github.com/willirath/xorca)
python package, that does a similar work for
all NEMO output grid. xnemogcm is designed to be more simple
and adapted to a simple idealized configuration.

## Usage

```python
from xnemogcm import open_nemo_and_domain_cfg
ds = open_nemo_and_domain_cfg(datadir='/path/to/data')

# Interface with xgcm
from xnemogcm import get_metrics
import xgcm
grid = xgcm.Grid(ds, metrics=get_metrics(ds), periodic=False)
```

## Installation

Installation via pip:
```bash
pip3 install xnemogcm
```

## Requirements for dev

We use *pipenv* to set up a virtual environment containing all
needed packages to run xnemogcm and the tests.
To install all the dependencies, type `pipenv install`
after cloning the directory. This will create a new virtual environment.
Typing `pipenv shell` in the package directory will activate the virtual environment.

## What's new

### v0.2.3 (2021-03-15)
* Support for surface only files
* Reshaping the data files for the tests (dev)