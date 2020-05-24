"Nested Xephyr servers"
from easyprocess import EasyProcess

from pyvirtualdisplay import Display

Display(visible=True, size=(220, 180), bgcolor="black").start()
Display(visible=True, size=(200, 160), bgcolor="white").start()
Display(visible=True, size=(180, 140), bgcolor="black").start()
Display(visible=True, size=(160, 120), bgcolor="white").start()
Display(visible=True, size=(140, 100), bgcolor="black").start()
Display(visible=True, size=(120, 80), bgcolor="white").start()
Display(visible=True, size=(100, 60), bgcolor="black").start()
EasyProcess(["xmessage", "hello"]).start()
