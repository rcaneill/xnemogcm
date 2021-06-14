from xnemogcm import open_nemo_and_domain_cfg
from xnemogcm.metrics import get_metrics
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def test_get_metrics():
    p = TEST_PATH / "data/open_and_merge"
    ds = open_nemo_and_domain_cfg(nemo_files=p, domcfg_files=p)
    metrics = get_metrics(ds)
    metrics_theory = {
        ("X",): ["e1t", "e1u", "e1v", "e1f"],  # X distances
        ("Y",): ["e2t", "e2u", "e2v", "e2f"],  # Y distances
        ("Z",): ["e3t", "e3u", "e3v", "e3w"],  # Z distances
    }
    assert metrics == metrics_theory
