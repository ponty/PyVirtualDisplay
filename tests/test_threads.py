import logging
from threading import Lock, Thread
from time import sleep

from easyprocess import EasyProcess
from PIL import ImageChops

from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
from tutil import platform_is_osx

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

    if not platform_is_osx():
        assert disps[0][1] != disps[1][1]


def func2(results):
    with SmartDisplay(manage_global_env=False) as disp:
        with EasyProcess(["xmessage", "hello2"], env=disp.env()):
            sleep(2)
            im = disp.waitgrab(timeout=1)
            results[0] = im


def test_smart():
    results = [None]
    t = Thread(target=func2, args=(results,))
    t.start()
    sleep(1)
    with SmartDisplay(manage_global_env=False) as disp:
        with EasyProcess(["xmessage", "hello"], env=disp.env()):
            sleep(2)
            im0 = disp.waitgrab(timeout=1)
            assert im0
    t.join()
    im1 = results[0]
    assert im1
    img_diff = ImageChops.difference(im0, im1)
    ex = img_diff.getextrema()
    logging.debug("diff getextrema: %s", ex)
    diff_bbox = img_diff.getbbox()
    assert diff_bbox is None
