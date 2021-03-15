from xnemogcm import open_domain_cfg, open_nemo
import os
from pathlib import Path
import xarray as xr

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_open_nemo_surface():
    """Test opening of nemo surface files (no depth dimension)"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/surface_fields",
        domcfg=domcfg,
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
