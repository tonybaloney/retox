# -*- coding: utf-8 -*-

from __future__ import absolute_import
from six.moves import cStringIO as StringIO
from mock import patch

import retox.__main__ as main

main.MAX_RUNS = 1

import curses
curses.COLORS = [curses.COLOR_BLACK]
curses.setupterm()

fc = [
    27394,
    3,
    19200,
    536872399,
    38400,
    38400,
    [b'\x04',
    b'\xff',
    b'\xff',
    b'\x7f',
    b'\x17',
    b'\x15',
    b'\x12',
    b'\x00',
    b'\x03',
    b'\x1c',
    b'\x1a',
    b'\x19',
    b'\x11',
    b'\x13',
    b'\x16',
    b'\x0f',
    b'\x01',
    b'\x00',
    b'\x14',
    b'\x00']]


def fake_std_in():
    class stdin(object):
        def fileno(*args):
            return 10
    return stdin()


def fake_scr():
    class scr(object):
        def getmaxyx(self):
            return (100, 100)

        def keypad(self, num):
            return 0

        def nodelay(self, num):
            return 0

        def refresh(self,):
            pass

    return scr()


@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stdin', new_callable=fake_std_in)
@patch('curses.cbreak')
@patch('curses.nocbreak')
@patch('curses.noecho')
@patch('curses.echo')
@patch('curses.endwin')
@patch('curses.initscr', fake_scr)
@patch('curses.curs_set')
@patch('curses.mousemask')
@patch('termios.tcgetattr', return_value=fc)
def test_main_entry_point(mocked_stdout, mocked_stdin, *args):
    '''
    Test full execution of the run
    '''
    ret = main.main(['-e', 'test'])
    assert ret == 0
