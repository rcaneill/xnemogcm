from functools import partial

import os
from pathlib import Path
import numpy as np
import xarray as xr

from . import arakawa_points as akp
from .tools import open_file_multi
from .domcfg import open_domain_cfg


def nemo_preprocess(ds, domcfg):
    """
    Preprocess function for the nemo files.

    This function renames the time dimension 'time_counter' into 't', 'time_counter_bounds' into 't_bounds'.
    It removes the old 'nav_lat' and 'nav_lon' variables and sets the 'x', 'y', and 'z' dimensions
    into the correct dimension, depending on the grid point (e.g. ['x_c', 'y_c', 'z_c'] for T point).

    Parameters
    ----------
    ds : xarray.Dataset
        a dataset containing raw NEMO output data opened from a file (e.g. 'BASIN_grid_T.nc'),
        with the old names for the variables and dimensions (e.g. 'time_counter')
    domcfg : xarray.Dataset
        a dataset containing the domcfg data

    Returns
    -------
    xarray.Dataset containing the new dimension names, the correct grid point and attributes.
    """
    filename = ds.encoding["source"]
    point_type = filename[filename.index("grid_") + 5 : -3]
    point = akp.Point(point_type)
    for name in ds:
        ds[name].attrs[
            "arakawa_point_type"
        ] = point.point_type  # adding metadata with point type
    # get the name of the depth variable e.g. deptht, depthu, etc
    try:
        z_nme = [i for i in ds.dims.keys() if "depth" in i][0]
    except IndexError:
        # This means that there is no depth dependence of the data (surface data)
        z_nme = None
    x_nme = "x"  # could be an argument / metadata
    y_nme = "y"
    ds = ds.rename({x_nme: point.x, y_nme: point.y})
    if z_nme:
        ds = ds.rename({z_nme: point.z})
    # setting z_c/z_f/x_c/etc to be the same as in domcfg
    points = [point.x, point.y]
    if z_nme:
        points += [point.z]
    for xyz in points:
        ds.coords[xyz] = domcfg[xyz]
    ds = ds.drop_vars(
        ["nav_lat", "nav_lon"],
        errors="ignore",
    )
    # rename time
    ds = ds.rename({"time_counter": "t", "time_counter_bounds": "t_bounds"})
    ds["t"].attrs["bounds"] = "t_bounds"
    return ds


def open_nemo(
    datadir=".",
    file_prefix="",
    domcfg=None,
    load_from_saved=False,
    save=False,
    saving_name=None,
    chunks=None,
    **kwargs_open
):
    """
    Open nemo dataset, and rename the coordinates to be conform to xgcm.Grid

    The filenames must finish with 'grid_X.nc', with X in
    ['T', 'U', 'V', 'W', 'UW', etc]

    Parameters
    ----------
    datadir : string or pathlib.Path
        The directory containing the 'domain_cfg_out' files
    file_prefix : string, optionnal
        Prefix of the files to open, if no prefix is given, will open
        all nemo files.
    domcfg : xarray.Dataset or None
        If given, the domcfg dataset,
        if *None*, will open the *domain_cfg_out* files.
    load_from_saved : bool, optionnal
        If the domcfg has already been openened and saved, it is possible
        read this file instead or computing it again from scratch
    save : bool, optionnal
        Whether to save the domcfg file or not
    saving_name : string,
        The name of the file to save in (will be saved in the *datadir*).
        If empty string is given, default will be 'xnemogcm.nemo.nc'
    chunks : dict
        The chunks to use when opening the files,
        e.g. chunks={'time_counter':10}
        /!\ chunks need to be provided with the old names of dimensions
        i.e. 'time_counter', 'x', etc
        For more complex chunking, you may want to open without any chunks and set them up afterward.
    kwargs_open : any other argument given to the xarray.open_mfdataset function
        e.g. parallel=True to use dask.delayed

    Returns
    -------
    nemo_ds : xarray.Dataset
        Dataset containing all outputed variables, set on the proper
        grid points (center, face, etc).
    """
    if domcfg is None:
        domcfg = open_domain_cfg(datadir, load_from_saved=load_from_saved, save=save)

    datadir = Path(
        datadir
    ).expanduser()  # expanduser replaces the '~' with '/home/$USER'

    if saving_name is None:
        if file_prefix == "":
            saving_name = "xnemogcm.nemo.nc"
        else:
            saving_name = "xnemogcm.nemo." + file_prefix + ".nc"
    saving_name = datadir / saving_name

    if load_from_saved and saving_name.exists():
        nemo_ds = xr.open_dataset(saving_name)
    else:
        files = [
            datadir / i
            for i in os.listdir(datadir)
            if "grid_" in i and i[-3:] == ".nc" and file_prefix in i
        ]
        nemo_ds = xr.open_mfdataset(
            files,
            compat="override",
            preprocess=partial(nemo_preprocess, domcfg=domcfg),
            chunks=chunks,
            **kwargs_open
        )
        # adding attributes
        nemo_ds.attrs["name"] = "NEMO dataset"
        if file_prefix:
            nemo_ds.attrs["name"] += " " + file_prefix
        nemo_ds.attrs[
            "description"
        ] = "Ocean grid variables, set on the proper positions"
        nemo_ds.attrs["title"] = "Ocean grid variables"

        if save:
            nemo_ds.to_netcdf(saving_name)

    return nemo_ds
