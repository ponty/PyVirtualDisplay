from easyprocess import EasyProcess

from pyvirtualdisplay import Display

if __name__ == "__main__":
    # start Xephyr
    Display(visible=True, size=(320, 240)).start()
    # start Gnumeric
    EasyProcess("gnumeric").start()
