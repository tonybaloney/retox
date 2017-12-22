Release History
===============

1.4.0 (2017-12-23)
------------------

* Directory watching only includes .py files now, so log files are ignored
* Fix bug where multiple watch folders would not be watched (@bstpierre)

1.3.1 (2017-12-19)
------------------

* Fix small issue in readme not rendering on Pypi

1.3.0 (2017-12-19)
------------------

* Added a dashboard at the top
* Individual task/action feedback for each virtualenv
* Capture crashes within the threadpool into log files
* Added tests and test structure, more ongoing
* Fixed unicode related issue when running in Python 3.x https://github.com/tonybaloney/retox/issues/1

1.2.1 (2017-12-17)
------------------

* Fixed issue where retox command was not starting, with error "TypeError: main() takes exactly 1 argument (0 given)"
  See https://github.com/tonybaloney/retox/issues/3

1.2.0 (2017-12-15)
------------------

* Support all tox command line parameters, like -e for environment selection
* Fixed issue where exceptions raised by subprocesses could crash host screen
* Removed dependency on click

1.1.1 (2017-12-14)
------------------

* Fix crash where venv.status would not resolve on a NoneType resource venv

1.1.0 (2017-12-14)
------------------

* Fix issue where after a failed test, the build would fail after install deps

1.0.0 (2017-12-14)
------------------

* Initial release