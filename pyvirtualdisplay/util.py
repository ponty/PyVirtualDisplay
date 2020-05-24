import sys

from easyprocess import EasyProcess


def get_helptext(program):
    p = EasyProcess([program, "-help"])
    p.enable_stdout_log = False
    p.enable_stderr_log = False
    p.call()
    helptext = p.stderr
    return helptext


def py2():
    return sys.version_info[0] == 2
