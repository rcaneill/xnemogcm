from xnemogcm import (
    open_domain_cfg,
    open_nemo,
    _merge_nemo_and_domain_cfg,
    open_nemo_and_domain_cfg,
)
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_merge_non_linear_free_surface():
    domcfg_kwargs = dict(
        datadir=TEST_PATH / "data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    domcfg = open_domain_cfg(**domcfg_kwargs)
    nemo_kwargs = dict(
        datadir=TEST_PATH / "data/nemo",
        domcfg=domcfg,
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    nemo_ds = open_nemo(**nemo_kwargs)
    ds = _merge_nemo_and_domain_cfg(nemo_ds, domcfg, linear_free_surface=False)
    assert "e3t" in ds
    assert "e3t_0" in ds
    assert "t" in ds.e3t.coords
    assert "e3f" not in ds
    ds2 = open_nemo_and_domain_cfg(
        nemo_kwargs, domcfg_kwargs, linear_free_surface=False
    )
    assert (ds == ds2).all()
    ds2 = open_nemo_and_domain_cfg(
        datadir=TEST_PATH / "data/open_and_merge", linear_free_surface=False
    )
    assert (ds == ds2).all()


def test_merge_linear_free_surface():
    pass


def test_attributes():
    ds = open_nemo_and_domain_cfg(datadir=TEST_PATH / "data/open_and_merge")
    assert ds.attrs
