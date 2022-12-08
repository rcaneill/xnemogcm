import pytest
from xnemogcm import open_domain_cfg, open_nemo

pytestmark = pytest.mark.parametrize("data_path", ["4.0.0"], indirect=True)


def test_open_nemo(data_path):
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_parallel(data_path):
    """Test opening of nemo files, with parallel option"""
    domcfg = open_domain_cfg(
        datadir=data_path / "domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
        parallel=True,
    )
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_chunks(data_path):
    """Test opening of nemo files, with chunks"""
    domcfg = open_domain_cfg(
        datadir=data_path / "domcfg_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
        chunks={"time_counter": 1},
    )
    for i in ["uo", "so", "thetao"]:
        assert nemo_ds[i].chunks is not None
    assert nemo_ds.chunks["t"] == (1, 1, 1)
