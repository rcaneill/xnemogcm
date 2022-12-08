import pytest
from xnemogcm import open_nemo_and_domain_cfg
from xnemogcm.metrics import get_metrics, compute_missing_metrics

pytestmark = pytest.mark.parametrize("data_path", ["4.0.0"], indirect=True)


def test_get_metrics(data_path):
    p = data_path / "open_and_merge"
    ds = open_nemo_and_domain_cfg(nemo_files=p, domcfg_files=p)
    metrics = get_metrics(ds)
    metrics_theory = {
        ("X",): ["e1t", "e1u", "e1v", "e1f"],  # X distances
        ("Y",): ["e2t", "e2u", "e2v", "e2f"],  # Y distances
        ("Z",): ["e3t", "e3u", "e3v", "e3w"],  # Z distances
    }
    assert metrics == metrics_theory
    assert len(get_metrics(compute_missing_metrics(ds))[("Z",)]) == 8


def test_calculate_all_metrics(data_path):
    p = data_path / "open_and_merge"
    ds = open_nemo_and_domain_cfg(nemo_files=p, domcfg_files=p)
    ds_full_metrics = compute_missing_metrics(ds.copy())
    for i in ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"]:
        assert i in ds_full_metrics

    ds_full_metrics_0 = compute_missing_metrics(ds.copy(), time_varying=False)
    for i in ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"]:
        assert (i + "_0") in ds_full_metrics_0

    ds_full_metrics_0 = compute_missing_metrics(
        ds.copy().drop_vars(
            [
                "e3t",
                "e3u",
                "e3v",
                "e3f",
                "e3w",
                "e3uw",
                "e3vw",
                "e3fw",
                "e3w_0",
                "e3u_0",
                "e3v_0",
                "e3f_0",
                "e3uw_0",
                "e3vw_0",
            ],
            errors="ignore",
        ),
        time_varying=False,
    )
    for i in ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"]:
        assert (i + "_0") in ds_full_metrics_0

    ds_full_metrics = compute_missing_metrics(
        ds.copy().drop_vars(["e3u", "e3v", "e3w"], errors="ignore"), time_varying=True
    )
    for i in ["e3t", "e3u", "e3v", "e3f", "e3w", "e3uw", "e3vw", "e3fw"]:
        assert i in ds_full_metrics

    ds_full_metrics = compute_missing_metrics(ds.copy(), all_scale_factors=["e3vw"])
    assert "e3vw" in ds_full_metrics
    assert not "e3fw" in ds_full_metrics


def test_calculate_all_metrics_precision(data_path):
    """Should do some tests of precision of the calculated metrics"""
    pass
