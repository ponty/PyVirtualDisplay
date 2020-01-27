from unittest import TestCase

from nose.tools import ok_

from pyvirtualdisplay.display import Display
from pyvirtualdisplay.randomize import Randomizer
from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay
from pyvirtualdisplay.xvnc import XvncDisplay


class Test(TestCase):
    def test_virt(self):
        vd = Display().start().stop()
        self.assertEquals(vd.return_code, 0)
        ok_(not vd.is_alive())

    def test_random(self):
        r = Randomizer()
        vd = Display(randomizer=r).start().stop()
        self.assertEquals(vd.return_code, 0)
        assert(r.min <= vd.display <= r.min + r.delta)
        ok_(not vd.is_alive())

    def test_nest(self):
        vd = Display().start()
        ok_(vd.is_alive())

        nd = Display(visible=1).start().stop()

        self.assertEquals(nd.return_code, 0)

        vd.stop()
        ok_(not vd.is_alive())

    def test_disp(self):
        vd = Display().start()
        ok_(vd.is_alive())

        d = Display(visible=1).start().sleep(2).stop()
        self.assertEquals(d.return_code, 0)

        d = Display(visible=0).start().stop()
        self.assertEquals(d.return_code, 0)

        vd.stop()
        ok_(not vd.is_alive())


def test_repr():
    display = Display()
    print(repr(display))


def test_repr2():
    display = XvfbDisplay()
    print(repr(display))


def test_repr3():
    display = XvncDisplay()
    print(repr(display))


def test_repr4():
    display = XephyrDisplay()
    print(repr(display))
