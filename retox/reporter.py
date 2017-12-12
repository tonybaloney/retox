# -*- coding: utf-8 -*-

import tox.session
import eventlet


class RetoxReporter(tox.session.Reporter):
    sortorder = ("runtests command installdeps installpkg inst inst-nodeps "
        "sdist-make create recreate".split())

    def __init__(self, session):
        super(RetoxReporter, self).__init__(session)
        self._actionmayfinish = set()

    def _loopreport(self):
        while 1:
            eventlet.sleep(0.2)
            msg = []
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
                sublist = []
                for popen in popenlist:
                    name = getattr(popen.action.venv, 'name', "INLINE")
                    sublist.append("%s" % (name))
                msg.append("%s %s" % (action_name, " ".join(sublist)))
            assert not ac2popenlist, ac2popenlist
            if msg:
                msg = "   ".join(msg)
                if len(msg) >= self.tw.fullwidth:
                    msg = msg[:self.tw.fullwidth-3]+".."
                self.tw.reline(msg)

    def logaction_start(self, action):
        if action.venv is not None:
            print("Started: " + action.venv.name)
        super(RetoxReporter, self).logaction_start(action)

    def logaction_finish(self, action):
        if action.venv is not None:
            print("Finished: " + action.venv.name)
        super(RetoxReporter, self).logaction_finish(action)
