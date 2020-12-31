import sys
from pathlib import Path

import pytest
from easyprocess import EasyProcess

from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import DisplayTimeoutError, SmartDisplay

python = sys.executable


def test_disp():
    with Display():

        d = SmartDisplay(visible=True).start().stop()
        assert d.return_code == 0

        d = SmartDisplay(visible=False).start().stop()
        assert d.return_code == 0


def test_slowshot():
    disp = SmartDisplay(visible=False).start()
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess([python, py]).start()
    img = disp.waitgrab()
    proc.stop()
    disp.stop()
    assert img is not None


def test_slowshot_with():
    disp = SmartDisplay(visible=False)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess([python, py])
    with disp:
        with proc:
            img = disp.waitgrab()
    assert img is not None


def test_slowshot_nocrop():
    disp = SmartDisplay(visible=False)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess([python, py])
    with disp:
        with proc:
            img = disp.waitgrab(autocrop=False)
    assert img is not None


def test_empty():
    disp = SmartDisplay(visible=False)
    proc = EasyProcess([python])
    with disp:
        with proc:
            with pytest.raises(Exception):
                disp.waitgrab(timeout=10)


def test_empty_nocrop():
    disp = SmartDisplay(visible=False)
    proc = EasyProcess([python])
    with disp:
        with proc:
            with pytest.raises(Exception):
                disp.waitgrab(autocrop=False, timeout=10)


def test_slowshot_timeout():
    disp = SmartDisplay(visible=False)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess([python, py])
    with disp:
        with proc:
            with pytest.raises(DisplayTimeoutError):
                img = disp.waitgrab(timeout=1)


def test_slowshot_timeout_nocrop():
    disp = SmartDisplay(visible=False)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess([python, py])
    with disp:
        with proc:
            with pytest.raises(DisplayTimeoutError):
                img = disp.waitgrab(timeout=1, autocrop=False)
