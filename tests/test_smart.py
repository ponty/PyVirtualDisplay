import sys

from easyprocess import EasyProcess
from path import Path

from pyvirtualdisplay.smartdisplay import DisplayTimeoutError, SmartDisplay
import pytest


def test_disp():
    vd = SmartDisplay().start()

    # d = SmartDisplay(visible=1).start().sleep(2).stop()
    # .assertEquals(d.return_code, 0)

    d = SmartDisplay(visible=0).start().stop()
    assert d.return_code == 0

    vd.stop()


def test_slowshot():
    disp = SmartDisplay(visible=0).start()
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess("python " + py).start()
    img = disp.waitgrab()
    proc.stop()
    disp.stop()
    assert img is not None


def test_slowshot_wrap():
    disp = SmartDisplay(visible=0)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess("python " + py)
    with disp:
        with proc:
            img = disp.waitgrab()
    assert img is not None


def test_empty():
    disp = SmartDisplay(visible=0)
    proc = EasyProcess(sys.executable)
    with disp:
        with proc:
            with pytest.raises(Exception):
                img = disp.waitgrab()


def test_slowshot_timeout():
    disp = SmartDisplay(visible=0)
    py = Path(__file__).parent / ("slowgui.py")
    proc = EasyProcess("python " + py)
    with disp:
        with proc:
            with pytest.raises(DisplayTimeoutError):
                img = disp.waitgrab(timeout=1)
