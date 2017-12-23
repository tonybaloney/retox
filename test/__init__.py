# -*- coding: utf-8 -*-
from asciimatics.screen import Screen


class MockScreen(Screen):
    def __init__(self):
        super(MockScreen, self).__init__(100, 200, 1, True)
        self._buffer = []

    @classmethod
    def open(cls, unicode_aware=False):
        return MockScreen()

    def set_title(self, title):
        self.title = title

    def has_resized(self):
        pass

    def get_event(self):
        pass

    def close(self, restore=True):
        pass

    def _change_colours(self, colour, attr, bg):
        pass

    def _print_at(self, text, x, y, width):
        self._buffer.append(text)

    def _scroll(self, lines):
        pass

    def _clear(self):
        pass
