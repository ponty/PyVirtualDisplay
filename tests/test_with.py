from pyvirtualdisplay.display import Display


def test_with():
    with Display(visible=False, size=(800, 600)) as vd:
        assert vd.is_alive()
    assert vd.return_code == 0
    assert not vd.is_alive()


def test_dpi():
    with Display(backend="xvfb", size=(800, 600), dpi=99) as vd:
        assert vd.is_alive()
    assert vd.return_code == 0
    assert not vd.is_alive()
