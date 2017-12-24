# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
import os

from retox.__main__ import get_hashes
from retox.path import Path
import retox.watch


def test_get_simple_hashes():
    '''
    Test that the hash method returns back both files and files
    in subdirectories
    '''
    hashes = get_hashes('test/')
    assert 'test/test_watch/sub/file2.py' in hashes.keys()
    assert 'test/test_watch/file1.py' in hashes.keys()


def test_get_simple_hashes_subdir():
    '''
    Test that the hash method returns back only files
    in subdirectories
    '''
    hashes = get_hashes('test/test_watch/sub')
    assert 'test/test_watch/sub/file2.py' in hashes.keys()
    assert 'test/test_watch/file1.py' not in hashes.keys()


def test_get_simple_hashes_timestamps():
    '''
    Test that the hash method returns back a time
    '''
    hashes = get_hashes('test/')
    os_time = os.path.getmtime('test/test_watch/sub/file2.py')
    assert hashes['test/test_watch/sub/file2.py'] == os_time

    os_time = os.path.getmtime('test/test_watch/file1.py')
    assert hashes['test/test_watch/file1.py'] == os_time


def test_hashes_dont_include_dirs():
    files = get_hashes('test/')
    paths = (Path(f) for f in files)
    assert not any(p.is_dir() for p in paths)


def test_get_excluded_hashes():
    '''
    Test that the hash method excludes files properly.
    '''
    files = get_hashes('test/', exclude='.*watch.*').keys()

    # This file should be excluded because it matches the regex.
    assert 'test/test_watcher.py' not in files

    # This directory is excluded, so nothing under it should be present.
    assert 'test/test_watch/file1.py' not in files
    assert 'test/test_watch/sub/file2.py' not in files

    # And we of course should still see (for example) test_log.py.
    assert 'test/test_log.py' in files


def test_multiple_watch_args():
    '''
    Test that multiple `-w` flags are respected.
    '''
    parser = argparse.ArgumentParser()
    retox.watch.tox_addoption(parser)
    args = parser.parse_args(['-w', 'dir1', '-w', 'dir2'])
    assert 'dir1' in args.watch
    assert 'dir2' in args.watch
