import sys
from time import sleep

from easyprocess import EasyProcess
from entrypoint2 import entrypoint

from pyvirtualdisplay import Display
from tutil import worker

# ubuntu 14.04 no displayfd
# ubuntu 16.04 displayfd
# ubuntu 18.04 displayfd


# TODO: osx error:            Cannot open "/tmp/server-0.xkm" to write keyboard description
if 0:  # TODO: and not platform_is_osx():

    def test_race_10_xvfb():
        check_N(10, "xvfb")

    def test_race_10_xephyr():
        check_N(10, "xephyr")

    def test_race_10_xvnc():
        if worker() == 0:
            check_N(10, "xvnc")


def check_N(N, backend):
    with Display():
        ls = []
        try:
            for i in range(N):
                cmd = [
                    sys.executable,
                    __file__.rsplit(".", 1)[0] + ".py",
                    str(i),
                    backend,
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
        assert good_count == N


@entrypoint
def main(i, backend):
    kwargs = dict()
    if backend == "xvnc":
        kwargs["rfbport"] = 42000 + int(i)

    d = Display(backend=backend, **kwargs).start()
    print("my index:%s  backend:%s disp:%s" % (i, backend, d.new_display_var))
    ok = d.is_alive()
    d.stop()
    assert ok
