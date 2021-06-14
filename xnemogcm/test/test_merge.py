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
    datadir_dom = TEST_PATH / "data/domcfg_1_file"
    datadir_nemo = TEST_PATH / "data/nemo"
    domcfg_kwargs = dict(datadir=datadir_dom)
    domcfg = open_domain_cfg(**domcfg_kwargs)
    nemo_kwargs = dict(
        datadir=datadir_nemo,
        domcfg=domcfg,
    )
    nemo_ds = open_nemo(**nemo_kwargs)
    ds = _merge_nemo_and_domain_cfg(nemo_ds, domcfg, linear_free_surface=False)
    assert "e3t" in ds
    assert "e3t_0" in ds
    assert "t" in ds.e3t.coords
    assert "e3f" not in ds
    ds2 = open_nemo_and_domain_cfg(
        nemo_files=datadir_nemo,
        domcfg_files=datadir_dom,
        nemo_kwargs=nemo_kwargs,
        domcfg_kwargs=domcfg_kwargs,
        linear_free_surface=False,
    )
    assert (ds == ds2).all()
    p = TEST_PATH / "data/open_and_merge"
    ds2 = open_nemo_and_domain_cfg(
        nemo_files=p, domcfg_files=p, linear_free_surface=False
    )
    assert (ds == ds2).all()


def test_merge_linear_free_surface():
    pass


def test_attributes():
    p = TEST_PATH / "data/open_and_merge"
    ds = open_nemo_and_domain_cfg(nemo_files=p, domcfg_files=p)
    assert ds.attrs


def test_add_coordinates():
    p = TEST_PATH / "data/open_and_merge"
    ds = open_nemo_and_domain_cfg(nemo_files=p, domcfg_files=p)
    assert "glamt" in ds.coords
    ds = open_nemo_and_domain_cfg(
        nemo_files=p, domcfg_files=p, domcfg_kwargs={"add_coordinates": False}
    )
    assert not "glamt" in ds.coords


def test_open_nemo_files_without_datadir():
    p = TEST_PATH / "data/open_and_merge"
    print('****\n'*10)
    ds = open_nemo_and_domain_cfg(nemo_files=p.glob('*_grid*.nc'), domcfg_files=p.glob('domain*.nc'))
    assert ds
