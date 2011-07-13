pyvirtualdisplay is a python wrapper for Xvfb_ and Xephyr_

Links:
 * home: https://github.com/ponty/PyVirtualDisplay
 * documentation: http://ponty.github.com/PyVirtualDisplay

Possible applications:
 * GUI testing
 * automatic GUI screenshot

Basic usages
============

Start Xephyr::

    from pyvirtualdisplay import Display
    xephyr=Display(visible=1, size=(320, 240)).start()

Create screenshot of xmessage with Xvfb::

    from easyprocess import EasyProcess
    from pyvirtualdisplay.smartdisplay import SmartDisplay
    disp = SmartDisplay(visible=0, bgcolor='black').start()
    xmessage = EasyProcess('xmessage hello').start()
    img = disp.waitgrab()
    xmessage.stop()
    disp.stop()
    img.show()

Installation
============

General
--------

 * install Xvfb_ and Xephyr_.
 * install setuptools_ or pip_
 * optional: pyscreenshot_ and PIL_ should be installed for ``smartdisplay`` submodule
 * install the program:

if you have setuptools_ installed::

    # as root
    easy_install pyvirtualdisplay

if you have pip_ installed::

    # as root
    pip install pyvirtualdisplay

Ubuntu
----------
::

    sudo apt-get install python-setuptools
    sudo apt-get install xvfb
    sudo apt-get install xserver-xephyr
    sudo easy_install pyvirtualdisplay
    # optional
    sudo apt-get install python-imaging
    sudo apt-get install scrot
    sudo easy_install pyscreenshot


Uninstall
----------
::

    # as root
    pip uninstall pyvirtualdisplay


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _Xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Xephyr: http://en.wikipedia.org/wiki/Xephyr
.. _pyscreenshot: https://github.com/ponty/pyscreenshot
.. _PIL: http://www.pythonware.com/library/pil/
