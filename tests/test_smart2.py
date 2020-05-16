from easyprocess import EasyProcess

from pyvirtualdisplay.smartdisplay import SmartDisplay


def test_double():
    with SmartDisplay(visible=False, bgcolor="black") as disp:
        with EasyProcess(["xmessage", "hello1"]):
            img = disp.waitgrab()
            assert img is not None

    with SmartDisplay(visible=False, bgcolor="black") as disp:
        with EasyProcess(["xmessage", "hello2"]):
            img = disp.waitgrab()
            assert img is not None
