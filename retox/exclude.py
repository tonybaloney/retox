# -*- coding: utf-8 -*-

from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    parser.add_argument(
        '--exclude',
        help="Exclude a pattern of files from being watched, expects RegEx")
