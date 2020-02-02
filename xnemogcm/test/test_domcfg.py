from xnemogcm import open_domain_cfg


def test_open_domcfg_1_file():
    """Test opening of 1 file"""
    open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )


def test_open_domcfg_multi_files():
    """Test opening of multi files from processors"""
    open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_multi_files",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )


def test_save_domcfg_1_file():
    """Test that saving works"""
    open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_1_file",
        load_from_saved=False,
        save=True,
        saving_name=None,
    )


def test_open_from_save():
    """Test that the saved domcfg is the same as the original"""
    domcfg1 = open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_1_file",
        load_from_saved=False,
        save=True,
        saving_name=None,
    )
    domcfg2 = open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_1_file",
        load_from_saved=True,
        save=False,
        saving_name=None,
    )
    assert (domcfg1 == domcfg2).all()


def test_compare_domcfg_1_multi():
    domcfg_1 = open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_1_file",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    domcfg_multi = open_domain_cfg(
        datadir="xnemogcm/test/data/domcfg_multi_files",
        load_from_saved=False,
        save=False,
        saving_name=None,
    )
    assert (domcfg_1 == domcfg_multi).all()
