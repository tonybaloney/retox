# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
import re
import sys

from tox.session import prepare
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from retox.service import RetoxService
from retox.ui import create_layout
from retox.log import retox_log
from retox.path import Path


MAX_RUNS = -1


def main(args=sys.argv):
    out = -1
    retox_log.debug("Starting command")
    retox_log.info("System stdout encoding is %s" % sys.stdout.encoding)

    # Use the Tox argparse logic
    tox_args = prepare(args)
    tox_args.option.resultjson = '.retox.json'

    # Custom arguments for watching directories
    if tox_args.option.watch is None:
        tox_args.option.watch = []
    elif not isinstance(tox_args.option.watch, list):
        tox_args.option.watch = [tox_args.option.watch]

    # Start a service and a green pool
    screen = Screen.open(unicode_aware=True)
    try:

        needs_update = True
        running = True

        env_frames, main_scene, log_scene, host_frame = create_layout(tox_args, screen)

        service = RetoxService(tox_args, screen, env_frames)
        service.start()

        exclude = tox_args.option.exclude

        # Create a local dictionary of the files to see for differences
        run_count = 0
        _watches = [get_hashes(w, exclude) for w in tox_args.option.watch]

        screen.set_scenes([main_scene], start_scene=main_scene)

        while running:
            if needs_update:
                host_frame.status = 'Running'
                run_count = run_count + 1
                out = service.run(tox_args.envlist)
                host_frame.last_result = out
                needs_update = False
            else:
                time.sleep(.5)
            if MAX_RUNS != -1 and run_count >= MAX_RUNS:
                running = False
            if tox_args.option.watch:
                # Refresh the watch folders and check for changes
                _new_watches = [get_hashes(w, exclude) for w in tox_args.option.watch]
                changes = zip(_watches, _new_watches)
                needs_update = any(x != y for x, y in changes)
                _watches = _new_watches

            if MAX_RUNS == -1:
                host_frame.status = 'Waiting'

                event = screen.get_event()
                if isinstance(event, KeyboardEvent):
                    if event.key_code == ord('q'):
                        running = False
                    elif event.key_code == ord('b'):
                        needs_update = True
                    elif event.key_code == ord('r'):
                        needs_update = True
                    # elif event.key_code == ord('l'):
                    #     show_logs(screen, log_scene)
    except Exception:
        import traceback
        retox_log.error("!!!!!! Process crash !!!!!!!")
        retox_log.error(traceback.format_exc())
    except SystemExit as exit_message:
        out = exit_message.code
    finally:
        # TODO : Extra key for rebuilding tox virtualenvs
        retox_log.debug(u"Finished and exiting")
        screen.clear()
        screen.close(restore=True)
    return out


def show_logs(screen, log_scene):
    screen.set_scenes([log_scene], start_scene=log_scene)
    running = True
    while running:
        event = screen.get_event()
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('q'):
                running = False


def get_hashes(path, exclude=None):
    '''
    Get a dictionary of file paths and timestamps.

    Paths matching `exclude` regex will be excluded.
    '''
    out = {}
    for f in Path(path).rglob('*'):
        if f.is_dir():
            # We want to watch files, not directories.
            continue
        if exclude and re.match(exclude, f.as_posix()):
            retox_log.debug("excluding '{}'".format(f.as_posix()))
            continue
        pytime = f.stat().st_mtime
        out[f.as_posix()] = pytime
    return out


if __name__ == '__main__':
    main(sys.argv)
