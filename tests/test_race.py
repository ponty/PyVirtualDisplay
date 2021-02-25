import sys
from time import sleep

from easyprocess import EasyProcess
from entrypoint2 import entrypoint

from pyvirtualdisplay import Display
from tutil import has_xvnc, worker

# ubuntu 14.04 no displayfd
# ubuntu 16.04 displayfd

# Xephyr leaks shared memory segments until 18.04
# 		https://gitlab.freedesktop.org/xorg/xserver/-/issues/130
#       approximately 4MB/call


def test_race_100_xvfb():
    check_n(100, "xvfb")


# TODO: this fails with "Xephyr cannot open host display"
#   Xephyr bug?
# def test_race_500_100_xephyr():
#     for _ in range(500):
#         check_n(100, "xephyr")



if has_xvnc():

    def test_race_10_xvnc():
        check_n(10, "xvnc")


def check_n(n, backend):
    with Display():
        ls = []
        try:
            for i in range(n):
                cmd = [
                    sys.executable,
                    __file__.rsplit(".", 1)[0] + ".py",
                    str(i),
                    backend,
                    str(n),
                    "--debug",
                ]
                p = EasyProcess(cmd)
                p.start()
                ls += [p]

            sleep(3)

            good_count = 0
            rc_ls = []
            for p in ls:
                p.wait()
                if p.return_code == 0:
                    good_count += 1
                rc_ls += [p.return_code]
        finally:
            for p in ls:
                p.stop()
        print(rc_ls)
        print(good_count)
        assert good_count == n


@entrypoint
def main(i, backend, retries):
    retries = int(retries)
    kwargs = dict()
    if backend == "xvnc":
        kwargs["rfbport"] = 42000 + 100 * worker() + int(i)
    # print("$DISPLAY=%s" % (os.environ.get("DISPLAY")))
    d = Display(backend=backend, retries=retries, **kwargs).start()
    print(
        "my index:%s  backend:%s disp:%s retries:%s"
        % (i, backend, d.new_display_var, d._obj._retries_current,)
    )
    ok = d.is_alive()
    d.stop()
    assert ok
