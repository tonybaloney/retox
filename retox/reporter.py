# -*- coding: utf-8 -*-

import tox.session
import eventlet

from retox.log import retox_log, catch_exceptions

SHIFT = 20


class FakeTerminalWriter(object):
    '''
    Redirect TerminalWriter messages to a log file
    '''
    hasmarkup = True

    def sep(self, char, message, **kwargs):
        return '-'

    def line(self, msg, *args, **kargs):
        retox_log.info("tox: " + msg)


class RetoxReporter(tox.session.Reporter):
    '''
    A custom tox reporter designed for updating a live UI
    '''

    screen = None
    env_frames = None

    def __init__(self, session):
        '''
        Create a new reporter

        :param session: The Tox Session
        :type  session: :class:`tox.session.Session`
        '''
        super(RetoxReporter, self).__init__(session)
        self._actionmayfinish = set()

        # Override default reporter functionality
        self.tw = FakeTerminalWriter()

    @classmethod
    def set_env_frames(cls, env_frames):
        cls.env_frames = env_frames

    def _loopreport(self):
        '''
        Loop over the report progress
        '''
        while 1:
            eventlet.sleep(0.2)
            ac2popenlist = {}
            for action in self.session._actions:
                for popen in action._popenlist:
                    if popen.poll() is None:
                        lst = ac2popenlist.setdefault(action.activity, [])
                        lst.append(popen)
                if not action._popenlist and action in self._actionmayfinish:
                    super(RetoxReporter, self).logaction_finish(action)
                    self._actionmayfinish.remove(action)

            self.screen.draw_next_frame(repeat=False)

    @catch_exceptions
    def logaction_start(self, action):
        if action.venv is not None:
            retox_log.debug("Started: %s %s" % (action.venv.name, action.activity))
            self.env_frames[action.venv.name].start(action.activity, action)
        super(RetoxReporter, self).logaction_start(action)

    @catch_exceptions
    def logaction_finish(self, action):
        if action.venv is not None:
            retox_log.debug("Finished: %s %s" % (action.venv.name, action.activity))
            self.env_frames[action.venv.name].stop(action.activity, action)
        super(RetoxReporter, self).logaction_finish(action)

    def error(self, msg):
        # TODO : Raise errors in a panel
        self.logline("ERROR: " + msg, red=True)

    @catch_exceptions
    def startsummary(self):
        retox_log.debug("Starting summary")
        for frame_name, frame in self.env_frames.items():
            for venv in self.session.venvlist:
                if venv.name == frame_name:
                    try:
                        frame.finish(venv.status)
                    except AttributeError:
                        frame.finish(None)
                venv.finish()

        super(RetoxReporter, self).startsummary()

    def reset(self):
        self._actionmayfinish = set()

        for _, frame in self.env_frames.items():
            frame.reset()
