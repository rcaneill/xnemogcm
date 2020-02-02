# xnemogcm

Interface to open NEMO global circulation model output dataset and create a xgcm grid.

One can be interested by the [XORCA](https://github.com/willirath/xorca)
python package, that does a similar work for
all NEMO output grid. xnemogcm is designed to be more simple
and adapted to a simple idealized configuration.

# Usage

```python
from xnemogcm import open_domain_cfg, open_nemo
import xgcm

domcfg = open_domain_cfg(datadir='xnemogcm/test/data/domcfg_1_file')
nemo_ds = open_nemo(datadir='xnemogcm/test/data/nemo', domcfg=domcfg)
nemo_grid = xgcm.Grid(domcfg, periodic=False)
```

# Installation

Installation is possible via pip:
```bash
pip install git+https://github.com/rcaneill/xnemogcm.git@master
```