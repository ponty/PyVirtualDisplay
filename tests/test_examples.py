import logging
import sys
import time

from easyprocess import EasyProcess

from pyvirtualdisplay import Display

log = logging.getLogger(__name__)


VISIBLE = 0

python = sys.executable


def test_screenshot3():
    with Display(visible=VISIBLE):
        with EasyProcess([python, "-m", "pyvirtualdisplay.examples.screenshot3"]):
            time.sleep(1)
