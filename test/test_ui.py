# -*- coding: utf-8 -*-

from __future__ import absolute_import

from asciimatics.screen import Screen
import retox.ui as ui


def test_create_layout():
    '''
    Test the creation of layouts with virtual environments
    '''
    screen = Screen(300, 400, 1, True)
    config = 1
    screens, scene, log, host = ui.create_layout(config, screen)
    assert screens is not None
