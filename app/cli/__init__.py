import pathlib

import cli.transform as transform
import cli.serve as serve

dir = pathlib.Path(__file__).resolve().parent
files_in_basepath = dir.iterdir()
commands = [item.name.removesuffix('.py') for item in files_in_basepath if '__' not in item.name]
