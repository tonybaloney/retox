# -*- coding: utf-8 -*-

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


RESULT_MESSAGES = {
    0: '[pass]',
    'commands failed': '[fail]',
    1: '[fail]'
}


def create_layout(config, screen):
    _env_screens = {}
    _log_screens = {}
    count = 0

    host_frame = RetoxFrame(screen, config)
    for env in config.envlist:
        _env_screens[env] = VirtualEnvironmentFrame(
            screen,
            env,
            len(config.envlist),
            count)
        _log_screens[env] = LogFrame(
            screen,
            env,
            len(config.envlist),
            count)
        count = count + 1
    _scene = Scene([host_frame] + [frame for _, frame in _env_screens.items()], -1, name="Retox")
    _log_scene = Scene([frame for _, frame in _log_screens.items()], duration=10, name="Logs")
    return _env_screens, _scene, _log_scene, host_frame


class RetoxRefreshMixin(object):
    def refresh(self):
        '''
        Refresh the list and the screen
        '''
        self._screen.force_update()
        self._screen.refresh()
        self._update(1)


class RetoxFrame(widgets.Frame, RetoxRefreshMixin):
    '''
    A UI frame for hosting the details of the overall host
    '''

    def __init__(self, screen, args):
        '''
        Create a new frame

        :param screen: The screen instance
        :type  screen: :class:`asciimatics.screen.Screen`

        :param args:  The tox arguments
        :type  args: ``object``
        '''
        super(RetoxFrame, self).__init__(
            screen,
            screen.height // 5,
            screen.width,
            x=0,
            y=0,
            has_border=True,
            hover_focus=True,
            title='Retox')
        self._screen = screen
        self._status = 'Starting'
        self._last_result = ''

        # Draw a box for the environment
        header_layout = widgets.Layout([10], fill_frame=False)
        self.add_layout(header_layout)

        self._status_label = widgets.Label('Status')
        header_layout.add_widget(self._status_label)

        self._last_result_label = widgets.Label('Last Result')
        header_layout.add_widget(self._last_result_label)

        if args.option.watch:
            self._watch_label = widgets.Label('Watching : %s  ' % ', '.join(args.option.watch))
            header_layout.add_widget(self._watch_label)

        self._commands_label = widgets.Label('Commands : (q) quit (b) build')
        header_layout.add_widget(self._commands_label)
        self.fix()
        self.refresh()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self._status_label.text = 'Status : {0}'.format(value)
        self.refresh()

    @property
    def last_result(self):
        return self._last_result

    @last_result.setter
    def last_result(self, value):
        self._last_result = value
        self._last_result_label.text = u'{0} : {1}'.format(
            'Result',
            RESULT_MESSAGES.get(value, str(value)))
        self.refresh()


class LogFrame(widgets.Frame, RetoxRefreshMixin):
    '''
    A UI frame for hosting the logs of a virtualenv
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
        super(LogFrame, self).__init__(
            screen,
            screen.height // 2,
            screen.width // venv_count,
            x=index * (screen.width // venv_count),
            has_border=True,
            hover_focus=True,
            title=venv_name)
        self.name = venv_name
        self._screen = screen

        # Draw a box for the environment
        layout = widgets.Layout([10], fill_frame=False)
        self.add_layout(layout)
        self._logs = widgets.ListBox(
            10,
            [],
            name="Logs",
            label="Logs")
        layout.add_widget(self._logs)
        self.fix()


class VirtualEnvironmentFrame(widgets.Frame, RetoxRefreshMixin):
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
            x=index * (screen.width // venv_count),
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
            name="Tasks",
            label="Running")
        self._completed_view = widgets.ListBox(
            10,
            [],
            name="Completed",
            label="Completed")
        task_layout.add_widget(self._task_view)
        completed_layout.add_widget(self._completed_view)
        self.fix()

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
