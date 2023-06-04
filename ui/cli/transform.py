import os
import pathlib

from argparse import _ArgumentGroup

from cv2 import imread, imwrite

from core.image_transformer import transform


def get_or_create_output_dir(img_path: pathlib.Path):
    output_path = f'{img_path.parent}/output/'
    if not os.path.exists(output_path):
       os.mkdir(output_path)
    return output_path


def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('transform')
    parser.add_argument('-i', '--image',
        help='path of the image to be processed/transformed',
        type=str,
        metavar='',
        required=True
    )
    parser.add_argument('-o', '--operations',
        nargs='+',
        type=str,
        help=f'Chain of operations to perform on the image. Available options: [flip_horizontal, flip_vertical, invert_colors, blur, edge_detect, draw_contours]',
        metavar='',
        required=True
    )


def run(*args, **kwargs) -> None:
    img_path: pathlib.Path = pathlib.Path(kwargs.get('image'))
    operations: list[str] = kwargs.get('operations')

    if not img_path.exists():
        print(f'path: {img_path} -> No image found.')
        return

    img = imread(str(img_path))
    result = transform(img, operations)

    format = img_path.suffix
    output_dir = get_or_create_output_dir(img_path)
    output_path = output_dir + img_path.name.replace(f'{format}', f"#{'#'.join(operations)}{format}")

    imwrite(output_path, result)
