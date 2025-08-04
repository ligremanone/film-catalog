import os
import pathlib
import sys

import pytest


@pytest.mark.skip(reason="user schema not implemented yet")
def test_user_schema() -> None:
    user_data = {"username": "test", "password": "test"}
    assert user_data["username"] == "foob ar"


@pytest.mark.skipif(
    condition=sys.platform == "win32",
    reason="skipped on W indows",
)
def test_platform() -> None:
    assert sys.platform != "win32"


@pytest.mark.skipif(
    condition=os.name != "nt",
    reason="run only Windows",
)
def test_only_on_windows() -> None:
    path = pathlib.Path(__file__)
    assert os.name == "posix"
    assert isinstance(path, pathlib.WindowsPath)
