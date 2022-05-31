import xarray as xr

from .tools import _dir_or_files_to_files


def _warn_namelist_not_found(name):
    import warnings

    warnings.warn(f"Asked to open {name} file but file not found, using empty namelist")


def open_namelist(datadir=None, files=None, ref=True, cfg=True):
    """
    Open the namelist and store it into a xarray.Dataset
    """
    import f90nml

    files = _dir_or_files_to_files(datadir, files, patterns=["namelist*"])

    if len(files) > 2:
        raise ValueError(
            f"Too many files given for the namelists, please check. Got {files}"
        )

    namcfg = {}
    namref = {}
    ds = xr.Dataset()

    for (load, name) in [[ref, "ref"], [cfg, "cfg"]]:
        if load:
            try:
                namelist = f90nml.read(*[i for i in files if name in str(i)])
                for nam in namelist.keys():
                    for i in namelist[nam]:
                        ds[i] = namelist[nam][i]
                        ds[i].attrs["namelist"] = nam
            except (FileNotFoundError, TypeError):
                _warn_namelist_not_found(name)

    return ds
