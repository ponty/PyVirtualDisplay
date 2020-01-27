import logging
import time

from easyprocess import EasyProcess

from pyvirtualdisplay.display import Display

log = logging.getLogger(__name__)


VISIBLE = 0


def test_screenshot3():
    with Display(visible=VISIBLE):
        with EasyProcess('python -m pyvirtualdisplay.examples.screenshot3'):
            time.sleep(1)
