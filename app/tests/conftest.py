import pytest
import pathlib


dir = pathlib.Path(__file__).resolve().parent


@pytest.fixture(scope='session')
def IMG_DIR():
    return dir.joinpath('assets')
