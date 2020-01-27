import time

from easyprocess import EasyProcess


def main():
    time.sleep(5)
    EasyProcess('zenity --question').start()

if __name__ == "__main__":
    main()
