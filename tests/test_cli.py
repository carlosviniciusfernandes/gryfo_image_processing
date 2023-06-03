import pathlib

from subprocess import Popen, PIPE

from cv2 import imread, subtract

TEST_IMG = 'lenna'
IMG_FORMAT = 'png'


def test_image_transform_via_cli__multiple_operations(IMG_DIR):
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

def test_image_transform_via_cli__keeps_color_channels(IMG_DIR):
    expected_output_path = pathlib.Path((f'{IMG_DIR}/output/{TEST_IMG}#blur.{IMG_FORMAT}'))

    process = Popen(
        ["python", "main.py", "transform", "-i", f'{IMG_DIR}/{TEST_IMG}.{IMG_FORMAT}', "-o", "blur"], stdout=PIPE
    )
    process.wait()

    assert expected_output_path.exists()
    diff = subtract(imread(f'{IMG_DIR}/{TEST_IMG}_blurred.{IMG_FORMAT}'), imread(str(expected_output_path)))
    try:
        assert diff.sum() == 0 # images are identical
    finally:
        expected_output_path.unlink()


def test_image_transform_via_cli__skip_unsupported_operation(IMG_DIR):
    expected_output_path = pathlib.Path((f'{IMG_DIR}/output/{TEST_IMG}#blur#not_supported.{IMG_FORMAT}'))

    process = Popen(
        ["python", "main.py", "transform", "-i", f'{IMG_DIR}/{TEST_IMG}.{IMG_FORMAT}', "-o", "blur", "not_supported"], stdout=PIPE
    )
    out, _ = process.communicate()
    assert f"Operation 'not_supported' not supported, skipping" in out.decode('utf-8')

    assert expected_output_path.exists()
    diff = subtract(imread(f'{IMG_DIR}/{TEST_IMG}_blurred.{IMG_FORMAT}'), imread(str(expected_output_path)))
    try:
        assert diff.sum() == 0 # images are identical
    finally:
        expected_output_path.unlink()


def test_image_transform_via_cli__no_image_found():
    process = Popen(
        ["python", "main.py", "transform", "-i", f'/wrong_path/{TEST_IMG}.{IMG_FORMAT}', "-o", "blur" ], stdout=PIPE,
    )
    out, _ = process.communicate()
    assert 'No image found' in out.decode('utf-8')
