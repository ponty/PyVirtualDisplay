"Create screenshot of xmessage in background"
from easyprocess import EasyProcess

from pyvirtualdisplay.smartdisplay import SmartDisplay

with SmartDisplay() as disp:
    with EasyProcess(["xmessage", "hello"]):
        img = disp.waitgrab()
img.save("xmessage.png")
