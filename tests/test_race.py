from easyprocess import EasyProcess
from pyvirtualdisplay import Display
import sys
from entrypoint2 import entrypoint
from time import sleep


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

        alive_count = 0
        alive_ls = []
        for p in ls:
            if p.is_alive():
                alive_count += 1
                alive_ls += [1]
            else:
                alive_ls += [0]
    finally:
        for p in ls:
            p.stop()
    # ret_count = 0
    # for p in ls:
    #     if p.return_code == 0:
    #         ret_count += 1
    print(alive_count)
    print(alive_ls)
    # print(ret_count)
    assert alive_count == N
    # assert ret_count == N


@entrypoint
def main(i):
    # print("my index:%s" % (i))
    d = Display().start()
    print("my index:%s  disp:%s" % (i, d.new_display_var))
    assert d.is_alive()
    sleep(600)
