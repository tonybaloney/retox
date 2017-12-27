# -*- coding: utf-8 -*-
from asciimatics.screen import Screen


class MockScreen(Screen):
    buffer = []

    def __init__(self):
        super(MockScreen, self).__init__(100, 200, 1, True)

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
        self.buffer.append(text)
        assert isinstance(text, str)

    def _scroll(self, lines):
        pass

    def _clear(self):
        pass
