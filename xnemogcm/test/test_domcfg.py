from xnemogcm import open_domain_cfg
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_no_file_provided():
    """Test exception raised if no file is found"""
    try:
        open_domain_cfg(datadir=TEST_PATH)
    except FileNotFoundError:
        pass


def test_domcfg_meshmask():
    """Test merging domain_cfg_out and mesh_mask"""
    domcfg = open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_mesh_mask"))
    assert "fmask" in domcfg


def test_open_domcfg_1_file():
    """Test opening of 1 file"""
    open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_1_file"))


def test_add_coordinates():
    """Test that the lat/lon/depth variables are set as coordinates"""
    domcfg = open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_1_file"))
    assert "glamt" in domcfg.coords
    assert "gphiu" in domcfg.coords
    assert "gdept_0" in domcfg.coords


def test_no_add_coordinates():
    """Test that the lat/lon/depth variables are set as coordinates"""
    domcfg = open_domain_cfg(
        datadir=(TEST_PATH / "data/domcfg_1_file"), add_coordinates=False
    )
    assert not "glamt" in domcfg.coords
    assert not "gphiu" in domcfg.coords
    assert not "gdept_0" in domcfg.coords


def test_open_domcfg_1_file_provide_files():
    """Test opening of 1 file"""
    open_domain_cfg(
        files=(TEST_PATH / "data/domcfg_1_file").glob("*domain_cfg_out*.nc")
    )


def test_open_domcfg_multi_files():
    """Test opening of multi files from processors"""
    open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_multi_files"))


def test_open_domcfg_multi_files_mesh_mask():
    """Test opening of multi files from processors, using mesh_mask files"""
    open_domain_cfg(datadir=(TEST_PATH / "data/mesh_mask_multi_files"))


def test_compare_domcfg_1_multi():
    domcfg_1 = open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_1_file"))
    domcfg_multi = open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_multi_files"))
    assert (domcfg_1 == domcfg_multi).all()


def test_compare_domcfg_mesh_mask():
    """Test that the data of mesh_mask are the same as in domain_cfg_out"""
    domcfg_1 = open_domain_cfg(datadir=(TEST_PATH / "data/domcfg_1_file"))
    domcfg_multi = open_domain_cfg(datadir=(TEST_PATH / "data/mesh_mask_multi_files"))
    assert (domcfg_1 == domcfg_multi).all()
