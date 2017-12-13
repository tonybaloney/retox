# -*- coding: utf-8 -*-

import tox.session
import eventlet
from asciimatics.scene import Scene


from retox.ui import VirtualEnvironmentFrame
from retox.log import retox_log

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
        count = 0
        for env in session.config.envlist:
            self._env_screens[env] = VirtualEnvironmentFrame(
                self.screen,
                env,
                self._env_count,
                count)
            count = count + 1
        self._scene = Scene([frame for _, frame in self._env_screens.items()], -1, name="Retox")
        self.screen.set_scenes([self._scene], start_scene=self._scene)

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
            self.screen.draw_next_frame(repeat=False)

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
