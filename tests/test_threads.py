from threading import Lock, Thread
from time import sleep

from easyprocess import EasyProcess

from pyvirtualdisplay import Display

disps = []
mutex = Lock()


def get_display(threadid, disp):
    dispnr = EasyProcess(["sh", "-c", "echo $DISPLAY"], env=disp.env()).call().stdout
    with mutex:
        disps.append((threadid, dispnr))


def func():
    with Display(manage_global_env=False) as disp:
        get_display(1, disp)
        sleep(2)
        get_display(1, disp)


def test_disp_var():
    t = Thread(target=func)
    t.start()
    sleep(1)

    with Display(manage_global_env=False) as disp:
        get_display(0, disp)
        sleep(2)
        get_display(0, disp)
    t.join()

    print(disps)

    assert disps[0][0] == 1
    assert disps[1][0] == 0
    assert disps[2][0] == 1
    assert disps[3][0] == 0

    # :1
    assert disps[0][1] == disps[2][1]

    # :0
    assert disps[1][1] == disps[3][1]

    assert disps[0][1] != disps[1][1]
