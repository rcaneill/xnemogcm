from collections import OrderedDict


all_scale_factors = ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"]

_metrics = {
    ("X",): ["e1t", "e1u", "e1v", "e1f"],  # X distances
    ("Y",): ["e2t", "e2u", "e2v", "e2f"],  # Y distances
    ("Z",): ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"],  # Z distances
}

dep_graph = OrderedDict(
    {
        "e3u": {"e3t": ["X"]},
        "e3w": {"e3t": ["Z"]},
        "e3v": {"e3t": ["Y"]},
        "e3f": {"e3t": ["X", "Y"]},
        "e3uw": {"e3w": ["X"]},
        "e3vw": {"e3w": ["Y"]},
        "e3fw": {"e3w": ["X", "Y"]},
    }
)


def compute_missing_metrics(
    ds, all_scale_factors=all_scale_factors, time_varying=True, periodic=False
):
    """
    Add all possible scale factors to the dataset.

    For the moment, e3t at least (or e3t_0) needs to be present in the dataset.
    May have some boundary issues.
    Will add the metrics to the given dataset. To avoid this, use a ds.copy()

    Parameters
    ----------
    ds : xarray.Dataset
        dataset containing the scale factors. Must be xgcm compatible (e.g. opened with xnemogcm)
    all_scale_factors : list
        list of the scale factors to compute (nothing is done for the scale factors
        already present in *ds*)
        Must be a sublist of: ['e3t', 'e3u', 'e3v', 'e3f', 'e3w', 'e3uw', 'e3vw', 'e3fw']
    time_varying : bool
        Whether to use the time varying scale factors (True) of the constant ones (False, 'e3x_0')

    Returns
    -------
    the new dataset with the scale factors added
    """
    try:
        import xgcm
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "xgcm is not installed, you need xgcm for this function"
        )
    from warnings import warn

    warn(
        "This function is in pre-phase. Do not expect a high precision, but a good estimate. Some boundary issues may arise."
    )

    grid = xgcm.Grid(ds, periodic=False)

    if not time_varying:
        all_scale_factors = [i + "_0" for i in all_scale_factors]

    for i in all_scale_factors:
        if i not in ds.variables:
            if time_varying:
                vertex = dep_graph[i]
            else:
                vertex = dep_graph[i[:-2]]
            for e3 in vertex.keys():
                if time_varying:
                    e3_nme = e3
                else:
                    e3_nme = e3 + "_0"
                if e3_nme in ds.variables:
                    # we stop at the first one matching
                    ds[i] = grid.interp(ds[e3_nme], vertex[e3], boundary="extend")
    return ds


def get_metrics(ds):
    """
    Return a dict with the available metrics, to be used with xgcm.Grid

    Parameters
    ----------
    ds : xarray.Dataset
        domain_cfg
        or DataSet returned by xnemogcm._merge_nemo_and_domain_cfg
        or Dataset returned by xnemogcm.open_nemo_and_domain_cfg
        Should contain the outputed metrics, in a standard format 'e3x'
        with x an arakawa point in lower case

    Returns
    -------
    metrics : dict
        dict understood by xgcm.Grid, metrics argument
    """
    metrics = {
        ("X",): ["e1t", "e1u", "e1v", "e1f"],  # X distances
        ("Y",): ["e2t", "e2u", "e2v", "e2f"],  # Y distances
        ("Z",): [
            "e3t",
            "e3u",
            "e3v",
            "e3f",
            "e3w",
            "e3uw",
            "e3vw",
            "e3fw",
        ],  # Z distances
    }
    metrics_output = {}
    for point in metrics.keys():
        m = []
        for e in metrics[point]:
            if e in ds.variables:
                m.append(e)
        metrics_output[point] = m
    return metrics_output
