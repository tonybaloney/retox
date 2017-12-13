import asciimatics.widgets as widgets


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


class VirtualEnvironmentFrame(widgets.Frame):
    def __init__(self, screen, venv_name, venv_count, count):
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

        layout = widgets.Layout([10], fill_frame=True)
        self.add_layout(layout)
        self._task_view = widgets.ListBox(
                    widgets.Widget.FILL_FRAME,
                    list(HEIGHTS.items()),
                    name="Tasks",
                    # on_change=self._on_pick
                    )
        layout.add_widget(self._task_view)
        self.fix()

    def start(self, activity):
        # self._screen.print_at('Started %s' % (activity), self.start_col, HEIGHTS.get(activity, 20))
        self._screen.refresh()

    def stop(self, activity):
        # self._screen.print_at('Finished %s' % (activity), self.start_col, HEIGHTS.get(activity, 20))
        self._screen.refresh()

    def update_action(self, action_name):
        # self._screen.print_at(action_name, self.start_col, HEIGHTS[action_name])
        self._screen.refresh()
