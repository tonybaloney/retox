ReTox
=====

A command line service that runs your tox tests in parallel, using threading and multicore CPUs.

See your tox environments in a dashboard and automatically watch source folders for file changes and re-run tests.

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

Credits
-------

This was inspired by the detox project, which was created by the tox development team. I worked and then significantly changed the way it works
to support re-running environments with ease
