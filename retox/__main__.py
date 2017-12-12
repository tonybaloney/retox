# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click
from tox.session import prepare

from retox.service import RetoxService
from retox.log import RetoxLogging

logger = RetoxLogging()


@click.command()
def main(args=None):
    logger.debug("Starting command")
    tox_args = prepare(args)
    service = RetoxService(tox_args, logger)
    service.start()
    service.run(tox_args.envlist)

if __name__ == '__main__':
    main()
