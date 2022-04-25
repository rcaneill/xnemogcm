from xnemogcm import open_domain_cfg, open_nemo
from xnemogcm.nemo import nemo_preprocess
import os
from pathlib import Path
import xarray as xr

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_options_for_files():
    """Test options to provide files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    datadir = TEST_PATH / "data/nemo"
    # 1. Provide datadir and no files
    open_nemo(datadir=datadir, files=None, domcfg=domcfg)
    open_nemo(datadir=datadir, files="", domcfg=domcfg)
    open_nemo(datadir=datadir, files=[], domcfg=domcfg)
    # 2. Provide datadir and files
    files = ["BASIN_grid_T.nc", "BASIN_grid_U.nc"]
    open_nemo(datadir=datadir, files=files, domcfg=domcfg)
    # 3. Don't provide datadir but files
    open_nemo(datadir=None, files=datadir.glob("*grid*.nc"), domcfg=domcfg)
    open_nemo(datadir="", files=datadir.glob("*grid*.nc"), domcfg=domcfg)
    open_nemo(datadir=[], files=datadir.glob("*grid*.nc"), domcfg=domcfg)
    # 4. Don't provide anything => error
    try:
        open_nemo(datadir=None, files=None, domcfg=domcfg)
    except FileNotFoundError:
        pass


def test_no_file_provided_or_wrong_name():
    """Test exception raised if no file is found"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    try:
        open_nemo(datadir=TEST_PATH, domcfg=domcfg)
    except FileNotFoundError:
        pass
    try:
        open_nemo(
            files=(TEST_PATH / "data/domcfg_1_file").glob("domain*"), domcfg=domcfg
        )
    except ValueError:
        pass


def test_open_nemo():
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
    )


def test_use_preprocess():
    """Test opening of one nemo file and preprocess it by hand"""
    domcfg = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file",
    )
    ds_raw = xr.open_dataset(TEST_PATH / "data/nemo/BASIN_grid_T.nc")
    ds_raw.encoding["source"] = "BASIN_grid_T.nc"
    ds = nemo_preprocess(ds_raw, domcfg)
    assert "x_c" in ds
    assert "t" in ds
