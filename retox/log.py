# -*- coding: utf-8 -*-
import logging


class RetoxLogging(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('retox.log')
        self.logger.addHandler(handler)

    def debug(self, *args):
        self.logger.debug(*args)

    def info(self, *args):
        self.logger.info(*args)

    def warning(self, *args):
        self.logger.warning(*args)

    def error(self, *args):
        self.logger.error(*args)

    def critical(self, *args):
        self.logger.critical(*args)

    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

retox_log = RetoxLogging()

logging.basicConfig(level=logging.ERROR)
