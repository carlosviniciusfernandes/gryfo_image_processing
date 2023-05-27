import argparse

import ui.cli as cli


def load_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'Gryfo Image Processing',
        description = 'This is a package for image processing. Get started using the --help command'
    )
    parser.add_argument('-l', '--list', help='list available commands', action='store_true')
    subparsers = parser.add_subparsers(help='name of the commands for execution', metavar='command', dest='command')
    for command in cli.commands:
        getattr(cli, f'{command}').add_command(subparsers)
    return parser


if __name__ == "__main__":
    parser = load_argument_parser()
    args = parser.parse_args()

    if(args.list):
        message = "Available commands:"
        message += ''.join([f'\n\t{plot}' for plot in cli.commands])
        print(message)
        exit()

    if(args.command is None):
        print('Use -h or --help for usage help')
        exit()

    getattr(cli, f'{args.command}').run(**vars(args))
