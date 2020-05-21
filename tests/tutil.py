from easyprocess import EasyProcess
import sys

def prog_check(cmd):
    try:
        if EasyProcess(cmd).call().return_code == 0:
            return True
    except Exception:
        return False


def platform_is_osx():
    return sys.platform == "darwin"
