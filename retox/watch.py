# -*- coding: utf-8 -*-

from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    parser.add_argument(
        '-w', '--watch',
        action='append',
        help="Watch a folder for changes and rebuild when detected file changes/new files")
