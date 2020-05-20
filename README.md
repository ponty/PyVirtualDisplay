pyvirtualdisplay is a python wrapper for [Xvfb][1], [Xephyr][2] and [Xvnc][3]

Links:
 * home: https://github.com/ponty/pyvirtualdisplay
 * PYPI: https://pypi.python.org/pypi/pyvirtualdisplay

[![Build Status](https://travis-ci.org/ponty/pyvirtualdisplay.svg?branch=master)](https://travis-ci.org/ponty/pyvirtualdisplay)

Features:
 - python wrapper
 - supported python versions: 2.7, 3.6, 3.7, 3.8
 - back-ends: Xvfb_, Xephyr_, Xvnc_

Known problems:
 - only a few back-end options are supported

Possible applications:
 * GUI testing
 * automatic GUI screenshot

Basic usages
============

Start Xvnc:

```python
from pyvirtualdisplay import Display
xvfb=Display(visible=False, size=(320, 240)).start()
```

Start Xephyr:

```python
from pyvirtualdisplay import Display
xephyr=Display(visible=True, size=(320, 240)).start()
```

Create screenshot of xmessage with Xvfb:

```python
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
with SmartDisplay(visible=False, bgcolor='black') as disp:
    with EasyProcess(['xmessage', 'hello']):
        img = disp.waitgrab()
img.show()
```

Installation
============

install the program:

```console
$ python3 -m pip install pyvirtualdisplay
```

optional: pyscreenshot_ and Pillow_ should be installed for ``smartdisplay`` submodule:

```console
$ python3 -m pip install pyscreenshot pillow
```

on Ubuntu:

```console
$ sudo apt-get install xvfb xserver-xephyr vnc4server
$ python3 -m pip install pyvirtualdisplay pyscreenshot pillow
```

Usage
=====

GUI Test
--------

Testing ``gnumeric`` on low resolution (examples/lowres.py):
```python
from easyprocess import EasyProcess
from pyvirtualdisplay import Display

if __name__ == "__main__":
    # start Xephyr
    Display(visible=True, size=(320, 240)).start()
    # start Gnumeric
    EasyProcess(['gnumeric']).start()
```

Image:

![](/_img/lowres.png)

Screenshot
----------

Create screenshot of ``xmessage`` in background (examples/screenshot3.py'):
```python
'''
using :keyword:`with` statement
'''
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

if __name__ == "__main__":
    with SmartDisplay(visible=False, bgcolor='black') as disp:
        with EasyProcess(['xmessage', 'hello']):
            img = disp.waitgrab()


    img.show()
```


Image:

![](/_img/screenshot3.png)

vncserver
---------

examples/vncserver.py

```python
'''
Example for Xvnc backend
'''

from easyprocess import EasyProcess
from pyvirtualdisplay import Display

if __name__ == "__main__":
    with Display(backend='xvnc', rfbport=5904) as disp:
        with EasyProcess(['xmessage', 'hello']) as proc:
            proc.wait()
```

xauth
=====

Some programs require a functional Xauthority file. PyVirtualDisplay can
generate one and set the appropriate environment variables if you pass
``use_xauth=True`` to the ``Display`` constructor. Note however that this
feature needs ``xauth`` installed, otherwise a
``pyvirtualdisplay.xauth.NotFoundError`` is raised.


[1]: http://en.wikipedia.org/wiki/Xvfb
[2]: http://en.wikipedia.org/wiki/Xephyr
[3]: https://tigervnc.org/
[4]: https://github.com/ponty/pyscreenshot
[5]: https://pillow.readthedocs.io


