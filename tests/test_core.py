from pyvirtualdisplay.display import Display
from pyvirtualdisplay.randomize import Randomizer
from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay
from pyvirtualdisplay.xvnc import XvncDisplay


def test_virt():
    vd = Display().start().stop()
    assert vd.return_code == 0
    assert not vd.is_alive()


def test_random():
    r = Randomizer()
    vd = Display(randomizer=r).start().stop()
    assert vd.return_code == 0
    assert r.min <= vd.display <= r.min + r.delta
    assert not vd.is_alive()


def test_nest():
    vd = Display().start()
    assert vd.is_alive()

    nd = Display(visible=1).start().stop()

    assert nd.return_code == 0

    vd.stop()
    assert not vd.is_alive()


def test_disp():
    vd = Display().start()
    assert vd.is_alive()

    # d = Display(visible=1).start().sleep(2).stop()
    # .assertEquals(d.return_code, 0)

    d = Display(visible=0).start().stop()
    assert d.return_code == 0

    vd.stop()
    assert not vd.is_alive()


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
