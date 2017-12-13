import asciimatics.widgets as widgets
from retox.log import retox_log
GLOBAL_COUNT = 0

TASK_NAMES = {
    'runtests': "Run Tests",
    'command': "Custom Command",
    'installdeps': "Install Dependencies",
    'installpkg': "Install Package",
    'inst': "Install",
    'inst-nodeps': "Install no-deps",
    'sdist-make': "Make sdist",
    'create': "Create",
    'recreate': "Recreate",
    'getenv': "Get environment"
}


class VirtualEnvironmentFrame(widgets.Frame):
    def __init__(self, screen, venv_name, venv_count, count):
        global GLOBAL_COUNT
        GLOBAL_COUNT = GLOBAL_COUNT + 1
        super(VirtualEnvironmentFrame, self).__init__(
            screen,
            screen.height // 2,
            screen.width // venv_count,
            x=count * (screen.width // venv_count) + 1,
            # on_load=self._reload_list,
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
                    8,
                    [],
                    name="Tasks",
                    label="Running"
                    # on_change=self._on_pick
                    )
        self._completed_view = widgets.ListBox(
                    8,
                    [],
                    name="Completed",
                    label="Completed"
                    # on_change=self._on_pick
                    )
        task_layout.add_widget(self._task_view)
        completed_layout.add_widget(self._completed_view)
        self.fix()

    def start(self, activity, action):
        self._task_view.options.append((TASK_NAMES.get(activity, activity), self.name))
        self._task_view.update(1)
        self._screen.force_update()
        self._screen.refresh()

    def stop(self, activity, action):
        try:
            self._task_view.options.remove((TASK_NAMES.get(activity, activity), self.name))
        except ValueError:
            retox_log.error("Could not find action %s in env %s" % (activity, self.name))
        self._completed_view.options.append((TASK_NAMES.get(activity, activity), self.name))
        self._completed_view.update(1)
        self._screen.force_update()
        self._screen.refresh()

    def update_action(self, action_name):
        if (activity, action) not in self._task_view.options:
            self._task_view.options.append((activity, action))
        self._screen.refresh()
