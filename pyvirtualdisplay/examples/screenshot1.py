from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

disp = SmartDisplay(visible=0, bgcolor='black').start()
xmessage = EasyProcess('xmessage screenshot').start()
img = disp.waitgrab()
xmessage.stop()
disp.stop()
img.show()

