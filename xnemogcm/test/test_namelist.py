from xnemogcm import open_namelist
import os
from pathlib import Path
import pytest

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_open_namelist_cfg():
    """Test opening the namelist_cfg"""
    namcfg = open_namelist(TEST_PATH / "data/namelist", cfg=True, ref=False)
    assert "rn_e1_deg" in namcfg
    assert namcfg["cn_exp"] == "BASIN"
    assert "nn_it000" not in namcfg


def test_open_namelist_ref():
    """Test opening the namelist_ref"""
    namref = open_namelist(TEST_PATH / "data/namelist", cfg=False, ref=True)
    assert "rn_e1_deg" not in namref
    assert namref["cn_exp"] == "ORCA2"


def test_open_namelist_merge():
    """
    Test opening the namelist_ref and namelist_ref, merging and replacing
    with the values from namelist_cfg when necessary
    """
    namelist = open_namelist(TEST_PATH / "data/namelist")
    assert "rn_e1_deg" in namelist
    assert namelist["cn_exp"] == "BASIN"
    assert namelist["nn_it000"] == 1


def test_warning():
    """Test that warnings are raised"""
    with pytest.warns(UserWarning):
        open_namelist(TEST_PATH, cfg=True, ref=False)
    with pytest.warns(UserWarning):
        open_namelist(TEST_PATH, cfg=False, ref=True)
