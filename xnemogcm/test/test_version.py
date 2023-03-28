import toml
from pathlib import Path
import xnemogcm


def test_versions_are_in_sync():
    """Checks if the pyproject.toml and xnemogcm.__init__.py __version__ are in sync."""

    path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    pyproject = toml.loads(open(str(path)).read())
    pyproject_version = pyproject["tool"]["poetry"]["version"]

    package_init_version = xnemogcm.__version__

    assert package_init_version == pyproject_version
