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
        NEMO domain_cfg_out dataset opened by the function xnemogcm.open_domain_cfg

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
    return ds


def open_nemo_and_domain_cfg(
    nemo_kwargs={}, domcfg_kwargs={}, datadir=None, linear_free_surface=False
):
    """
    Open nemo_ds and domcfg with open_nemo and open_domain_cfg and merge them with _merge_nemo_and_domain_cfg.

    See the respective functions docstrings for more details.

    Simple usage: ds = open_nemo_and_domain_cfg(datadir="/path/to/dir/with/nemo/and/domain_cfg/data")

    Arguments
    ---------
    nemo_kwargs : dict
        dict containing the parameters of the xnemogcm.open_nemo function
        e.g. {'datadir':'.', 'domcfg':None}
    domcfg_kwargs : dict
        dict containing the parameters of the xnemogcm.open_domain_cfg function
    datadir : string or pathlib.Path
        path of the nemo and domcfg data, if not provided in the dictionaries.
    linear_free_surface : bool
        True if linear free surface is used. Used by xnemogcm._merge_nemo_and_domain_cfg function
    """
    if datadir:
        nemo_kwargs["datadir"] = datadir
        domcfg_kwargs["datadir"] = datadir
    nemo_ds = open_nemo(**nemo_kwargs)
    domcfg = open_domain_cfg(**domcfg_kwargs)
    return _merge_nemo_and_domain_cfg(nemo_ds, domcfg, linear_free_surface)
