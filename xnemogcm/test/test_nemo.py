import pytest
from xnemogcm import open_domain_cfg, open_nemo, process_nemo
from xnemogcm.nemo import nemo_preprocess
from xnemogcm.arakawa_points import ALL_POINTS
import xarray as xr


@pytest.mark.parametrize("parallel", [True, False])
@pytest.mark.parametrize("option", [0, 1, 2, 3])
def test_options_for_files(parallel, option, data_path):
    """Test options to provide files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    datadir = data_path / "nemo"
    if option == 0:
        # 0. Provide datadir and no files
        open_nemo(datadir=datadir, files=None, domcfg=domcfg, parallel=parallel)
        open_nemo(datadir=datadir, files="", domcfg=domcfg, parallel=parallel)
        open_nemo(datadir=datadir, files=[], domcfg=domcfg, parallel=parallel)
    elif option == 1:
        # 1. Provide datadir and files
        files = [
            "GYRE_1y_00010101_00011230_grid_T.nc",
            "GYRE_1y_00010101_00011230_grid_U.nc",
        ]
        open_nemo(datadir=datadir, files=files, domcfg=domcfg, parallel=parallel)
    elif option == 2:
        # 2. Don't provide datadir but files
        open_nemo(
            datadir=None,
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
        open_nemo(
            datadir="",
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
        open_nemo(
            datadir=[],
            files=datadir.glob("*grid*.nc"),
            domcfg=domcfg,
            parallel=parallel,
        )
    elif option == 3:
        # 3. Don't provide anything => error
        try:
            open_nemo(datadir=None, files=None, domcfg=domcfg, parallel=parallel)
        except FileNotFoundError:
            pass


def test_no_file_provided_or_wrong_name(data_path):
    """Test exception raised if no file is found"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    with pytest.raises(FileNotFoundError):
        open_nemo(datadir=data_path, domcfg=domcfg)
    with pytest.raises(ValueError):
        open_nemo(
            files=(data_path / "mesh_mask_1_file").glob("mesh_mask*"), domcfg=domcfg
        )


def test_open_nemo(data_path):
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )


def test_open_nemo_no_grid_in_filename(data_path):
    """Test opening of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    nemo_ds2 = open_nemo(
        files=(data_path / "nemo_no_grid_in_filename").glob("*.nc"),
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_process_nemo(data_path):
    """Test processing of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    positions = [
        (xr.open_dataset(data_path / f"nemo_no_grid_in_filename/{i}.nc"), i)
        for i in ["T", "U", "V", "W"]
    ]
    nemo_ds2 = process_nemo(
        positions=positions,
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_process_nemo_from_desc(data_path):
    """Test processing of nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    positions = [
        (
            xr.open_dataset(data_path / f"nemo_no_grid_in_filename/{i}.nc"),
            None,
        )
        for i in ["T", "U", "V", "W"]
    ]
    nemo_ds2 = process_nemo(
        positions=positions,
        domcfg=domcfg,
    )
    xr.testing.assert_identical(nemo_ds, nemo_ds2)


def test_use_preprocess(data_path):
    """Test opening of one nemo file and preprocess it by hand"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    ds_raw = xr.open_dataset(data_path / "nemo/GYRE_1y_00010101_00011230_grid_T.nc")
    ds_raw.encoding["source"] = "GYRE_1y_00010101_00011230_grid_T.nc"
    ds = nemo_preprocess(ds_raw, domcfg)
    assert "x_c" in ds
    assert "t" in ds


def test_coordinates_horizontal(data_path):
    """Test that coordinates are added to nemo files"""
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    assert "glamt" in nemo_ds.toce.coords
    assert "glamu" in nemo_ds.uoce.coords


def test_coordinates_vertical(data_path, request):
    """Test that coordinates are added to nemo files"""
    if request.node.callspec.id == "3.6":
        pytest.xfail(
            "Failing for nemo <= 3.6 as gdept_0 and gdepw_0 are not in mesh mask"
        )
    domcfg = open_domain_cfg(
        datadir=data_path / "mesh_mask_1_file",
    )
    nemo_ds = open_nemo(
        datadir=data_path / "nemo",
        domcfg=domcfg,
    )
    assert "gdept_0" in nemo_ds.toce.coords
