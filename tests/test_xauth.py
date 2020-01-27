import os

from nose import SkipTest
from nose.tools import eq_, ok_

from pyvirtualdisplay import xauth
from pyvirtualdisplay.display import Display


def test_xauth():
    '''
    Test that a Xauthority file is created.
    '''
    if not xauth.is_installed():
        raise SkipTest('This test needs xauth installed')
    old_xauth = os.getenv('XAUTHORITY')
    display = Display(visible=0, use_xauth=True)
    display.start()
    new_xauth = os.getenv('XAUTHORITY')

    ok_(new_xauth is not None)
    ok_(os.path.isfile(new_xauth))
    filename = os.path.basename(new_xauth)
    ok_(filename.startswith('PyVirtualDisplay.'))
    ok_(filename.endswith('Xauthority'))

    display.stop()
    eq_(old_xauth, os.getenv('XAUTHORITY'))
    ok_(not os.path.isfile(new_xauth))
