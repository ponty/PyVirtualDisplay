from easyprocess import EasyProcess, EasyProcessError


def get_helptext(program):
    p = EasyProcess([program, "-help"])
    p.enable_stdout_log = False
    p.enable_stderr_log = False
    p.call()
    helptext = p.stderr
    return helptext
