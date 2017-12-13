# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
import os
import click

from tox.session import prepare
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from retox.service import RetoxService

from retox.log import retox_log


@click.option('--watch', '-w', multiple=True)
@click.command()
def main(watch, args=None):
    retox_log.debug("Starting command")

    tox_args = prepare(args)
    screen = Screen.open()
    service = RetoxService(tox_args, screen)
    service.start()

    needs_update = True
    running = True
    screen.print_at('Status : Starting  ', 1, 1)
    if watch:
        screen.print_at('Watching : %s  ' % ', '.join(watch), 1, 2)

    screen.print_at('Commands : (q) quit (b) build', 1, screen.height - 1)

    _watches = [get_hashes(w) for w in watch]

    while running:
        if needs_update:
            screen.print_at('Status : Running  ', 1, 1)
            screen.refresh()
            out = service.run(tox_args.envlist)
            screen.print_at('Result : %s  ' % out , 1, 3)
            needs_update = False
        else:
            time.sleep(.5)

        if watch:
            # Refresh the watch folders and check for changes
            _new_watches = [get_hashes(w) for w in watch]
            changes = zip(_watches, _new_watches)
            needs_update = any(x != y for x, y in changes)
            _watches = _new_watches

        screen.print_at('Status : Waiting  ', 1, 1)
        screen.refresh()
        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('q'):
                running = False
            elif event.key_code == ord('b'):
                needs_update = True
            elif event.key_code == ord('r'):
                needs_update = True

    # TODO : Extra key for rebuilding tox virtualenvs
    retox_log.debug("Finished and exiting")
    screen.clear()
    screen.close(restore=True)


def get_hashes(path, ignore={'.pyc'}):
    '''
    Get a dictionary of file paths and timestamps
    '''
    out = {}
    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
        for file in files:
            for i in ignore:
                if not file.endswith(i):
                    pytime = os.path.getmtime(os.path.join(root, file))
                    out[os.path.join(root, file)] = pytime
    return out

if __name__ == '__main__':
    main()
