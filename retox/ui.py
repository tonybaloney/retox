# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys

import asciimatics.widgets as widgets
from asciimatics.screen import Screen
from asciimatics.scene import Scene

from retox.log import retox_log

TASK_NAMES = {
    'runtests': u"Run Tests",
    'command': u"Custom Command",
    'installdeps': u"Install Dependencies",
    'installpkg': u"Install Package",
    'inst': u"Install",
    'inst-nodeps': u"Install no-deps",
    'sdist-make': u"Make sdist",
    'create': u"Create",
    'recreate': u"Recreate",
    'getenv': u"Get environment"
}


if sys.version_info.major == 2:
    RESULT_MESSAGES = {
        0: '[pass]',
        'commands failed': '[fail]'
    }
else:
    RESULT_MESSAGES = {
        0: u'✓',
        'commands failed': u'✗'
    }


class VirtualEnvironmentFrame(widgets.Frame):
    '''
    A UI frame for hosting the details of a virtualenv
    '''

    def __init__(self, screen, venv_name, venv_count, index):
        '''
        Create a new frame

        :param screen: The screen instance
        :type  screen: :class:`asciimatics.screen.Screen`

        :param venv_name: The name of this environment, e.g. py27
        :type  venv_name: ``str``

        :param venv_count: How many environments are there?
        :type  venv_count: ``int``

        :param index: which environment index is this
        :type  index: ``int``
        '''
        super(VirtualEnvironmentFrame, self).__init__(
            screen,
            screen.height // 2,
            screen.width // venv_count,
            x=index * (screen.width // venv_count) + 1,
            has_border=True,
            hover_focus=True,
            title=venv_name)
        self.name = venv_name
        self._screen = screen

        # Draw a box for the environment
        task_layout = widgets.Layout([10], fill_frame=False)
        self.add_layout(task_layout)
        completed_layout = widgets.Layout([10], fill_frame=False)
        self.add_layout(completed_layout)
        self._task_view = widgets.ListBox(
            10,
            [],
            name=u"Tasks",
            label=u"Running")
        self._completed_view = widgets.ListBox(
            10,
            [],
            name=u"Completed",
            label=u"Completed")
        task_layout.add_widget(self._task_view)
        completed_layout.add_widget(self._completed_view)
        self.fix()

    @staticmethod
    def create_screens(session, screen):
        _env_screens = {}
        count = 0
        for env in session.config.envlist:
            _env_screens[env] = VirtualEnvironmentFrame(
                screen,
                env,
                len(session.config.envlist),
                count)
            count = count + 1
        _scene = Scene([frame for _, frame in _env_screens.items()], -1, name="Retox")
        screen.set_scenes([_scene], start_scene=_scene)
        return _env_screens, _scene

    def start(self, activity, action):
        '''
        Mark an action as started

        :param activity: The virtualenv activity name
        :type  activity: ``str``

        :param action: The virtualenv action
        :type  action: :class:`tox.session.Action`
        '''
        try:
            self._start_action(activity, action)
        except ValueError:
            retox_log.debug("Could not find action %s in env %s" % (activity, self.name))
        self.refresh()

    def stop(self, activity, action):
        '''
        Mark a task as completed

        :param activity: The virtualenv activity name
        :type  activity: ``str``

        :param action: The virtualenv action
        :type  action: :class:`tox.session.Action`
        '''
        try:
            self._remove_running_action(activity, action)
        except ValueError:
            retox_log.debug("Could not find action %s in env %s" % (activity, self.name))
        self._mark_action_completed(activity, action)
        self.refresh()

    def finish(self, status):
        '''
        Move laggard tasks over

        :param activity: The virtualenv status
        :type  activity: ``str``
        '''
        retox_log.info("Completing %s with status %s" % (self.name, status))
        result = Screen.COLOUR_GREEN if not status else Screen.COLOUR_RED
        self.palette['title'] = (Screen.COLOUR_WHITE, Screen.A_BOLD, result)
        for item in list(self._task_view.options):
            self._task_view.options.remove(item)
            self._completed_view.options.append(item)
        self.refresh()

    def reset(self):
        '''
        Reset the frame between jobs
        '''
        self.palette['title'] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE)
        self._completed_view.options = []
        self._task_view.options = []
        self.refresh()

    def refresh(self):
        '''
        Refresh the list and the screen
        '''
        self._screen.force_update()
        self._screen.refresh()
        self._update(1)

    def _start_action(self, activity, action):
        self._task_view.options.append(self._make_list_item_from_action(activity, action))

    def _remove_running_action(self, activity, action):
        self._task_view.options.remove(self._make_list_item_from_action(activity, action))

    def _mark_action_completed(self, activity, action):
        name, value = self._make_list_item_from_action(activity, action)
        name = RESULT_MESSAGES.get(action.venv.status, str(action.venv.status)) + ' ' + name
        self._completed_view.options.append((name, value))

    def _make_list_item_from_action(self, activity, action):
        return TASK_NAMES.get(activity, activity), self.name
