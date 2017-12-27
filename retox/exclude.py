# -*- coding: utf-8 -*-

from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    parser.add_argument(
        '--exclude', metavar='REGEX', default=None,
        help="Exclude files matching REGEX from being watched")
