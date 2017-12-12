# -*- coding: utf-8 -*-

import tox.session
import eventlet

from random import randint
from asciimatics.screen import Screen

from retox.log import retox_log


HEIGHTS = {
    'runtests': 4,
    'command': 5,
    'installdeps': 6,
    'installpkg': 7,
    'inst': 8,
    'inst-nodeps': 9,
    'sdist-make': 10,
    'create': 11,
    'recreate': 12
}

SHIFT = 20


class FakeTerminalWriter(object):
    '''
    Redirect TerminalWriter messages to a log file
    '''
    hasmarkup = True

    def sep(self, char, message, **kwargs):
        return '-'

    def line(self, msg, *args, **kargs):
        retox_log.debug("Captured from tox: " + msg)


class RetoxReporter(tox.session.Reporter):
    screen = None

    sortorder = ("runtests command installdeps installpkg inst inst-nodeps "
        "sdist-make create recreate".split())

    def __init__(self, session):
        super(RetoxReporter, self).__init__(session)
        self._env_count = len(session.config.envlist)
        self._actionmayfinish = set()

        # Override default reporter functionality
        self.tw = FakeTerminalWriter()

        self._env_screens = {}
        offset = 0
        for env in session.config.envlist:
            self._env_screens[env] = VirtualEnvironment(
                env,
                offset,
                self.screen)
            offset = offset + SHIFT

    def _loopreport(self):
        while 1:
            eventlet.sleep(0.2)
            updates = []
            ac2popenlist = {}
            for action in self.session._actions:
                for popen in action._popenlist:
                    if popen.poll() is None:
                        l = ac2popenlist.setdefault(action.activity, [])
                        l.append(popen)
                if not action._popenlist and action in self._actionmayfinish:
                    super(RetoxReporter, self).logaction_finish(action)
                    self._actionmayfinish.remove(action)

            for action_name in self.sortorder:
                try:
                    popenlist = ac2popenlist.pop(action_name)
                except KeyError:
                    continue

                for popen in popenlist:
                    name = getattr(popen.action.venv, 'name', "INLINE")
                    screen = self._env_screens.get(name, None)
                    if screen:
                        screen.update_action(action_name)

            assert not ac2popenlist, ac2popenlist

    def logaction_start(self, action):
        if action.venv is not None:
            retox_log.debug("Started: %s %s" % (action.venv.name, action.activity))
            self._env_screens[action.venv.name].start(action.activity)
        super(RetoxReporter, self).logaction_start(action)

    def logaction_finish(self, action):
        if action.venv is not None:
            retox_log.debug("Finished: %s %s" % (action.venv.name, action.activity))
            self._env_screens[action.venv.name].stop(action.activity)
        super(RetoxReporter, self).logaction_finish(action)


class VirtualEnvironment(object):
    def __init__(self, venv_name, start_col, screen):
        self.name = venv_name
        self.start_col = start_col
        self._screen = screen

        # Draw a box for the environment
        self._screen.fill_polygon([(start_col, 1),
                                   (start_col+SHIFT, 1),
                                   (start_col+SHIFT, 22),
                                   (start_col, 22)], colour=3, bg=4)
        self._screen.refresh()

    def start(self, activity):
        self._screen.print_at('Started %s' % (activity), self.start_col, HEIGHTS.get(activity, 20))
        self._screen.refresh()

    def stop(self, activity):
        self._screen.print_at('Finished %s' % (activity), self.start_col, HEIGHTS.get(activity, 20))
        self._screen.refresh()

    def update_action(self, action_name):
        # self._screen.print_at(action_name, self.start_col, HEIGHTS[action_name])
        self._screen.refresh()
