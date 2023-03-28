import pytest
from xnemogcm import open_domain_cfg, open_nemo


def test_open_nemo(data_path):
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    for i in ["uoce", "soce", "toce"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_parallel(data_path):
    """Test opening of nemo files, with parallel option"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
        parallel=True,
    )
    for i in ["uoce", "soce", "toce"]:
        assert nemo_ds[i].chunks is not None


def test_open_nemo_chunks(data_path):
    """Test opening of nemo files, with chunks"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
        chunks={"time_counter": 1},
    )
    for i in ["uoce", "soce", "toce"]:
        assert nemo_ds[i].chunks is not None
    assert nemo_ds.chunks["t"] == (1,)
