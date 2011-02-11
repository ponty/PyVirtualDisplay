PyVirtualDisplay is a python wrapper for Xvfb_ and Xephyr_

home: https://github.com/ponty/PyVirtualDisplay

documentation: http://ponty.github.com/PyVirtualDisplay

Possible applications:
 * GUI testing
 * automatic GUI screenshot

Basic usage
============

::

    from pyvirtualdisplay import Display
    # Start Xephyr
    disp1=Display(visible=1, size=(320, 240)).start()


Installation
============

General
--------

The easiest way to get abandi is if you have setuptools_ installed::

    # as root
    easy_install PyVirtualDisplay

or if you have pip_ installed::

    # as root
    pip install PyVirtualDisplay

Uninstall::

    # as root
    pip uninstall PyVirtualDisplay

Ubuntu
----------
::

    sudo apt-get install python-setuptools
    sudo apt-get install xvfb
    sudo apt-get install xephyr
    sudo easy_install PyVirtualDisplay


.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pip.openplans.org/
.. _Xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Xephyr: http://en.wikipedia.org/wiki/Xephyr
