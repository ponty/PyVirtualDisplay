import logging
from threading import Thread
from time import sleep

from easyprocess import EasyProcess
from PIL import ImageChops

from pyvirtualdisplay.smartdisplay import SmartDisplay


def func2(results):
    with SmartDisplay(manage_global_env=False) as disp:
        env = disp.env()
        logging.info("env=%s", env)
        sleep(2)
        with EasyProcess(["xmessage", "hello"], env=env):
            im = disp.waitgrab(timeout=1)
            results[0] = im
            sleep(2)


def test_smart():
    results = [None]
    t = Thread(target=func2, args=(results,))
    t.start()
    sleep(1)
    with SmartDisplay(manage_global_env=False) as disp:
        env = disp.env()
        logging.info("env=%s", env)
        with EasyProcess(["xmessage", "hello"], env=env):
            sleep(2)
            im0 = disp.waitgrab(timeout=1)
            assert im0
    t.join()
    im1 = results[0]
    assert im1
    # im0.save('/vagrant/im0.png')
    # im1.save('/vagrant/im1.png')
    img_diff = ImageChops.difference(im0, im1)
    ex = img_diff.getextrema()
    logging.debug("diff getextrema: %s", ex)
    diff_bbox = img_diff.getbbox()
    assert diff_bbox is None
