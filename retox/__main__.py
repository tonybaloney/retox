# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click
from tox.session import prepare
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from retox.service import RetoxService
from retox.log import retox_log



@click.command()
def main(args=None):
    retox_log.debug("Starting command")
    tox_args = prepare(args)
    screen = Screen.open()
    service = RetoxService(tox_args, screen)
    service.start()

    needs_update = True
    running = True
    screen.print_at('Status : Starting  ', 1, 1)
    screen.print_at('Commands : (q) quit (b) build (r) rebuild environments', 1, screen.height - 1)
    while running:
        if needs_update:
            screen.print_at('Status : Running  ', 1, 1)
            screen.refresh()
            service.run(tox_args.envlist)
            needs_update = False
        screen.print_at('Status : Waiting  ', 1, 1)
        screen.refresh()
        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('q'):
                running = False
            elif event.key_code == ord('b'):
                needs_update = True

    # TODO : Go back and start again when files have changed.
    retox_log.debug("Finished")
    screen.clear()
    screen.close(restore=True)

if __name__ == '__main__':
    main()
