from easyprocess import EasyProcess
import sys
from pyvirtualdisplay.util import get_helptext


def prog_check(cmd):
    try:
        if EasyProcess(cmd).call().return_code == 0:
            return True
    except Exception:
        return False


def platform_is_osx():
    return sys.platform == "darwin"


def has_displayfd():
    return "-displayfd" in get_helptext("Xvfb")
