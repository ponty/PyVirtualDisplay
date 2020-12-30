import logging
import os
import sys
from tempfile import TemporaryDirectory
from time import sleep

from easyprocess import EasyProcess

from pyvirtualdisplay import Display
from tutil import has_xvnc, kill_process_tree, prog_check, worker

log = logging.getLogger(__name__)


python = sys.executable


def test_screenshot():
    owd = os.getcwd()
    with TemporaryDirectory(prefix="pyvirtualdisplay_") as tmpdirname:
        try:
            os.chdir(tmpdirname)
            p = EasyProcess([python, "-m", "pyvirtualdisplay.examples.screenshot"])
            p.call()
            assert p.return_code == 0
        finally:
            os.chdir(owd)


def test_headless():
    p = EasyProcess([python, "-m", "pyvirtualdisplay.examples.headless"]).start()
    sleep(1)
    assert p.is_alive()
    # p.stop()
    kill_process_tree(p)


def test_nested():
    with Display():
        p = EasyProcess([python, "-m", "pyvirtualdisplay.examples.nested"]).start()
        sleep(1)
        assert p.is_alive()
        # p.stop()
        kill_process_tree(p)


if has_xvnc():

    def test_vncserver():
        if worker() == 0:
            p = EasyProcess(
                [python, "-m", "pyvirtualdisplay.examples.vncserver"]
            ).start()
            sleep(1)
            assert p.is_alive()
            # p.stop()
            kill_process_tree(p)


if prog_check(["gnumeric", "-help"]):

    def test_lowres():
        with Display():
            p = EasyProcess([python, "-m", "pyvirtualdisplay.examples.lowres"]).start()
            sleep(1)
            assert p.is_alive()
            # p.stop()
            kill_process_tree(p)
