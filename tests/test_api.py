
import pathlib
import requests

from cv2 import imread, subtract
from urllib3 import encode_multipart_formdata


TEST_IMG = 'lenna'
IMG_FORMAT = 'png'


def test_image_transfom_via_api__application_json(API_URL, LENNA_JSON, EDGE_FLIPPED_LENNA_JSON):
    headers = {'Content-Type': 'application/json'}
    payload = {
        **LENNA_JSON,
        'operations': ['flip_horizontal', 'edge_detect']
    }

    response = requests.post(f'{API_URL}/image/transform', json=payload, headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['image'] == EDGE_FLIPPED_LENNA_JSON['image']


def test_image_transfom_via_api__multipart_form_data(API_URL, IMG_DIR):
    image = f'{TEST_IMG}.{IMG_FORMAT}'
    fields = {
        "image": (f'{image}', open(f'{IMG_DIR}/{image}', 'rb').read(), 'image/png'),
        "operations": 'edge_detect,flip_horizontal'
    }
    payload, header = encode_multipart_formdata(fields)
    headers = {'Content-Type': header}

    response = requests.post(f'{API_URL}/image/transform', data=payload, headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'

    output_path = pathlib.Path((f'{IMG_DIR}/output/{TEST_IMG}#edge_detect#flip_horizontal.{IMG_FORMAT}'))
    with open(output_path, 'wb') as f:
        f.write(response.content)
    diff = subtract(imread(f'{IMG_DIR}/{TEST_IMG}_edges_flipped.{IMG_FORMAT}'), imread(str(output_path)))
    try:
        assert diff.sum() == 0 # images are identical
    finally:
        output_path.unlink()


def test_image_transfom_via_api__keeps_image_channels(API_URL, LENNA_JSON, BLURRED_LENNA_JSON):
    headers = {'Content-Type': 'application/json'}
    payload = {
        **LENNA_JSON,
        'operations': ['blur']
    }

    response = requests.post(f'{API_URL}/image/transform', json=payload, headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['image'] == BLURRED_LENNA_JSON['image']


def test_image_transfom_via_api__no_image_bad_request(API_URL):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'image': '',
        'operations': ['flip_horizontal', 'edge_detect']
    }

    response = requests.post(f'{API_URL}/image/transform', json=payload, headers=headers)

    assert response.status_code == 400
    assert 'No image provided' in response.json().get('message')


def test_image_transfom_via_api__empty_operations_bad_request(API_URL):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'image': 'blur',
        'operations': []
    }

    response = requests.post(f'{API_URL}/image/transform', json=payload, headers=headers)

    assert response.status_code == 400
    assert 'No operations' in response.json().get('message')
