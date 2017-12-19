Retox
=====

A command line service that runs your tox tests in parallel, using threading and multicore CPUs.

See your tox environments in a dashboard and automatically watch source folders for file changes and re-run tests.

See : https://github.com/tonybaloney/retox/raw/master/docs/_static/screenshot.jpeg for an example screenshot

Requirements
------------

Linux users may need to install libncurses5-dev before using Tox. If you see an error "ImportError: No module named '_curses'" this is because of the Requirement.

Usage
-----

To install, run 

.. code-block:: bash

    pip install retox

Then from any project that has a `tox.ini` file setup and using tox, you can simply run

.. code-block:: bash

    retox 

This will start the service, from where you can press (b) to rebuild on demand.

Watching folders
----------------

Retox can watch one or many directories for file changes and re-run the tox environments when changes are detected

.. code-block:: bash

    retox -w my_project_folder -w my_test_folder

Tox support
-----------

Any tox arguments can be given to the command, and using --help to get a full list of commands. Tox arguments will be passed to all virtualenvs

.. code-block:: bash

    retox -e py27,py36

Logging
-------

2 files will be created - .retox.log, which is a file for all runs of the logs for the virtual environments. This can be handy to tail to see live output
.retox.json - a JSON file with the virtualenv tasks and specific command output.

Credits
-------

This was inspired by the detox project, which was created by the tox development team. I worked and then significantly changed the way it works
to support re-running environments with ease.
