from easyprocess import EasyProcess
from pyscreenshot import grab
from pyvirtualdisplay import Display
 
img = Display(visible=0).wrap(
                EasyProcess('xmessage screenshot2').wrap(
                                    grab, delay=1))()
img = img.crop(img.getbbox())
img.show()

