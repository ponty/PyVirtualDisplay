import time

from easyprocess import EasyProcess


def main():
    time.sleep(10)
    EasyProcess(["xmessage", "hello"]).start()


if __name__ == "__main__":
    main()
