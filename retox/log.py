# -*- coding: utf-8 -*-
import logging
LEVEL = logging.DEBUG

class RetoxLogging(object):
    '''
    Create a special logging class that redirects stdout 
    so it doesnt interfere with the screen session
    Write logging output to a file retox.log
    '''

    def __init__(self):
        self.logger = logging.getLogger('retox')
        self.logger.propagate = False
        handler = logging.FileHandler('retox.log')
        self.logger.handlers = []
        self.logger.addHandler(handler)
        self.logger.level = LEVEL

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

logging.basicConfig(level=logging.ERROR)

retox_log = RetoxLogging()
