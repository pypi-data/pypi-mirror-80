import argparse
import logging
import sys
from pathlib import Path

from mkproj.util import mkproj


def _parse_args(args: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "mkproj",
        description="Vanilla project skeleton generator.",
        epilog=f"NOTE: Project is created in cwd ({str(Path.cwd())}) !"
    )

    parser.add_argument(
        "-v",
        dest="loglevel",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        help="set logging level to debug (default: info)"
    )

    parser.add_argument(
        "-n",
        dest="name",
        action="store",
        type=str,
        required=True,
        help="project name"
    )

    parser.add_argument(
        "-d",
        dest="description",
        action="store",
        type=str,
        default="description-goes-here",
        help="project description"
    )

    parser.add_argument(
        "-p",
        dest="package",
        action="store",
        type=str,
        default=None,
        help="project package (default: project name)"
    )

    return parser.parse_args(args)


def _init_logging(loglevel):
    logging.basicConfig(
        level=loglevel,
        format="%(name)s: [%(levelname)s] %(message)s",
        stream=sys.stdout
    )


def main(args: list):
    args = _parse_args(args)
    _init_logging(args.loglevel)
    mkproj(Path.cwd(), args.name, args.description, args.package)


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
