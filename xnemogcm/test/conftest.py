import pytest
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = TEST_PATH / "data"

nemo_versions = ["3.6", "4.0", "4.2.0"]


def pytest_generate_tests(metafunc):
    if "data_path" in metafunc.fixturenames:
        metafunc.parametrize(
            "data_path", [DATA_PATH / i for i in nemo_versions], ids=nemo_versions
        )


@pytest.fixture
def data_path_namelist():
    return DATA_PATH / "namelist"
