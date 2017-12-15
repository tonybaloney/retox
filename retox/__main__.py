# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import time
import os
import sys

from tox.session import prepare
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from retox.service import RetoxService

from retox.log import retox_log


def main(args):
    retox_log.debug("Starting command")
    retox_log.info("System stdout encoding is %s" % sys.stdout.encoding)

    # Use the Tox argparse logic
    tox_args = prepare(args)
    tox_args.option.resultjson = '.retox.json'
    # Custom arguments for watching directories
    watch = tox_args.option.watch
    if watch is None:
        watch = []

    # Start a service and a green pool
    screen = Screen.open(unicode_aware=True)
    service = RetoxService(tox_args, screen)
    service.start()

    needs_update = True
    running = True

    screen.print_at(u'Status : Starting  ', 1, 1)

    if watch:
        screen.print_at(u'Watching : %s  ' % ', '.join(watch), 1, 2)

    screen.print_at(u'Commands : (q) quit (b) build', 1, screen.height - 1)

    # Create a local dictionary of the files to see for differences
    _watches = [get_hashes(w) for w in watch]

    try:
        while running:
            if needs_update:
                screen.print_at(u'Status : Running  ', 1, 1)
                out = service.run(tox_args.envlist)
                screen.refresh()
                screen.print_at(u'Result : %s  ' % str(out), 1, 3)
                needs_update = False
            else:
                time.sleep(.5)

            if watch:
                # Refresh the watch folders and check for changes
                _new_watches = [get_hashes(w) for w in watch]
                changes = zip(_watches, _new_watches)
                needs_update = any(x != y for x, y in changes)
                _watches = _new_watches

            screen.print_at(u'Status : Waiting  ', 1, 1)
            screen.refresh()
            event = screen.get_event()
            if isinstance(event, KeyboardEvent):
                if event.key_code == ord('q'):
                    running = False
                elif event.key_code == ord('b'):
                    needs_update = True
                elif event.key_code == ord('r'):
                    needs_update = True
    except Exception as e:
        import traceback
        retox_log.error("!!!!!! Process crash !!!!!!!")
        retox_log.error(traceback.format_exc())
    finally:
        # TODO : Extra key for rebuilding tox virtualenvs
        retox_log.debug(u"Finished and exiting")
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
    main(sys.argv)
