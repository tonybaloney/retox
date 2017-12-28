# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse

import retox.exclude


def test_exclude_args():
    '''
    Test that `--exclude` flag is handled.
    '''
    parser = argparse.ArgumentParser()
    retox.exclude.tox_addoption(parser)
    args = parser.parse_args(['--exclude=\\.pyc$'])
    assert args.exclude == '\\.pyc$'
