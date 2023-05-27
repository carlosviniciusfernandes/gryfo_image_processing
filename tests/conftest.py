import json
import pytest
import pathlib

from multiprocessing import Process

from ui.cli.serve import run as serve

dir = pathlib.Path(__file__).resolve().parent


@pytest.fixture(scope='session')
def IMG_DIR() -> pathlib.Path | str:
    return dir.joinpath('assets')


@pytest.fixture(scope='session', autouse=True)
def TEST_SERVER() -> None:
    process = Process(target=serve)
    process.start()
    yield
    process.terminate()


@pytest.fixture(scope='session')
def API_URL() -> str:
    return 'http://127.0.0.1:8000'


@pytest.fixture(scope='session')
def LENNA_JSON(IMG_DIR) -> dict:
    with open(f'{IMG_DIR}/lenna.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def EDGE_FLIPPED_LENNA_JSON(IMG_DIR) -> dict:
    with open(f'{IMG_DIR}/lenna_edges_flipped.json', 'r') as f:
        return json.load(f)
