import sys
from unittest import TestCase

from easyprocess import EasyProcess
from path import Path

from pyvirtualdisplay.smartdisplay import DisplayTimeoutError, SmartDisplay


class Test(TestCase):
    def test_disp(self):
        vd = SmartDisplay().start()

        # d = SmartDisplay(visible=1).start().sleep(2).stop()
        # self.assertEquals(d.return_code, 0)

        d = SmartDisplay(visible=0).start().stop()
        self.assertEquals(d.return_code, 0)

        vd.stop()

    def test_slowshot(self):
        disp = SmartDisplay(visible=0).start()
        py = Path(__file__).parent / ("slowgui.py")
        proc = EasyProcess("python " + py).start()
        img = disp.waitgrab()
        proc.stop()
        disp.stop()
        assert img is not None

    def test_slowshot_wrap(self):
        disp = SmartDisplay(visible=0)
        py = Path(__file__).parent / ("slowgui.py")
        proc = EasyProcess("python " + py)
        with disp:
            with proc:
                img = disp.waitgrab()
        assert img is not None

    def test_empty(self):
        disp = SmartDisplay(visible=0)
        proc = EasyProcess(sys.executable)
        with disp:
            with proc:
                with self.assertRaises(Exception):
                    img = disp.waitgrab()

    def test_slowshot_timeout(self):
        disp = SmartDisplay(visible=0)
        py = Path(__file__).parent / ("slowgui.py")
        proc = EasyProcess("python " + py)
        with disp:
            with proc:
                with self.assertRaises(DisplayTimeoutError):
                    img = disp.waitgrab(timeout=1)
