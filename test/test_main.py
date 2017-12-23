# -*- coding: utf-8 -*-

from __future__ import absolute_import

from mock import patch
import asciimatics.screen
from retox.__main__ import main
from . import MockScreen


def mock_screen_open(self, unicode_aware=False):
    return MockScreen()


@patch.object(asciimatics.screen.Screen, 'open', mock_screen_open)
def test_main_entry_point():
    '''
    Test full execution of the run
    '''
    ret = main([])
    assert ret == 0
