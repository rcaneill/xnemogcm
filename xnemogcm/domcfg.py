from pathlib import Path
import warnings
import numpy as np
import xarray as xr

from . import arakawa_points as akp
from .tools import open_file_multi, get_domcfg_points


def open_domain_cfg(
    datadir=".",
    load_from_saved=False,
    save=False,
    saving_name="xnemogcm.domcfg.nc",
    mercator_grid=False,
):
    """
    Return a dataset containing all dataarrays of the domain_cfg_out*.nc files.

    For that, open and merge all the datasets.
    The dataset is compatible with xgcm, the corresponding grid
    can be create through: xgcm.Grid(domcfg)

    Parameters
    ----------
    datadir : string or pathlib.Path
        The directory containing the 'domain_cfg_out' or 'mesh_mask' files
    load_from_saved : bool, optionnal
        If the domcfg has already been openened and saved, it is possible
        read this file instead or computing it again from scratch
    save : bool, optionnal
        Whether to save the domcfg file or not
    saving_name : string
        The name of the file to save in (will be saved in the *datadir*)
    mercator_grid : bool, optionnal
        If the domain is a simple basin on the sphere (Mercator)
        some more variabes will be created to simplify plots
        without using a sphere projection.

    Returns
    -------
    domcfg : xarray.Dataset
        The domain configuration dataset, can be read by xgcm.
    """
    # TODO see dask arrays (chunk argument in xr.open_dataset)
    datadir = Path(datadir).expanduser()
    #
    if saving_name is None:
        saving_name = "xnemogcm.domcfg.nc"
    saving_name = datadir / saving_name
    #
    if load_from_saved and saving_name.exists():
        domcfg = xr.open_dataset(saving_name)
        return domcfg
    #
    try:
        mask = open_file_multi(datadir, file_prefix="mesh_mask")
    except FileNotFoundError:
        mask = xr.Dataset()
    #
    try:
        domcfg = open_file_multi(datadir, file_prefix="domain_cfg_out")
    except FileNotFoundError:
        domcfg = xr.Dataset()
    #
    domcfg = domcfg.combine_first(mask)
    if not domcfg:
        raise FileNotFoundError("No 'domain_cfg_out' or 'mesh_mask' files are provided")
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
    # domcfg["z_c"].data = np.arange(len(domcfg["z_c"]))
    domcfg["z_f"] = domcfg["z_c"] - 0.5
    #
    domcfg.coords["x_c"] = (
        [
            "x_c",
        ],
        domcfg.coords["x_c"],
        {"axis": "X"},
    )  # center point
    domcfg.coords["x_f"] = (
        [
            "x_f",
        ],
        domcfg.coords["x_f"],
        {"axis": "X", "c_grid_axis_shift": 0.5},
    )  # right  point
    domcfg.coords["y_c"] = (
        [
            "y_c",
        ],
        domcfg.coords["y_c"],
        {"axis": "Y"},
    )  # center point
    domcfg.coords["y_f"] = (
        [
            "y_f",
        ],
        domcfg.coords["y_f"],
        {"axis": "Y", "c_grid_axis_shift": 0.5},
    )  # right  point
    domcfg.coords["z_c"] = (
        [
            "z_c",
        ],
        domcfg.coords["z_c"],
        {"axis": "Z"},
    )  # center point
    domcfg.coords["z_f"] = (
        [
            "z_f",
        ],
        domcfg.coords["z_f"],
        {"axis": "Z", "c_grid_axis_shift": -0.5},
    )  # left   point
    #

    if mask:
        # Creating a fmaskutil if not existing
        if "fmaskutil" not in domcfg:
            domcfg["fmaskutil"] = domcfg["fmask"].isel({"z_c": 0}).copy()

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
    #
    if mercator_grid:
        # add a variable for longitude = cos(latitude) for the plots
        for point in ["t", "u", "v", "f"]:
            domcfg["x_{}_plot".format(point.upper())] = (
                domcfg["glam{}".format(point)] - np.mean(domcfg["glam{}".format(point)])
            ) * xr.ufuncs.cos(
                xr.ufuncs.deg2rad(domcfg["gphi{}".format(point)])
            ) + np.mean(
                domcfg["glam{}".format(point)]
            )
            domcfg["y_{}_plot".format(point.upper())] = domcfg["gphi{}".format(point)]
    #
    if save:
        domcfg.to_netcdf(saving_name)
    #
    return domcfg
