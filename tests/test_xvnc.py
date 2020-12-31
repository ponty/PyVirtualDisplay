import tempfile
from pathlib import Path

from vncdotool import api

from pyvirtualdisplay import Display
from pyvirtualdisplay.xvnc import XvncDisplay
from tutil import has_xvnc, rfbport, worker

if has_xvnc():

    def test_xvnc():
        with tempfile.TemporaryDirectory() as temp_dir:
            vnc_png = Path(temp_dir) / "vnc.png"
            password = "123456"
            passwd_file = Path(temp_dir) / "pwd.txt"
            vncpasswd_generated = b"\x49\x40\x15\xf9\xa3\x5e\x8b\x22"
            passwd_file.write_bytes(vncpasswd_generated)

            if worker() == 0:
                with Display(backend="xvnc"):
                    with api.connect("localhost:0") as client:
                        client.timeout = 1
                        client.captureScreen(vnc_png)
                with XvncDisplay():
                    with api.connect("localhost:0") as client:
                        client.timeout = 1
                        client.captureScreen(vnc_png)

            sconnect = "localhost:%s" % (rfbport() - 5900)
            with Display(backend="xvnc", rfbport=rfbport()):
                with api.connect(sconnect) as client:
                    client.timeout = 1
                    client.captureScreen(vnc_png)
            with XvncDisplay(rfbport=rfbport()):
                with api.connect(sconnect) as client:
                    client.timeout = 1
                    client.captureScreen(vnc_png)

            with Display(backend="xvnc", rfbport=rfbport(), rfbauth=passwd_file):
                with api.connect(sconnect, password=password) as client:
                    client.timeout = 1
                    client.captureScreen(vnc_png)
            with XvncDisplay(rfbport=rfbport(), rfbauth=passwd_file):
                with api.connect(sconnect, password=password) as client:
                    client.timeout = 1
                    client.captureScreen(vnc_png)
