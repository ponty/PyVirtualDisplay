from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

disp = SmartDisplay(visible=0, bgcolor='black')
func = disp.wrap(EasyProcess('xmessage screenshot').wrap(disp.waitgrab))
img=func()
img.show()
