'''
Example for Xvnc backend
'''

from easyprocess import EasyProcess
from pyvirtualdisplay.display import Display

if __name__ == "__main__":
    with Display(backend='xvnc', rfbport=5904) as disp:
        with EasyProcess('xmessage hello') as proc:
            proc.wait()
