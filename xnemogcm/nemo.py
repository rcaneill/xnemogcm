from functools import partial
import re
from pathlib import Path
import xarray as xr

from . import arakawa_points as akp
from .tools import _dir_or_files_to_files


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
    to_rename = {}
    
    point_type_fn = None
    point_type_desc = None
    
    # Try with filename
    filename = ds.encoding.get("source", "")
    all_points_str = a = '|'.join(akp.ALL_POINTS)
    m = re.search(f"grid_({a})", filename)
    if m:
        point_type_fn = m.groups()[0]

    # try with description
    desc = ds.attrs.get('description', '')
    m = re.search(f"ocean ({a}) grid", desc)
    if m:
        point_type_desc = m.groups()[0]        
        
    if point_type_fn is None and point_type_desc is None:
        raise ValueError(
            f'{filename} does not contain grid_X in its name, with X in ["T", "U", "V", ...] and has no description attribute'
        )
    elif point_type_fn is not None and point_type_desc is not None:
        if point_type_fn != point_type_desc:
            raise ValueError(
                f'found point type {point_type_fn} from filename but {point_type_desc} from description attribute'
            )
        else:
            point_type = point_type_fn
    else:
        if point_type_fn is not None:
            point_type = point_type_fn
        else:
            point_type = point_type_desc
            
    point = akp.Point(point_type)
    # get the name of the depth variable e.g. deptht, depthu, etc
    try:
        z_nme = [i for i in ds.dims.keys() if "depth" in i][0]
    except IndexError:
        # This means that there is no depth dependence of the data (surface data)
        z_nme = None
    x_nme = "x"
    y_nme = "y"
    to_rename.update({x_nme: point.x, y_nme: point.y})
    points = [point.x, point.y]
    if z_nme:
        to_rename.update({z_nme: point.z})
        points += [point.z]
    
    ds = ds.drop_vars(
        ["nav_lat", "nav_lon"],
        errors="ignore",
    )
    # rename time and space
    to_rename.update({"time_counter": "t", "time_counter_bounds": "t_bounds"})
    ds = ds.rename(to_rename)
    ds["t"].attrs["bounds"] = "t_bounds"
    # setting z_c/z_f/x_c/etc to be the same as in domcfg    
    ds = ds.assign_coords({i:domcfg[i] for i in points})
    return ds


def open_nemo(domcfg, datadir=None, files=None, chunks=None, **kwargs_open):
    """
    Open nemo dataset, and rename the coordinates to be conform to xgcm.Grid

    The filenames must finish with 'grid_X.nc', with X in
    ['T', 'U', 'V', 'W', 'UW', etc]

    Parameters
    ----------
    datadir : string or pathlib.Path
        The directory containing the nemo files
    domcfg : xarray.Dataset
        the domcfg dataset, e.g. opened with xnemogcm.open_domain_cfg
    files : list, optional
        List of the files to open
    chunks : dict
        The chunks to use when opening the files,
        e.g. chunks={'time_counter':10}
        /! chunks need to be provided with the old names of dimensions
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
    files = _dir_or_files_to_files(datadir, files, patterns=["*grid_*.nc"])
    if not files:
        raise FileNotFoundError("No output files are provided")
    #
    nemo_ds = xr.open_mfdataset(
        files,
        preprocess=partial(nemo_preprocess, domcfg=domcfg),
        chunks=chunks,
        **kwargs_open,
    )
    # adding attributes
    nemo_ds.attrs["name"] = "NEMO dataset"
    nemo_ds.attrs["description"] = "Ocean grid variables, set on the proper positions"
    nemo_ds.attrs["title"] = "Ocean grid variables"

    return nemo_ds
