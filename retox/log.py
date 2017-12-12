# -*- coding: utf-8 -*-
import logging
import colorlog


class RetoxLogging(object):

    def __init__(self):

        self.logger = logging.getLogger('retox')
        self.logger.propagate = 0

        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(asctime)-2s %(log_color)s%(message)s",
            datefmt='%H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        self.reset()

    def reset(self):
        self.errors = 0

    def foundErrors(self):
        return self.errors > 0

    def debug(self, *args):
        self.logger.debug(*args)

    def info(self, *args):
        self.logger.info(*args)

    def warning(self, *args):
        self.logger.warning(*args)

    def error(self, *args):
        self.logger.error(*args)
        self.errors += 1

    def critical(self, *args):
        self.logger.critical(*args)
        self.errors += 1

    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

retox_log = RetoxLogging()

logging.basicConfig(level=logging.INFO)
