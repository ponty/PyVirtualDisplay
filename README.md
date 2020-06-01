pyvirtualdisplay is a python wrapper for [Xvfb][1], [Xephyr][2] and [Xvnc][3]

Links:
 * home: https://github.com/ponty/pyvirtualdisplay
 * PYPI: https://pypi.python.org/pypi/pyvirtualdisplay

[![Build Status](https://travis-ci.org/ponty/pyvirtualdisplay.svg?branch=master)](https://travis-ci.org/ponty/pyvirtualdisplay)

Features:
 - python wrapper
 - supported python versions: 2.7, 3.6, 3.7, 3.8
 - back-ends:  [Xvfb][1], [Xephyr][2] and [Xvnc][3]

Possible applications:
 * headless run
 * GUI testing
 * automatic GUI screenshot

Installation
============

install the program:

```console
$ python3 -m pip install pyvirtualdisplay
```

optional: [pyscreenshot][pyscreenshot] and [Pillow][pillow] should be installed for ``smartdisplay`` submodule:

```console
$ python3 -m pip install pyscreenshot pillow
```

on Ubuntu:

```console
$ sudo apt-get install xvfb xserver-xephyr vnc4server xfonts-base
$ python3 -m pip install pyvirtualdisplay pyscreenshot pillow
```

Usage
=====

Controlling the display with `start()` and `stop()` methods:

```py
from pyvirtualdisplay import Display
disp = Display().start()
# display is active
disp.stop()
# display is stopped
```

Controlling the display with context manager:

```py
from pyvirtualdisplay import Display
with Display() as disp:
    # display is active
    pass
# display is stopped
```

Selecting Xvfb backend:

```py
disp=Display()
# or
disp=Display(visible=False)
# or
disp=Display(backend="xvfb")
```

Selecting Xephyr backend:
```py
disp=Display(visible=True)
# or
disp=Display(backend="xephyr")
```

Selecting Xvnc backend:
```py
disp=Display(backend="xvnc")
```

Setting display size:

```py
disp=Display(size=(100, 60))
```

Setting display color depth:

```py
disp=Display(color_depth=24)
```

headless run
------------

The display is hidden.
If `visible=True` then a nested Xephyr window opens and the GUI can be controlled.

```py
# pyvirtualdisplay/examples/headless.py

"Start Xvfb server. Open xmessage window."

from easyprocess import EasyProcess

from pyvirtualdisplay import Display

with Display(visible=False, size=(100, 60)) as disp:
    with EasyProcess(["xmessage", "hello"]) as proc:
        proc.wait()

```

vncserver
---------

The same as headless example, but it can be controlled with a VNC client.

```py
# pyvirtualdisplay/examples/vncserver.py

"Start virtual VNC server. Connect with: vncviewer localhost:5904"

from easyprocess import EasyProcess

from pyvirtualdisplay import Display

with Display(backend="xvnc", size=(100, 60), rfbport=5904) as disp:
    with EasyProcess(["xmessage", "hello"]) as proc:
        proc.wait()

```

Run it:
```console
$ python3 -m pyvirtualdisplay.examples.vncserver
```

<!-- embedme doc/gen/vncviewer_localhost:5904.txt -->
Check it with vncviewer:
```console
$ vncviewer localhost:5904
```

![](/doc/gen/vncviewer_localhost:5904.png)


GUI Test
--------

```py
# pyvirtualdisplay/examples/lowres.py

"Testing gnumeric on low resolution."
from easyprocess import EasyProcess

from pyvirtualdisplay import Display

# start Xephyr
with Display(visible=True, size=(320, 240)) as disp:
    # start Gnumeric
    with EasyProcess(["gnumeric"]) as proc:
        proc.wait()

```

<!-- embedme doc/gen/python3_-m_pyvirtualdisplay.examples.lowres.txt -->
Run it:
```console
$ python3 -m pyvirtualdisplay.examples.lowres
```

Image:

![](/doc/gen/python3_-m_pyvirtualdisplay.examples.lowres.png)


Screenshot
----------

```py
# pyvirtualdisplay/examples/screenshot.py

"Create screenshot of xmessage in background using 'smartdisplay' submodule"
from easyprocess import EasyProcess

from pyvirtualdisplay.smartdisplay import SmartDisplay

# 'SmartDisplay' instead of 'Display'
# It has 'waitgrab()' method.
# It has more dependencies than Display.
with SmartDisplay() as disp:
    with EasyProcess(["xmessage", "hello"]):
        # wait until something is displayed on the virtual display (polling method)
        # and then take a fullscreen screenshot
        # and then crop it. Background is black.
        img = disp.waitgrab()
img.save("xmessage.png")

```

<!-- embedme doc/gen/python3_-m_pyvirtualdisplay.examples.screenshot.txt -->
Run it:
```console
$ python3 -m pyvirtualdisplay.examples.screenshot
```

Image:

![](/doc/gen/xmessage.png)


Nested Xephyr
-------------

```py
# pyvirtualdisplay/examples/nested.py

"Nested Xephyr servers"
from easyprocess import EasyProcess

from pyvirtualdisplay import Display

with Display(visible=True, size=(220, 180), bgcolor="black"):
    with Display(visible=True, size=(200, 160), bgcolor="white"):
        with Display(visible=True, size=(180, 140), bgcolor="black"):
            with Display(visible=True, size=(160, 120), bgcolor="white"):
                with Display(visible=True, size=(140, 100), bgcolor="black"):
                    with Display(visible=True, size=(120, 80), bgcolor="white"):
                        with Display(visible=True, size=(100, 60), bgcolor="black"):
                            with EasyProcess(["xmessage", "hello"]) as proc:
                                proc.wait()

```

<!-- embedme doc/gen/python3_-m_pyvirtualdisplay.examples.nested.txt -->
Run it:
```console
$ python3 -m pyvirtualdisplay.examples.nested
```

Image:

![](/doc/gen/python3_-m_pyvirtualdisplay.examples.nested.png)

xauth
=====

Some programs require a functional Xauthority file. PyVirtualDisplay can
generate one and set the appropriate environment variables if you pass
``use_xauth=True`` to the ``Display`` constructor. Note however that this
feature needs ``xauth`` installed, otherwise a
``pyvirtualdisplay.xauth.NotFoundError`` is raised.

Concurrency
===========

_"Recent X servers as of version 1.13 (Xvfb, too) support the -displayfd command line option: It will make the X server choose the display itself"_
https://stackoverflow.com/questions/2520704/find-a-free-x11-display-number/

First help text is checked (e.g. `Xvfb -help`) to find if `-displayfd` flag is available.
If `-displayfd` flag is available then it is used, if not then there are 10 retries by default which should be enough for starting 10 concurrent X servers.
The `retries` parameter can be increased if necessary.

Hierarchy
=========

![Alt text](https://g.gravizo.com/source/svg?https%3A%2F%2Fraw.githubusercontent.com/ponty/pyvirtualdisplay/master/doc/hierarchy.dot)

[1]: http://en.wikipedia.org/wiki/Xvfb
[2]: http://en.wikipedia.org/wiki/Xephyr
[3]: https://tigervnc.org/
[pillow]: https://pillow.readthedocs.io
[pyscreenshot]: https://github.com/ponty/pyscreenshot

