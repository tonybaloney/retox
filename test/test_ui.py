# -*- coding: utf-8 -*-

from __future__ import absolute_import

import retox.ui as ui
from tox.config import parseconfig
from . import MockScreen


def test_create_layout():
    '''
    Test the creation of layouts with virtual environments
    '''
    screen = MockScreen()
    config = parseconfig([])
    screens, scene, log, host = ui.create_layout(config, screen)
    assert screens is not None
    assert len(screens) == len(config.envlist)
    assert len(log._effects) == len(screens)
