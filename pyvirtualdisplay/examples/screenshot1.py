from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

if __name__ == "__main__":
    disp = SmartDisplay(visible=0, bgcolor='black').start()
    xmessage = EasyProcess('xmessage hello').start()
    img = disp.waitgrab()
    xmessage.stop()
    disp.stop()
    img.show()
