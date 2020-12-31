import logging
import os

import psutil
from easyprocess import EasyProcess

from pyvirtualdisplay.util import get_helptext

log = logging.getLogger(__name__)


def prog_check(cmd):
    try:
        p = EasyProcess(cmd)
        p.enable_stdout_log = False
        p.enable_stderr_log = False
        p.call()
        return p.return_code == 0
    except Exception:
        return False


# def platform_is_osx():
#     return sys.platform == "darwin"


def has_displayfd():
    return "-displayfd" in get_helptext("Xvfb")


def has_xvnc():
    return prog_check(["Xvnc", "-help"])


def worker():
    w = 0
    PYTEST_XDIST_WORKER = os.environ.get("PYTEST_XDIST_WORKER")
    if PYTEST_XDIST_WORKER:
        # gw42
        w = int(PYTEST_XDIST_WORKER[2:])
    return w


def rfbport():
    port = 5900 + worker() + 9876
    log.info("rfbport=%s", port)
    return port


def kill_process_tree(ep):
    parent_pid = ep.pid
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        try:
            child.kill()
        except psutil.NoSuchProcess:
            log.warning("NoSuchProcess error in kill_process_tree")
    parent.kill()
