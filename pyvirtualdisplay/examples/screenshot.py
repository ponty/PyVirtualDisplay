"Create screenshot of xmessage in background"
from easyprocess import EasyProcess

from pyvirtualdisplay.smartdisplay import SmartDisplay

with SmartDisplay() as disp:
    with EasyProcess(["xmessage", "hello"]):
        # wait until something is displayed on the virtual display (polling method)
        # and then take a screenshot
        img = disp.waitgrab()
img.save("xmessage.png")
