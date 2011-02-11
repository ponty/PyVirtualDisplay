from easyprocess import EasyProcess
from pyscreenshot import grab
from pyvirtualdisplay import Display

vd = Display(visible=0).start()
xmessage = EasyProcess('xmessage screenshot').start().sleep(1)
img = grab()
xmessage.stop()
vd.stop()
img = img.crop(img.getbbox())
img.show()

