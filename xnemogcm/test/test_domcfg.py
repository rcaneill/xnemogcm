from xnemogcm import open_domain_cfg
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_open_domcfg_1_file():
    """Test opening of 1 file"""
    open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=False, save=False,
    )


def test_open_domcfg_multi_files():
    """Test opening of multi files from processors"""
    open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_multi_files",
        load_from_saved=False,
        save=False,
    )


def test_open_domcfg_multi_files_mesh_mask():
    """Test opening of multi files from processors, using mesh_mask files"""
    open_domain_cfg(
        datadir=TEST_PATH / "data/mesh_mask_multi_files",
        load_from_saved=False,
        save=False,
    )


def test_save_domcfg_1_file():
    """Test that saving works"""
    open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=False, save=True,
    )


def test_open_from_save():
    """Test that the saved domcfg is the same as the original"""
    domcfg1 = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=False, save=True,
    )
    domcfg2 = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=True, save=False,
    )
    assert (domcfg1 == domcfg2).all()


def test_compare_domcfg_1_multi():
    domcfg_1 = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=False, save=False,
    )
    domcfg_multi = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_multi_files",
        load_from_saved=False,
        save=False,
    )
    assert (domcfg_1 == domcfg_multi).all()


def test_compare_domcfg_mesh_mask():
    """Test that the data of mesh_mask are the same as in domain_cfg_out"""
    domcfg_1 = open_domain_cfg(
        datadir=TEST_PATH / "data/domcfg_1_file", load_from_saved=False, save=False,
    )
    domcfg_multi = open_domain_cfg(
        datadir=TEST_PATH / "data/mesh_mask_multi_files",
        load_from_saved=False,
        save=False,
    )
    assert (domcfg_1 == domcfg_multi).all()
