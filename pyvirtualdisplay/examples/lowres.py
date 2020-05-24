"Testing gnumeric on low resolution."
from easyprocess import EasyProcess

from pyvirtualdisplay import Display

# start Xephyr
Display(visible=True, size=(320, 240)).start()
# start Gnumeric
EasyProcess(["gnumeric"]).start()
