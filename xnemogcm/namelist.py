import os
from pathlib import Path
import xarray as xr
import warnings

import f90nml


def _warn_namelist_not_found(name):
    warnings.warn(f"Asked to open {name} file but file not found, using empty namelist")


def open_namelist(datadir=".", ref=True, cfg=True):
    """
    Open the namelist and store it into a xarray.Dataset
    """
    datadir = Path(
        datadir
    ).expanduser()  # expanduser replaces the '~' with '/home/$USER'

    namcfg = {}
    namref = {}
    ds = xr.Dataset()
    for (load, name) in [[ref, "namelist_ref"], [cfg, "namelist_cfg"]]:
        if load:
            try:
                namelist = f90nml.read(datadir / name)
                for nam in namelist.keys():
                    for i in namelist[nam]:
                        ds[i] = namelist[nam][i]
                        ds[i].attrs["namelist"] = nam
            except FileNotFoundError:
                _warn_namelist_not_found(name)

    return ds
