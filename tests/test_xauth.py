import os

from pyvirtualdisplay import Display, xauth


def test_xauth():
    """
    Test that a Xauthority file is created.
    """
    if not xauth.is_installed():
        print("This test needs xauth installed")
        return
    old_xauth = os.getenv("XAUTHORITY")
    display = Display(visible=False, use_xauth=True)
    display.start()
    new_xauth = os.getenv("XAUTHORITY")

    assert new_xauth is not None
    assert os.path.isfile(new_xauth)
    filename = os.path.basename(new_xauth)
    assert filename.startswith("PyVirtualDisplay.")
    assert filename.endswith("Xauthority")

    display.stop()
    assert old_xauth == os.getenv("XAUTHORITY")
    assert not os.path.isfile(new_xauth)
