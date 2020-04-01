from pathlib import Path
import warnings
import numpy as np
import xarray as xr
import xgcm

from . import arakawa_points as akp
from .tools import open_file_multi, get_domcfg_points, mtc_nme


def open_domain_cfg(
    datadir=".",
    load_from_saved=True,
    save=True,
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
        The directory containing the 'domain_cfg_out' files
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
    domcfg = open_file_multi(datadir, file_prefix="domain_cfg_out")
    try:
        mask = open_file_multi(datadir, file_prefix="mesh_mask")
        #
        # keeping only dataarrays that contain the masks
        var_to_drop = [i for i in mask if not "mask" in i]
        for i in var_to_drop:
            mask = mask.drop_vars(i, error="ignore")
        #
        # adding the mask to domcfg
        domcfg = domcfg.combine_first(mask)
    except:
        # This means that #potentially# no mask file is provided
        mask = None
        warnings.warn("No mask file was found")
        #
    # This part is used to put the vars on the right point of the grid (e.g. T, U, V points)
    domcfg_points = get_domcfg_points()
    # Replacing the name of the coordinates
    for i in domcfg.keys():
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
    domcfg["z_c"].data = np.arange(len(domcfg["z_c"]))
    domcfg["z_f"] = domcfg["z_c"] - 0.5
    #
    domcfg.coords["x_c"] = (
        ["x_c",],
        domcfg.coords["x_c"],
        {"axis": "X"},
    )  # center point
    domcfg.coords["x_f"] = (
        ["x_f",],
        domcfg.coords["x_f"],
        {"axis": "X", "c_grid_axis_shift": 0.5},
    )  # right  point
    domcfg.coords["y_c"] = (
        ["y_c",],
        domcfg.coords["y_c"],
        {"axis": "Y"},
    )  # center point
    domcfg.coords["y_f"] = (
        ["y_f",],
        domcfg.coords["y_f"],
        {"axis": "Y", "c_grid_axis_shift": 0.5},
    )  # right  point
    domcfg.coords["z_c"] = (
        ["z_c",],
        domcfg.coords["z_c"],
        {"axis": "Z"},
    )  # center point
    domcfg.coords["z_f"] = (
        ["z_f",],
        domcfg.coords["z_f"],
        {"axis": "Z", "c_grid_axis_shift": -0.5},
    )  # left   point
    #

    if mask is not None:
        # Creating a fmaskutil if not existing
        if "fmaskutil" not in domcfg:
            domcfg["fmaskutil"] = domcfg["fmask"].isel({"z_c": 0}).copy()
        # Creating maskplots (TODO put this in a netcdf file)
        # T
        domcfg["tmaskplot"] = domcfg["tmask"].isel({"z_c": 0}).copy()
        # U
        domcfg["umaskplot"] = domcfg["umask"].isel({"z_c": 0}).copy()
        domcfg["umaskplot"].data = np.ones(domcfg["umaskplot"].shape)
        domcfg["umaskplot"][{"x_f": -1}] = 0
        domcfg["umaskplot"][{"y_c": -1}] = 0
        # V
        domcfg["vmaskplot"] = domcfg["vmask"].isel({"z_c": 0}).copy()
        domcfg["vmaskplot"].data = np.ones(domcfg["vmaskplot"].shape)
        domcfg["vmaskplot"][{"x_c": 0}] = 0
        domcfg["vmaskplot"][{"x_c": -1}] = 0
        domcfg["vmaskplot"][{"y_f": -1}] = 0
        # F
        domcfg["fmaskplot"] = domcfg["fmask"].isel({"z_c": 0}).copy()
        domcfg["fmaskplot"].data = np.ones(domcfg["fmaskplot"].shape)
        domcfg["fmaskplot"][{"x_f": -1}] = 0
        domcfg["fmaskplot"][{"y_f": -1}] = 0

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
    metric_diff = {
        "x_c": "e1t",
        "x_f": "e1u",
        "y_c": "e2t",
        "y_f": "e2v",
        "z_c": "e3t_0",
        "z_f": "e3w_0",
    }
    #
    domcfg = compute_metric_pos(domcfg, metric_diff=metric_diff)
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


def compute_metric_pos(domcfg, metric_pos={}, metric_diff={}):
    """
    Compute the metric of the points position and scale factors on domcfg
    Does not work on inner and outer points for the moment

    Arguments
    ---------
    domcfg : xarray.Dataset
        the domcfg dataset, containing coordinates for the different point positions (T, U, etc)
    metric_pos : dict
        dict with keys that are the name of the different coordinates, and the name of the
        variable in domcfg that contains the position
    metric_diff : dict
        idem, but with the scale factors, i.e. the size of the grid cells
        e.g. {'x_c':'e3t'}
        ! for a T point, the scale factor corresponds to the difference of position of the U points, in the x direction
    """
    # creating xgcm grid
    grid = xgcm.Grid(domcfg, periodic=False)

    if metric_pos == {} and metric_diff == {}:
        raise (ValueError("metric_pos and metric_diff can not be both empty"))
    # TODO add a test to see if we have enough info (pos OR diff OR (pos and diff)) ?

    metric_pos_rename = {}
    metric_diff_rename = {}
    # creating metrics that must be computed with the right name, using tools.mtc_nme
    for coord_nme in metric_pos.keys():
        metric_pos_rename[coord_nme] = mtc_nme(coord_nme)
        metric_diff_rename[coord_nme] = mtc_nme(coord_nme, diff=True)
    for coord_nme in metric_diff.keys():
        metric_pos_rename[coord_nme] = mtc_nme(coord_nme)
        metric_diff_rename[coord_nme] = mtc_nme(coord_nme, diff=True)

    # add metrics that already are existing to the variables, with the name change and remove them from dict so we don't need to compute them
    metric_diff_rename_bak = metric_diff_rename.copy()
    for coord_nme in metric_pos.keys():
        domcfg[metric_pos_rename[coord_nme]] = domcfg[metric_pos[coord_nme]]
        metric_pos_rename.pop(coord_nme)
    for coord_nme in metric_diff.keys():
        domcfg[metric_diff_rename[coord_nme]] = domcfg[metric_diff[coord_nme]]
        metric_diff_rename.pop(coord_nme)

    # TODO compute diff before, so we can used it after if necessary
    for coord_nme in metric_diff_rename.keys():
        raise (
            NotImplementedError(
                "Computation of scale factors from position is not implemented yet. Please compute scale factor of {} on your own".format(
                    coord_nme
                )
            )
        )

    # print('metric_pos_rename\n',metric_pos_rename)
    # compute the metric position from the differences
    for coord_nme in metric_pos_rename.keys():
        # print('\n********')
        # print('\n coord_nme\n', coord_nme)
        # e.g. coord_nme = 'x_c'
        # Find if this is a center, right or left point
        axis_nme = domcfg[coord_nme].attrs["axis"]  # e.g. 'X' or 'Y'
        # print('\n axis_nme \n', axis_nme)
        ax = grid.axes[axis_nme]
        (point_position, tmp) = ax._get_axis_coord(
            domcfg[coord_nme]
        )  # e.g. ('center', 'x_c')
        # print('\n (point_position, tmp) \n', (point_position, tmp))
        coord_shift_nme = ax.coords[ax._default_shifts[point_position]]  # e.g. 'x_f'
        diff_shift_nme = metric_diff_rename_bak[coord_shift_nme]  # e.g. 'x_f_diff'
        if point_position in ["inner", "outer"]:
            raise (
                NotImplementedError(
                    "The {} position has not been implemented yet".format(
                        point_position
                    )
                )
            )

        # cumsum of scale factors associated to the shift axis
        pos = grid.cumsum(
            domcfg[diff_shift_nme], axis=axis_nme, boundary="fill", fill_value=0
        )
        coords_of_pos_original = [i for i in pos.coords.keys()]
        # print('\n pos \n', pos)
        if "c_grid_axis_shift" in domcfg[coord_shift_nme].attrs:
            axis_shift = -domcfg[coord_shift_nme].attrs["c_grid_axis_shift"]
        else:
            # the shift is a center point => no shift here
            axis_shift = 0
        # print('\n axis_shift\n', axis_shift)
        # origin of the axis : 0 for 'right' and 'left' point (e.g. surface of the ocean, W point, 0)
        #          = [0,-0.5,0.5] *  scale factor at origin
        shift_origin = axis_shift * domcfg[diff_shift_nme].isel({coord_shift_nme: 0})
        # shift origin to 0 and then to the right value
        pos = pos - pos.isel({coord_nme: 0}) + shift_origin
        # print(' \n shifted')
        # print('\n pos \n', pos)
        # We need to drop all extra coordinates that come from the shifting
        for i in pos.coords.keys():
            if i not in coords_of_pos_original:
                pos = pos.drop(i)
        # print('\n dropping coordinates')
        # print('\n pos\n', pos)
        domcfg.coords[metric_pos_rename[coord_nme]] = pos
        # print(pos)

    return domcfg


def create_grid(domcfg):
    """Create a xgcm grid based on the domcfg"""
    grid = xgcm.Grid(
        domcfg,
        periodic=False,
        metrics={
            ("X",): ["e1t", "e1u"],
            ("Y",): ["e2t", "e2v"],
            ("Z",): ["e3t_0", "e3w_0"],
        },
    )
    return grid
