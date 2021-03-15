from xnemogcm import open_domain_cfg, open_nemo
from xnemogcm.nemo import nemo_preprocess
import os
from pathlib import Path
import xarray as xr

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_open_nemo():
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
        load_from_saved=False,
        save=False,
        saving_name=None,
    )


def test_use_preprocess():
    """Test opening of one nemo file and preprocess it by hand"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    ds_raw = xr.open_dataset(
        TEST_PATH / "data/nemo/BASIN_grid_T.nc"
    )
    ds = nemo_preprocess(ds_raw, domcfg)
    assert "x_c" in ds
    assert "t" in ds
    assert ds.thetao.attrs["arakawa_point_type"] == "T"


def test_save_nemo():
    """Test saving of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    nemo_ds0 = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
        load_from_saved=False,
        save=True,
        saving_name=None,
    )
    nemo_ds1 = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
        load_from_saved=True,
        save=False,
        saving_name=None,
    )
    assert (nemo_ds0 == nemo_ds1).all()
