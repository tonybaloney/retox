# -*- coding: utf-8 -*-

from __future__ import absolute_import

from mock import patch
import asciimatics.screen
import retox.__main__ as main
from . import MockScreen

main.MAX_RUNS = 1
main.Screen = MockScreen


def test_main_entry_point():
    '''
    Test full execution of the run
    '''
    ret = main.main(['-e', 'test'])
    assert ret == 0
