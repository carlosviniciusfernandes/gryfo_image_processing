import pathlib

from subprocess import Popen, PIPE

from cv2 import imread, subtract

TEST_IMG = 'lenna'
IMG_FORMAT = 'png'


def test_image_transform_via_cli(IMG_DIR):
    expected_output_path = pathlib.Path((f'{IMG_DIR}/output/{TEST_IMG}#edge_detect#flip_horizontal.{IMG_FORMAT}'))

    process = Popen(
        ["python", "main.py", "transform", "-i", f'{IMG_DIR}/{TEST_IMG}.{IMG_FORMAT}', "-o", "edge_detect", 'flip_horizontal'], stdout=PIPE
    )
    process.wait()

    assert expected_output_path.exists()
    diff = subtract(imread(f'{IMG_DIR}/{TEST_IMG}_edges_flipped.{IMG_FORMAT}'), imread(str(expected_output_path)))
    try:
        assert diff.sum() == 0 # images are identical
    finally:
        expected_output_path.unlink()
