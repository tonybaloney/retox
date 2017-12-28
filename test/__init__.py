# -*- coding: utf-8 -*-
from asciimatics.screen import Screen


class MockScreen(Screen):
    buffer = []
    height = 100
    width = 600
    colours = []

    def __init__(self):
        super(MockScreen, self).__init__(MockScreen.height, MockScreen.width, 1, True)

    def _change_colours(self, colour, attr, bg):
        super(MockScreen, self)._change_colours(colour, attr, bg)

    def set_title(self, title):
        self.title = title

    def _print_at(self, text, x, y, width):
        self.buffer.append(text)
        assert isinstance(text, str)
        # super(MockScreen, self)._print_at(text, x, y, width)

    def has_resized(self):
        pass

    def get_event(self):
        pass

    def close(self, restore=True):
        pass

    def _scroll(self, lines):
        pass

    def _clear(self):
        pass

    def refresh(self):
        """
        Refresh the screen.
        """
        super(MockScreen, self).refresh()

    @staticmethod
    def _safe_write(msg):
        MockScreen.buffer.append(msg)
