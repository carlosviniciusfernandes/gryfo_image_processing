import io
import base64
import cv2
import numpy as np

from PIL import Image

from .exceptions import APIException
from .middleware import APIMiddleware
from core.image_transformer import transform


def _b64_to_ndarray(b64: str | bytes) -> np.ndarray:
    match type(b64).__name__:
        case 'bytes':
            img_arr = np.array(Image.open(io.BytesIO(b64)))
            return cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
        case 'str':
            img_bytes = base64.b64decode(b64)
            img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
            return cv2.imdecode(img_arr, flags=1)
        case _:
            raise APIException('Could not read image type', code=400)


def _buffer_to_output(buffer: bytes, format: str = 'bytes'):
    match format:
        case 'json':
            return {'image': f"data:image/png;base64,{base64.b64encode(buffer).decode('utf-8')}"}
        case _:
            #* bytes is the default
            return buffer


@APIMiddleware
def transform_image(image: str | bytes = '', operations: list[str] = [], output_format: str = '') -> dict:
    if not image:
        raise APIException('No image provided', code=400)

    new_image = transform(_b64_to_ndarray(image), operations)

    _, buffer = cv2.imencode('.png', new_image)

    return _buffer_to_output(buffer, output_format)
