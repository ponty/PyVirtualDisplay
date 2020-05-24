import sys

from easyprocess import EasyProcess

from pyvirtualdisplay.util import get_helptext


def prog_check(cmd):
    try:
        return EasyProcess(cmd).call().return_code == 0
    except Exception:
        return False


def platform_is_osx():
    return sys.platform == "darwin"


def has_displayfd():
    return "-displayfd" in get_helptext("Xvfb")


def has_xvnc():
    return prog_check(["Xvnc", "-help"])
