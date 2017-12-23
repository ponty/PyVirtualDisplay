from easyprocess import EasyProcess
from pyvirtualdisplay import Display

if __name__ == "__main__":
    # start Xephyr
    Display(visible=1, size=(320, 240)).start()
    # start Gnumeric
    EasyProcess('gnumeric').start()
