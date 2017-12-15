Release History
===============

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