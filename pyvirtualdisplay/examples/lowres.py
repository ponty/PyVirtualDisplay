from easyprocess import EasyProcess
from pyvirtualdisplay import Display

if __name__ == "__main__":
    Display(visible=1, size=(320, 240)).start()
    EasyProcess('gnumeric').start()
