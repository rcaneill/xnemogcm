import pytest
import os
from pathlib import Path

TEST_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = TEST_PATH / "data"

nemo_version = ["4.0.0"]


@pytest.fixture
def data_path(request):
    if request.param == "4.0.0":
        return DATA_PATH / "4.0.0"


@pytest.fixture
def data_path_namelist():
    return DATA_PATH / "namelist"
