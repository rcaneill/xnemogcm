import pytest
from xnemogcm import open_domain_cfg, open_nemo
import xarray as xr


def test_open_nemo_surface(data_path):
    """Test opening of nemo surface files (no depth dimension)"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "surface_fields",
        domcfg=domcfg,
    )


def test_open_nemo_surface_coordinates(data_path):
    """Test opening of nemo surface files (no depth dimension)"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "surface_fields",
        domcfg=domcfg,
    )
    assert "glamt" in nemo_ds.sst.coords
    assert not ("gdept" in nemo_ds.sst.coords)
