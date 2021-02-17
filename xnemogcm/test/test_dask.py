from xnemogcm import open_domain_cfg, open_nemo
import os
from pathlib import Path

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
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_parallel():
    """Test opening of nemo files, with parallel option"""
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
        parallel=True,
    )
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_chunks():
    """Test opening of nemo files, with chunks"""
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
        chunks={"time_counter": 1},
    )
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None
    assert nemo_ds.chunks["t"] == (1, 1, 1)
