from pathlib import Path
from itertools import chain


def _dir_or_files_to_files(datadir=None, files=None, patterns=[]):
    """
    Return a list of files from combining datadir and files.

    Depending of the arguments, different cases happen:
    1. if datadir is given, and no files given:
       will return all the files in datadir that match the patterns
       chain(*[datadir.glob(pattern) for pattern in patterns])
    2. if datadir is given and files are given
       will concatenate : [datadir / file for file in files]
    3. if datadir is not given and files are given
       do nothing and return files
    4. if datadir is not given and files is not given
       raise an error

    datadir : string or pathlib.Path or None
    files : list or iterator or None
    patterns : list of strings
        the patterns that need to be matched
        e.g. patterns=['*domain_cfg*.nc', '*mesh_mask*.nc']
    """
    if isinstance(datadir, (str, Path)):
        datadir = Path(
            datadir
        ).expanduser()  # expanduser replaces the '~' with '/home/$USER'
    if not datadir:
        if not files:
            # error
            raise FileNotFoundError("No files to open, please provide datadir or files")
        else:
            # do nothing, the files are understood as ['/path/to/file1', '/path/to/file2', ...]
            pass
    else:
        datadir = Path(datadir).expanduser()
        if not files:
            # understood as taking all mesh_mask and domain_cfg files from datadir
            files = chain(*[datadir.glob(pattern) for pattern in patterns])
        else:
            # understood as taking [datadir / files[0], datadir / files[1], ...]
            files = [datadir / file for file in files]
    return list(files)


def get_domcfg_points():
    """The points are hard coded at hand to be sure to not introduce errors from the reading of the names"""
    domcfg_points = {
        "nav_lon": "T",
        "nav_lat": "T",
        "jpiglo": None,
        "jpjglo": None,
        "jpkglo": None,
        "jperio": None,
        "ln_zco": None,
        "ln_zps": None,
        "ln_sco": None,
        "ln_isfcav": None,
        "glamt": "T",
        "glamu": "U",
        "glamv": "V",
        "glamf": "F",
        "gphit": "T",
        "gphiu": "U",
        "gphiv": "V",
        "gphif": "F",
        "e1t": "T",
        "e1u": "U",
        "e1v": "V",
        "e1f": "F",
        "e2t": "T",
        "e2u": "U",
        "e2v": "V",
        "e2f": "F",
        "ff_f": "F",
        "ff_t": "T",
        "e3t_1d": "T",
        "e3w_1d": "W",
        "e3t_0": "T",
        "e3u_0": "U",
        "e3v_0": "V",
        "e3f_0": "F",
        "e3w_0": "W",
        "e3uw_0": "UW",
        "e3vw_0": "VW",
        "top_level": "T",
        "bottom_level": "T",
        "stiffness": "T",
        "gdept_0": "T",
        "gdepw_0": "W",
        "gdepu": "U",
        "gdepv": "V",
        "ht_0": "T",
        "hu_0": "U",
        "hv_0": "V",
        "tmask": "T",
        "umask": "U",
        "vmask": "V",
        "fmask": "F",
        "tmaskutil": "T",
        "umaskutil": "U",
        "vmaskutil": "V",
        "gdept_1d": "T",
        "gdepw_1d": "W",
        "mbathy": "T",
        "misf": "T",
        "isfdraft": "T",
    }
    return domcfg_points
