import os
from pathlib import Path
import numpy as np
import xarray as xr

from . import arakawa_points as akp
from .tools import open_file_multi
from .domcfg import open_domain_cfg


def open_nemo(
    datadir=".",
    file_prefix="",
    domcfg=None,
    load_from_saved=False,
    save=False,
    saving_name=None,
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
        filenames = [
            i
            for i in os.listdir(datadir)
            if "grid_" in i and i[-3:] == ".nc" and file_prefix in i
        ]
        nemo_ds = xr.Dataset()
        for filename in filenames:
            point_type = filename[filename.index("grid_") + 5 : -3]
            point = akp.Point(point_type)
            ds = xr.open_dataset(datadir / filename)
            for name in ds:
                ds[name].attrs[
                    "arakawa_point_type"
                ] = point.point_type  # adding metadata with point type
            # get the name of the depth variable e.g. deptht, depthu, etc
            z_nme = [i for i in ds.dims.keys() if "depth" in i][0]
            x_nme = "x"  # could be an argument / metadata
            y_nme = "y"
            ds = ds.rename({x_nme: point.x, y_nme: point.y, z_nme: point.z})
            # setting z_c/z_f to be the same as in domcfg
            for xyz in [point.x, point.y, point.z]:
                ds.coords[xyz] = domcfg[xyz]
            # droppping 'time_centered_bounds' ## ,'time_centered_bounds'
            nemo_ds = nemo_ds.merge(
                ds.drop_vars(
                    [
                        "nav_lat",
                        "nav_lon",
                        "time_centered",
                        "time_centered_bounds",
                        "time_instant",
                        "time_instant_bounds",
                    ],
                    errors="ignore",
                )
            )
        # adding attributes
        nemo_ds.attrs["name"] = "NEMO dataset " + file_prefix
        nemo_ds.attrs[
            "description"
        ] = "Ocean grid variables, set on the proper positions"
        nemo_ds.attrs["title"] = "Ocean grid variables"
        # nemo_ds.attrs['Conventions'] = 'CF-1.6'   #TODO verify that every variable has an attrbute name, so we can put again the convention CF-1.6
        # rename time
        nemo_ds = nemo_ds.rename(
            {"time_counter": "t", "time_counter_bounds": "t_bounds"}
        )

        if save:
            nemo_ds.to_netcdf(saving_name)

    return nemo_ds
