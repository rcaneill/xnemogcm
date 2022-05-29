from pathlib import Path
import numpy as np
import xarray as xr

from . import arakawa_points as akp
from .tools import get_domcfg_points, _dir_or_files_to_files


def domcfg_preprocess(ds):
    """
    Preprocess domcfg / meshmask files when needed to be recombined (= 1 file per processor)
    """
    if "z" in ds:
        ds = ds.rename({"z": "nav_lev"})
    if "DOMAIN_position_first" in ds.attrs.keys():
        (x0, y0) = ds.attrs["DOMAIN_position_first"]
        ds = ds.assign_coords({"x": ds.x + x0 - 1, "y": ds.y + y0 - 1})
    else:
        # This means that we are not merging multiple outputs from processors but e.g. a domain_cfg and a mesh_mask
        ds.coords["x"] = ds.x
        ds.coords["y"] = ds.y
    # We need to add "nav_lev" in the coordinates if not present
    if (not "nav_lev" in ds.coords) and ("nav_lev" in ds):
        ds.coords["nav_lev"] = ds["nav_lev"]
    return ds


def open_file_multi(files):
    """
    Open and merge netcdf file created on each processor by NEMO (e.g. domain_cfg of mesh_mask).
    If only one file is present, open and return it without any process.

    2 methods are accepted: 1) give a directory *pathdir* and a file prefix (e.g. 'domain_cfg')
    *file_prefix*, 2) give a list of file names *files*.
    """
    ds = xr.open_mfdataset(
        files,
        preprocess=domcfg_preprocess,
        combine_attrs="drop_conflicts",
        data_vars="minimal",
    )
    # data_vars='minimal' necessary to not add x and y dimensions into dimensionless variables
    # see https://github.com/pydata/xarray/issues/2064

    for i in ["time_counter", "t"]:
        if i in ds.dims:
            ds = ds.squeeze(i)
    for i in [
        "DOMAIN_position_first",
        "DOMAIN_position_last",
        "DOMAIN_number",
        "DOMAIN_number_total",
        "DOMAIN_size_local",
    ]:
        ds.attrs.pop(i, None)

    return ds


def _add_coordinates(domcfg):
    """
    If existing in the domcfg dataset, adds the lat/lon/depth variables as coordinates
    """
    coordinates = [
        "glamt",
        "glamu",
        "glamv",
        "glamf",
        "gphit",
        "gphiu",
        "gphiv",
        "gphif",
        "gdept_0",
        "gdepw_0",
        "gdept_1d",
        "gdepw_1d",
    ]
    for coord in coordinates:
        if coord in domcfg:
            domcfg.coords[coord] = domcfg[coord]
    return domcfg


def open_domain_cfg(datadir=None, files=None, add_coordinates=True):
    """
    Return a dataset containing all dataarrays of the domain_cfg*.nc / mesh_mask files.

    For that, open and merge all the datasets.
    The dataset is compatible with xgcm, the corresponding grid
    can be create through: xgcm.Grid(domcfg)

    Parameters
    ----------
    datadir : string or pathlib.Path or None
        The directory containing the 'domain_cfg' or 'mesh_mask' files
    files : list or iterator or None
        list of the file names that correspond to the domain_cfg and/or mesh_mask files,
        e.g. 'files=Path('path/to/data').glob('*my_domcfg*.nc') if your domain_cfg files are called
        'something_my_domcfg_00.nc' and 'something_my_domcfg_01.nc'
    add_coordinates : bool
        Whether to add the 'glamt', 'gphit', etc as coordinates of the dataset

    Returns
    -------
    domcfg : xarray.Dataset
        The domain configuration dataset, can be read by xgcm.
    """
    # TODO see dask arrays (chunk argument in xr.open_dataset)
    files = _dir_or_files_to_files(
        datadir, files, patterns=["*domain_cfg*.nc", "*mesh_mask*.nc"]
    )
    #
    if not files:
        raise FileNotFoundError("No 'domain_cfg' or 'mesh_mask' files are provided")
    #
    domcfg = open_file_multi(files=files)
    #
    # This part is used to put the vars on the right point of the grid (e.g. T, U, V points)
    domcfg_points = get_domcfg_points()
    # Replacing the name of the coordinates
    for i in domcfg.keys():
        if i not in domcfg_points.keys():
            continue
        if domcfg_points[i] is not None:
            point = akp.Point(domcfg_points[i])
            if "x" in domcfg[i].coords:
                domcfg[i] = domcfg[i].rename({"x": point.x})
            if "y" in domcfg[i].coords:
                domcfg[i] = domcfg[i].rename({"y": point.y})
            if "nav_lev" in domcfg[i].coords:
                domcfg[i] = domcfg[i].rename({"nav_lev": point.z})
    #
    domcfg["x_f"] = domcfg["x_c"] + 0.5
    domcfg["y_f"] = domcfg["y_c"] + 0.5
    domcfg = domcfg.assign_coords(z_c=np.arange(len(domcfg["z_c"])))
    domcfg["z_f"] = domcfg["z_c"] - 0.5
    #
    domcfg.coords["x_c"] = (
        [
            "x_c",
        ],
        domcfg.coords["x_c"].data,
        {"axis": "X"},
    )  # center point
    domcfg.coords["x_f"] = (
        [
            "x_f",
        ],
        domcfg.coords["x_f"].data,
        {"axis": "X", "c_grid_axis_shift": 0.5},
    )  # right  point
    domcfg.coords["y_c"] = (
        [
            "y_c",
        ],
        domcfg.coords["y_c"].data,
        {"axis": "Y"},
    )  # center point
    domcfg.coords["y_f"] = (
        [
            "y_f",
        ],
        domcfg.coords["y_f"].data,
        {"axis": "Y", "c_grid_axis_shift": 0.5},
    )  # right  point
    #
    domcfg.coords["z_c"] = (
        [
            "z_c",
        ],
        domcfg.coords["z_c"].data,
        {"axis": "Z"},
    )  # center point
    domcfg.coords["z_f"] = (
        [
            "z_f",
        ],
        domcfg.coords["z_f"].data,
        {"axis": "Z", "c_grid_axis_shift": -0.5},
    )  # left   point
    # Cleaning unused coordinates
    coordinates = [
        key for key in domcfg.coords.keys()
    ]  # all coordinates, including unused ones
    for var in domcfg.data_vars:
        for coord in domcfg[var].dims:
            if coord in coordinates:
                coordinates.pop(coordinates.index(coord))
    # coordinates now contains unused coordinates
    for coord in coordinates:
        domcfg = domcfg.drop_dims(coord, errors="ignore").drop_vars(
            coord, errors="ignore"
        )
    # adding variables as coordinates
    if add_coordinates:
        domcfg = _add_coordinates(domcfg)
    return domcfg
