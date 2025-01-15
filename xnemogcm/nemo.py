import re
import xarray as xr

from . import arakawa_points as akp
from .tools import _dir_or_files_to_files


def _get_point_type(filename, description):
    """
    Infers point type from filename and/or description
    """
    point_type_fn = None
    point_type_desc = None

    # Try with filename
    a = "|".join(akp.ALL_POINTS)
    m = re.search(f"grid_({a})", filename)
    if m:
        point_type_fn = m.groups()[0]

    # try with description
    m = re.search(f"ocean ({a}) grid", description)
    if m:
        point_type_desc = m.groups()[0]

    if point_type_fn is None and point_type_desc is None:
        raise ValueError(
            f'{filename} does not contain grid_X in its name, with X in ["T", "U", "V", ...] and has no description attribute'
        )
    elif point_type_fn is not None and point_type_desc is not None:
        if point_type_fn != point_type_desc:
            raise ValueError(
                f"found point type {point_type_fn} from filename but {point_type_desc} from description attribute"
            )
        else:
            point_type = point_type_fn
    else:
        if point_type_fn is not None:
            point_type = point_type_fn
        else:
            point_type = point_type_desc
    return point_type


def _is_depth_dim(i, attrs):
    if "depth" == i[:5]:
        return True
    if "long_name" not in attrs.keys():
        return False
    return attrs["long_name"][:8] == "Vertical" and attrs["long_name"][-6:] == "levels"


def nemo_preprocess(ds, domcfg, point_type=None):
    """
    Preprocess function for the nemo files.

    This function renames the time dimension 'time_counter' into 't', 'time_counter_bounds' into 't_bounds'.
    It removes the old 'nav_lat' and 'nav_lon' variables and sets the 'x', 'y', and 'z' dimensions
    into the correct dimension, depending on the grid point (e.g. ['x_c', 'y_c', 'z_c'] for T point).

    Parameters
    ----------
    ds : xarray.Dataset
        a dataset containing raw NEMO output data (e.g. opened from a netcdf file as 'BASIN_grid_T.nc'
        or opened from any other backend, zarr, etc),
        with the old names for the variables and dimensions (e.g. 'time_counter')
    domcfg : xarray.Dataset
        a dataset containing the domcfg data
    point_type: None or str in ['T', 'U', 'V', 'W', 'UW', 'VW', 'FW']
        The point type. If None, will be inferred from either filename or attribute

    Returns
    -------
    xarray.Dataset containing the new dimension names, the correct grid point and attributes.
    """
    to_rename = {}
    if point_type is None:
        point_type = _get_point_type(
            filename=ds.encoding.get("source", ""),
            description=ds.attrs.get("description", ""),
        )

    point = akp.Point(point_type)

    # the depth variable name can be either deptht, depthu, etc
    # or grid_T_3D_inner, etc
    all_z_nme = [i for i in ds.dims if _is_depth_dim(i, ds[i].attrs)]
    if len(all_z_nme) >= 1:
        z_nme = all_z_nme[0]
        ds = ds.swap_dims({i: "depth_tmp_xnemogcm" for i in all_z_nme}).swap_dims(
            {"depth_tmp_xnemogcm": z_nme}
        )
    else:
        # This means that there is no depth dependence of the data (surface data)
        z_nme = None

    # get the name of the dimension along i e.g. x, x_grid_U, x_grid_U_inner etc
    x_nme = [i for i in ds.dims if "x_grid" in i or i == "x"]
    # get the name of the dimension along j e.g. y, y_grid_U, y_grid_U_inner etc
    y_nme = [i for i in ds.dims if "y_grid" in i or i == "y"]

    for x in x_nme:
        to_rename.update({x: point.x})

    for y in y_nme:
        to_rename.update({y: point.y})

    points = [point.x, point.y]
    if z_nme:
        to_rename.update({z_nme: point.z})
        points += [point.z]

    ds = ds.drop_vars(
        ["nav_lat", "nav_lon"],
        errors="ignore",
    )
    # rename time and space
    # get time_counter bounds
    time_b = ds["time_counter"].attrs.get("bounds")
    if time_b and time_b in ds:
        to_rename.update({"time_counter": "t", time_b: "t_bounds"})
    else:
        to_rename.update({"time_counter": "t"})
        if time_b not in ds:
            ds["time_counter"].attrs.pop("bounds")
            time_b = None
    ds = ds.rename(to_rename)
    if time_b and "t_bounds" in ds:
        ds["t"].attrs["bounds"] = "t_bounds"
    # setting z_c/z_f/x_c/etc to be the same as in domcfg
    ds = ds.assign_coords({i: domcfg[i] for i in points})
    # Assign the proper coordinates
    # 1st case: horizontal
    if z_nme:
        p = set(points[:2])
    else:
        p = set(points)
    coords = [i for i in domcfg.coords if set(domcfg.coords[i].dims) == p]
    ds = ds.assign_coords({i: domcfg[i] for i in coords})
    # 2nd case vertical
    if z_nme:
        p = set(points)
        coords = [i for i in domcfg.coords if set(domcfg.coords[i].dims) == p]
        ds = ds.assign_coords({i: domcfg[i] for i in coords})
    return ds


def _check_position(ds, position, parallel=False):
    if position is not None:
        return position
    else:
        if parallel:
            from dask import delayed

            get_point_type = delayed(_get_point_type)
        else:
            get_point_type = _get_point_type
        return get_point_type(filename="", description=ds.attrs.get("description", ""))


def process_nemo(positions, domcfg, parallel=False):
    """
    Process datasets from NEMO outputs and set coordinates and attributes.

    Parameters
    ----------
    positions : list of tuples
        [(ds1, 'X'), (ds2, 'Y'), (ds3, 'Z'), etc]
        Here 'X', 'Y', 'Z' must me the proper positions
        e.g. in ['T', 'U', 'V', 'W', 'UW', 'VW', 'FW']
        *OR*
        can be set to None. If None, then the corresponding dataset(s)
        must have the global attribute 'description' with value
        'ocean X grid variables' with X in ['T', 'U', ...]
    domcfg : xarray.Dataset
        the domcfg dataset
    parallel : bool, default False
        whether to use dask.delayed to process tasks in parallel

    Returns
    -------
    nemo_ds : xarray.Dataset
        Dataset containing all outputted variables, set on the proper
        grid points (center, face, etc).
    """
    if parallel:
        import dask

        # wrap preprocess with delayed
        preprocess = dask.delayed(nemo_preprocess)
    else:
        preprocess = nemo_preprocess
    """
    list_ds = []
    for X in positions.keys():
        for ds in positions[X]:
            list_ds.append((ds, X))
    """
    datasets = [
        preprocess(ds=ds, domcfg=domcfg, point_type=_check_position(ds, X, parallel))
        for (ds, X) in positions
    ]
    if parallel:
        # netcdf4 is not thread safe
        # https://github.com/pydata/xarray/issues/7079#issuecomment-1267477522
        with dask.config.set(scheduler="single-threaded"):
            (datasets,) = dask.compute(datasets)

    nemo_ds = xr.combine_by_coords(datasets, combine_attrs="drop_conflicts")
    # adding attributes
    nemo_ds.attrs["name"] = "NEMO dataset"
    nemo_ds.attrs["description"] = "Ocean grid variables, set on the proper positions"
    nemo_ds.attrs["title"] = "Ocean grid variables"
    return nemo_ds


def open_nemo(
    domcfg, datadir=None, files=None, chunks=None, parallel=False, **kwargs_open
):
    """
    Open nemo dataset, and rename the coordinates to be conform to xgcm.Grid

    The filenames must finish with 'grid_X.nc', with X in
    ['T', 'U', 'V', 'W', 'UW', 'VW', 'FW']
    *OR*
    the global attribute 'description' of each individual file must
    be 'ocean X grid variables' with X in ['T', 'U', ...]

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
    kwargs_open : any other argument given to the xarray.open_dataset function

    Returns
    -------
    nemo_ds : xarray.Dataset
        Dataset containing all outputted variables, set on the proper
        grid points (center, face, etc).
    """
    files = _dir_or_files_to_files(datadir, files, patterns=["*grid_*.nc"])
    if not files:
        raise FileNotFoundError("No output files are provided")
    #
    if parallel:
        from dask import delayed

        open_dataset = delayed(xr.open_dataset)
        get_point_type = delayed(_get_point_type)
    else:
        open_dataset = xr.open_dataset
        get_point_type = _get_point_type
    datasets = [
        open_dataset(
            f,
            chunks=chunks or {},
            **kwargs_open,
        )
        for f in files
    ]
    positions = [
        (
            ds,
            get_point_type(
                filename=str(f), description=ds.attrs.get("description", "")
            ),
        )
        for ds, f in zip(datasets, files)
    ]

    # Follow xarray's handling of open_mfdatasets
    try:
        out = process_nemo(positions=positions, domcfg=domcfg, parallel=parallel)
    except ValueError:
        for ds in datasets:
            ds.close()
        raise
    return out
