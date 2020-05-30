from pyvirtualdisplay import Display
from tutil import has_xvnc


def test_with_xvfb():
    with Display(size=(800, 600)) as vd:
        assert vd.is_alive()
        assert vd._backend == "xvfb"
    assert vd.return_code == 0
    assert not vd.is_alive()

    with Display(visible=False, size=(800, 600)) as vd:
        assert vd.is_alive()
        assert vd._backend == "xvfb"
    assert vd.return_code == 0
    assert not vd.is_alive()

    with Display(backend="xvfb", size=(800, 600)) as vd:
        assert vd.is_alive()
        assert vd._backend == "xvfb"
    assert vd.return_code == 0
    assert not vd.is_alive()


def test_with_xephyr():
    with Display() as vd:
        with Display(visible=True, size=(800, 600)) as vd:
            assert vd.is_alive()
            assert vd._backend == "xephyr"
        assert vd.return_code == 0
        assert not vd.is_alive()

        with Display(backend="xephyr", size=(800, 600)) as vd:
            assert vd.is_alive()
            assert vd._backend == "xephyr"
        assert vd.return_code == 0
        assert not vd.is_alive()


if has_xvnc():

    def test_with_xvnc():
        with Display(backend="xvnc", size=(800, 600)) as vd:
            assert vd.is_alive()
            assert vd._backend == "xvnc"
        assert vd.return_code == 0
        assert not vd.is_alive()


def test_dpi():
    with Display(backend="xvfb", size=(800, 600), dpi=99) as vd:
        assert vd.is_alive()
    assert vd.return_code == 0
    assert not vd.is_alive()
