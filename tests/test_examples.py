from easyprocess import EasyProcess
from pyvirtualdisplay.display import Display
import logging
import time


log = logging.getLogger(__name__)


VISIBLE = 0


def test_screenshot3():
    with Display(visible=VISIBLE):
        with EasyProcess('python -m pyvirtualdisplay.examples.screenshot3'):
            time.sleep(1)
