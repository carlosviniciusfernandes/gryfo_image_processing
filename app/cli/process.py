import os
import pathlib

from argparse import _ArgumentGroup

from cv2 import imread, imwrite

from services.image_transformer import transform


def get_or_create_output_dir(img_path: pathlib.Path):
    output_path = f'{img_path.parent}/output/'
    if not os.path.exists(output_path):
       os.mkdir(output_path)
    return output_path


def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('process')
    parser.add_argument('-i', '--image',
        help='path of the image to be processed',
        type=str,
        metavar='',
        required=True
    )
    parser.add_argument('-o', '--operations',
        nargs='+',
        type=str,
        help=f'Operations to perform',
        metavar='',
        default=[]
    )


def run(*args, **kwargs) -> None:
    img_path: pathlib.Path = pathlib.Path(kwargs.get('image'))
    operations: list[str] = kwargs.get('operations')

    img = imread(str(img_path))
    result = transform(img, operations)

    format = img_path.suffix
    output_dir = get_or_create_output_dir(img_path)
    output_path = output_dir + img_path.name.replace(f'{format}', f"#{'#'.join(operations)}{format}")

    imwrite(output_path, result)
