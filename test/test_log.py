# -*- coding: utf-8 -*-

from mock import patch

from six.moves import cStringIO as StringIO
import retox.log


@patch('sys.stdout', new_callable=StringIO)
def test_stdout_redirect(mocked_stdout):
    retox.log.retox_log.warning("Test Warning")
    assert 'test' not in mocked_stdout.getvalue()
