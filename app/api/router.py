from api.controller import transform_image

router = {
    'POST': {
        '/image/transform': transform_image
    }
}
