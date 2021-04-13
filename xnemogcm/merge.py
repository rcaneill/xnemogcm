import types
from pathlib import Path
import numpy as np
import xarray as xr

from .arakawa_points import ALL_POINTS
from .nemo import open_nemo
from .domcfg import open_domain_cfg


def _merge_nemo_and_domain_cfg(nemo_ds, domcfg, linear_free_surface=False):
    """
    Return a merged array, containing the information of both nemo_ds and domcfg.

    If vertical scale factors 'e3t', 'e3u', 'e3v', 'e3w', 'e3f', etc are found
    in nemo_ds, this is interpreted as a type of z* coordinates (non-linear free surface),
    the final DataSet will contain both the 'e3x' and 'e3x_0' scale factors.
    If no vertical scale factors are found in nemo_ds, 'e3x' scale factors
    will be added in the DataSet. This allows you to always use the 'e3x'
    scale factors, both in linear free surface and in non-linear free surface
    (thickness weighted values needed in nemo_ds).

    Parameters
    ----------
    nemo_ds : xarray.DataSet
        NEMO output dataset opened by the function xnemogcm.open_nemo
    domcfg : xarray.DataSet
        NEMO domain_cfg dataset opened by the function xnemogcm.open_domain_cfg

    Returns
    -------
    ds : xarray.DataSet
        merged dataset containing both information of nemo_ds and domcfg
    """
    ds = xr.merge([nemo_ds, domcfg])
    attrs = domcfg.attrs
    attrs.update(nemo_ds.attrs)
    ds.attrs.update(attrs)
    if linear_free_surface:
        for point in ALL_POINTS:
            point = point.lower()
            if (f"e3{point}" not in ds) and (f"e3{point}_0" in domcfg):
                ds[f"e3{point}"] = domcfg[f"e3{point}_0"]
                ds[f"e3{point}"].attrs["WARNING"] = (
                    f"Warning: this scale factor has been copied from e3{point}_0,"
                    "it is not valid for thickness weighted data"
                )
    ds.attrs.pop("file_name", None)
    return ds


def open_nemo_and_domain_cfg(
    nemo_files,
    domcfg_files,
    nemo_kwargs={},
    domcfg_kwargs={},
    linear_free_surface=False,
):
    """
    Open nemo_ds and domcfg with open_nemo and open_domain_cfg and merge them with _merge_nemo_and_domain_cfg.

    See the respective functions docstrings for more details.

    2 methods are available for nemo files and domain_cfg/mesh_mask files: 1) provide a list of the files
    you want to open, 2) provide the path of the directories containing the files and xnemogcm will try
    to open as much files as it can.

    Arguments
    ---------
    nemo_files : list / generator or string / Path
        1) list / generator containing the nemo output files, or
        2) string / Path of the directory containing the nemo output files.
           Will open all files containing "grid_X" in their name, "X" being "T", "U", "V", "W", "F", etc
    domcfg_files : list / generator or string / Path
        1) list / generator containing the domain_cfg / mesh_mask files, or
        2) string / Path of the directory containing the domain_cfg / mesh_mask output files.
           Will open all files containing "domain_cfg" or "mesh_mask" in their name.
    nemo_kwargs : dict
        dict containing the parameters of the xnemogcm.open_nemo function
        e.g. {'chunks':{'time_counter':10}}
    domcfg_kwargs : dict
        dict containing the parameters of the xnemogcm.open_domain_cfg function
    linear_free_surface : bool
        True if linear free surface is used. Used by xnemogcm._merge_nemo_and_domain_cfg function
    """
    if isinstance(domcfg_files, (list, types.GeneratorType)):
        domcfg_kwargs["files"] = domcfg_files
    elif isinstance(domcfg_files, (str, Path)):
        domcfg_kwargs["datadir"] = domcfg_files

    if isinstance(nemo_files, (list, types.GeneratorType)):
        nemo_kwargs["files"] = nemo_files
    elif isinstance(nemo_files, (str, Path)):
        nemo_kwargs["datadir"] = nemo_files

    domcfg = open_domain_cfg(**domcfg_kwargs)
    nemo_kwargs["domcfg"] = domcfg
    nemo_ds = open_nemo(**nemo_kwargs)
    return _merge_nemo_and_domain_cfg(nemo_ds, domcfg, linear_free_surface)
