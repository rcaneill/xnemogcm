import numpy as np
import xgcm
import xarray as xr
from pathlib import Path
import os


def safedrop(ds, names):
    """
    Drop safely names from ds, i.e. check for each name that it is an existing variable

    Arguments
    ---------
    ds : xarray.Dataset
    names : list
        Contain the list of variables to drop
    """
    names_to_drop = [i for i in names if i in ds]
    return ds.drop(names_to_drop)


def open_file_multi(pathdir, file_prefix):
    """
    Open and merge netcdf file created on each processor by NEMO (e.g. domain_cfg_out of mesh_mask
    """
    pathdir = Path(pathdir).expanduser()
    files = [i for i in os.listdir(pathdir) if file_prefix in i]
    data_ds = xr.open_dataset(pathdir / files[0])
    # Setting the x and y coordinates to be the gobal coordinates
    data_ds["x"] = data_ds.x + data_ds.attrs["DOMAIN_position_first"][0] - 1
    data_ds["y"] = data_ds.y + data_ds.attrs["DOMAIN_position_first"][1] - 1
    domposfir = data_ds.attrs["DOMAIN_position_first"]
    domposlas = data_ds.attrs["DOMAIN_position_last"]
    for i in files[1:]:
        ds = xr.open_dataset(pathdir / i)
        ds["x"] = ds.x + ds.attrs["DOMAIN_position_first"][0] - 1
        ds["y"] = ds.y + ds.attrs["DOMAIN_position_first"][1] - 1
        domposfir = np.min([domposfir, ds.attrs["DOMAIN_position_first"]], axis=0)
        domposlas = np.max([domposlas, ds.attrs["DOMAIN_position_last"]], axis=0)
        data_ds = ds.combine_first(data_ds)
    #
    data_ds = data_ds.isel(time_counter=0)
    data_ds.attrs["DOMAIN_position_first"] = domposfir
    data_ds.attrs["DOMAIN_position_last"] = domposlas
    data_ds.attrs["DOMAIN_number"] = 1
    data_ds.attrs["DOMAIN_number_total"] = 1
    data_ds.attrs["DOMAIN_size_local"] = data_ds.attrs["DOMAIN_size_global"]
    return data_ds


def get_domcfg_points():
    """The points are hard coded at hand to be sure to not introduce errors from the reading of the names"""
    domcfg_points = {
        "nav_lon": "T",
        "nav_lat": "T",
        "jpiglo": None,
        "jpjglo": None,
        "jpkglo": None,
        "jperio": None,
        "ln_zco": None,
        "ln_zps": None,
        "ln_sco": None,
        "ln_isfcav": None,
        "glamt": "T",
        "glamu": "U",
        "glamv": "V",
        "glamf": "F",
        "gphit": "T",
        "gphiu": "U",
        "gphiv": "V",
        "gphif": "F",
        "e1t": "T",
        "e1u": "U",
        "e1v": "V",
        "e1f": "F",
        "e2t": "T",
        "e2u": "U",
        "e2v": "V",
        "e2f": "F",
        "ff_f": "F",
        "ff_t": "T",
        "e3t_1d": "T",
        "e3w_1d": "W",
        "e3t_0": "T",
        "e3u_0": "U",
        "e3v_0": "V",
        "e3f_0": "F",
        "e3w_0": "W",
        "e3uw_0": "UW",
        "e3vw_0": "VW",
        "top_level": "T",
        "bottom_level": "T",
        "stiffness": "T",
        "gdept_0": "T",
        "gdepw_0": "W",
        "ht_0": "T",
        "hu_0": "U",
        "hv_0": "V",
        "tmask": "T",
        "umask": "U",
        "vmask": "V",
        "fmask": "F",
        "tmaskutil": "T",
        "umaskutil": "U",
        "vmaskutil": "V",
    }
    return domcfg_points


def mtc_nme(coord_name, diff=False, mask=False):
    """Return name of the coordinate metric of position (e.g. in meters), if *diff* is True, return name of scale factor"""
    if diff:
        return coord_name + "_dif"
    elif mask:
        return coord_name + "_msk"
    else:
        return coord_name + "_pos"
