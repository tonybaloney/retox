# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from retox.__main__ import get_hashes


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