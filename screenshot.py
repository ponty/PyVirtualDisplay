from easyprocess import EasyProcess
import os
from pyvirtualdisplay.smartdisplay import SmartDisplay
import cog

import logging
logging.basicConfig(level=logging.DEBUG)

def screenshot(cmd, fname):
    if os.path.exists(fname):
        os.remove(fname)
    with SmartDisplay(visible=0, bgcolor='black') as disp:
        with EasyProcess(cmd):
            img = disp.waitgrab()
            img.save(fname)
            cog.outl( '.. image:: %s' % fname )