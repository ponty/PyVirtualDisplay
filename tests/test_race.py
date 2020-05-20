from easyprocess import EasyProcess
from pyvirtualdisplay import Display
import sys
from entrypoint2 import entrypoint
from time import sleep

# ubuntu 14.04 no displayfd
# ubuntu 16.04 displayfd
# ubuntu 18.04 displayfd


def has_displayfd():
    p = EasyProcess(["Xvfb", "-help"])
    p.enable_stdout_log = False
    p.enable_stderr_log = False
    p.call()
    helptext = p.stderr
    return "-displayfd" in helptext


if has_displayfd():

    def test_race_10_100():
        check_N(10)
        check_N(100)


def check_N(N):
    ls = []
    try:
        for i in range(N):
            cmd = [
                sys.executable,
                __file__.rsplit(".", 1)[0] + ".py",
                str(i),
                "--debug",
            ]
            p = EasyProcess(cmd)
            p.start()
            ls += [p]

        sleep(3)

        good_count = 0
        for p in ls:
            p.wait()
            if p.return_code == 0:
                good_count += 1
    finally:
        for p in ls:
            p.stop()
    print(good_count)
    assert good_count == N


@entrypoint
def main(i):
    d = Display().start()
    print("my index:%s  disp:%s" % (i, d.new_display_var))
    ok = d.is_alive()
    d.stop()
    assert ok
