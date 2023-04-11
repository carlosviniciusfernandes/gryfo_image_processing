import pathlib

from cv2 import imread, subtract

from cli.process import run as process_image_via_cli

TEST_IMG = 'lenna'
IMG_FORMAT = 'png'


def test_process_image_via_cli(IMG_DIR):
    expected_output_path = pathlib.Path((f'{IMG_DIR}/output/{TEST_IMG}#edge_detect#flip_horizontal.{IMG_FORMAT}'))
    process_image_via_cli(
        image=f'{IMG_DIR}/{TEST_IMG}.{IMG_FORMAT}',
        operations=['edge_detect', 'flip_horizontal'],
    )

    assert expected_output_path.exists()
    diff = subtract(imread(f'{IMG_DIR}/{TEST_IMG}_edges_flipped.{IMG_FORMAT}'), imread(str(expected_output_path)))
    assert diff.sum() == 0 # images are identical

    expected_output_path.unlink()


def test_process_image_via_api(IMG_DIR):
    pass