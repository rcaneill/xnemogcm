from xnemogcm import open_domain_cfg

def test_open_domcfg_1_file():
    open_domain_cfg(pathdir='xnemogcm/test/data/domcfg_1_file',
                    load_from_saved=False,
                    save=False,
                    saving_name=None)
    

