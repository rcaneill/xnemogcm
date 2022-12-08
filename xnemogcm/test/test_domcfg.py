import pytest
from xnemogcm import open_domain_cfg

pytestmark = pytest.mark.parametrize("data_path", ["4.0.0"], indirect=True)


def test_options_for_files(data_path):
    """Test options to provide files"""
    datadir = data_path / "domcfg_mesh_mask"
    # 1. Provide datadir and no files
    open_domain_cfg(datadir=datadir, files=None)
    open_domain_cfg(datadir=datadir, files="")
    open_domain_cfg(datadir=datadir, files=[])
    # 2. Provide datadir and files
    files = [
        "domain_cfg_out_0000.nc",
        "domain_cfg_out_0001.nc",
        "domain_cfg_out_0002.nc",
        "domain_cfg_out_0003.nc",
        "mesh_mask_0000.nc",
        "mesh_mask_0001.nc",
        "mesh_mask_0002.nc",
        "mesh_mask_0003.nc",
    ]
    open_domain_cfg(datadir=datadir, files=files)
    # 3. Don't provide datadir but files
    open_domain_cfg(datadir=None, files=datadir.glob("*domain*.nc"))
    open_domain_cfg(datadir="", files=datadir.glob("*domain*.nc"))
    open_domain_cfg(datadir=[], files=datadir.glob("*domain*.nc"))
    # 4. Don't provide anything => error
    try:
        open_domain_cfg(datadir=None, files=None)
    except FileNotFoundError:
        pass


def test_no_file_provided(data_path):
    """Test exception raised if no file is found"""
    try:
        open_domain_cfg(datadir=data_path)
    except FileNotFoundError:
        pass


def test_domcfg_meshmask(data_path):
    """Test merging domain_cfg_out and mesh_mask"""
    domcfg = open_domain_cfg(datadir=(data_path / "domcfg_mesh_mask"))
    assert "fmask" in domcfg


def test_open_domcfg_1_file(data_path):
    """Test opening of 1 file"""
    open_domain_cfg(datadir=(data_path / "domcfg_1_file"))


def test_add_coordinates(data_path):
    """Test that the lat/lon/depth variables are set as coordinates"""
    domcfg = open_domain_cfg(datadir=(data_path / "domcfg_1_file"))
    assert "glamt" in domcfg.coords
    assert "gphiu" in domcfg.coords
    assert "gdept_0" in domcfg.coords


def test_no_add_coordinates(data_path):
    """Test that the lat/lon/depth variables are set as coordinates"""
    domcfg = open_domain_cfg(
        datadir=(data_path / "domcfg_1_file"), add_coordinates=False
    )
    assert not "glamt" in domcfg.coords
    assert not "gphiu" in domcfg.coords
    assert not "gdept_0" in domcfg.coords


def test_open_domcfg_1_file_provide_files(data_path):
    """Test opening of 1 file"""
    open_domain_cfg(files=(data_path / "domcfg_1_file").glob("*domain_cfg_out*.nc"))


def test_open_domcfg_multi_files(data_path):
    """Test opening of multi files from processors"""
    open_domain_cfg(datadir=(data_path / "domcfg_multi_files"))


def test_open_domcfg_multi_files_mesh_mask(data_path):
    """Test opening of multi files from processors, using mesh_mask files"""
    open_domain_cfg(datadir=(data_path / "mesh_mask_multi_files"))


def test_compare_domcfg_1_multi(data_path):
    domcfg_1 = open_domain_cfg(datadir=(data_path / "domcfg_1_file"))
    domcfg_multi = open_domain_cfg(datadir=(data_path / "domcfg_multi_files"))
    assert domcfg_1.equals(domcfg_multi)


def test_compare_domcfg_mesh_mask(data_path):
    """Test that the data of mesh_mask are the same as in domain_cfg_out"""
    domcfg_1 = open_domain_cfg(datadir=(data_path / "domcfg_1_file"))
    domcfg_multi = open_domain_cfg(datadir=(data_path / "mesh_mask_multi_files"))
    assert (domcfg_1 == domcfg_multi).all()
