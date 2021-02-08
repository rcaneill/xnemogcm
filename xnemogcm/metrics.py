_metrics = {
    ("X",): ["e1t", "e1u", "e1v", "e1f"],  # X distances
    ("Y",): ["e2t", "e2u", "e2v", "e2f"],  # Y distances
    ("Z",): ["e3t", "e3u", "e3v", "e3f", "e3w"],  # Z distances
}


def get_metrics(ds):
    """
    Return a dict with the available metrics, to be used with xgcm.Grid

    Parameters
    ----------
    ds : xarray.DataSet
        domain_cfg_out
        or DataSet returned by xnemogcm._merge_nemo_and_domain_cfg
        or Dataset returned by xnemogcm.open_nemo_and_domain_cfg
        Should contain the outputed metrics, in a standard format 'e3x'
        with x an arakawa point in lower case

    Returns
    -------
    metrics : dict
        dict understood by xgcm.Grid, metrics argument
    """
    metrics = _metrics.copy()
    for point in metrics.keys():
        for e in metrics[point]:
            if e not in ds:
                metrics[point].remove(e)
    return metrics
