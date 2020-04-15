pyvirtualdisplay is a python wrapper for Xvfb_, Xephyr_ and Xvnc_

Links:
 * home: https://github.com/ponty/pyvirtualdisplay
 * PYPI: https://pypi.python.org/pypi/pyvirtualdisplay

|Travis| |License|

Features:
 - python wrapper
 - supported python versions: 2.7, 3.5, 3.6, 3.7, 3.8
 - back-ends: Xvfb_, Xephyr_, Xvnc_

Known problems:
 - only a few back-end options are supported

Possible applications:
 * GUI testing
 * automatic GUI screenshot

Basic usages
============

Start Xephyr::

    from pyvirtualdisplay import Display
    xephyr=Display(visible=True, size=(320, 240)).start()

Create screenshot of xmessage with Xvfb::

    from easyprocess import EasyProcess
    from pyvirtualdisplay.smartdisplay import SmartDisplay
    with SmartDisplay(visible=False, bgcolor='black') as disp:
        with EasyProcess('xmessage hello'):
            img = disp.waitgrab()
    img.show()

Installation
============

install the program::

    pip3 install pyvirtualdisplay

optional: pyscreenshot_ and Pillow_ should be installed for ``smartdisplay`` submodule::

    pip3 install pyscreenshot pillow

on Ubuntu::

    sudo apt-get install xvfb xserver-xephyr vnc4server
    pip3 install pyvirtualdisplay pyscreenshot pillow

Usage
=====

..  #-- from docs.screenshot import screenshot--#  
..  #-#

GUI Test
--------

Testing ``gnumeric`` on low resolution::

  #-- include('examples/lowres.py') --#
  from easyprocess import EasyProcess
  from pyvirtualdisplay import Display

  if __name__ == "__main__":
      # start Xephyr
      Display(visible=True, size=(320, 240)).start()
      # start Gnumeric
      EasyProcess('gnumeric').start()
  #-#

Image:

.. #-- screenshot('python -m pyvirtualdisplay.examples.lowres','lowres.png') --#
.. image:: _img/lowres.png
.. #-#

Screenshot
----------

Create screenshot of ``xmessage`` in background::

  #-- include('examples/screenshot3.py') --#
  '''
  using :keyword:`with` statement
  '''
  from easyprocess import EasyProcess
  from pyvirtualdisplay.smartdisplay import SmartDisplay

  if __name__ == "__main__":
      with SmartDisplay(visible=False, bgcolor='black') as disp:
          with EasyProcess('xmessage hello'):
              img = disp.waitgrab()


      img.show()
  #-#


Image:

..  #-- screenshot('python -m pyvirtualdisplay.examples.screenshot3','screenshot3.png') --#
.. image:: _img/screenshot3.png
..  #-#
    
vncserver
---------

::

  #-- include('examples/vncserver.py') --#
  '''
  Example for Xvnc backend
  '''

  from easyprocess import EasyProcess
  from pyvirtualdisplay.display import Display

  if __name__ == "__main__":
      with Display(backend='xvnc', rfbport=5904) as disp:
          with EasyProcess('xmessage hello') as proc:
              proc.wait()
  #-#

xauth
=====

Some programs require a functional Xauthority file. PyVirtualDisplay can
generate one and set the appropriate environment variables if you pass
``use_xauth=True`` to the ``Display`` constructor. Note however that this
feature needs ``xauth`` installed, otherwise a
``pyvirtualdisplay.xauth.NotFoundError`` is raised.


.. _Xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Xephyr: http://en.wikipedia.org/wiki/Xephyr
.. _Xvnc: http://www.hep.phy.cam.ac.uk/vnc_docs/xvnc.html
.. _pyscreenshot: https://github.com/ponty/pyscreenshot
.. _Pillow: https://pillow.readthedocs.io


.. |Travis| image:: https://travis-ci.org/ponty/PyVirtualDisplay.svg?branch=master
   :target: https://travis-ci.org/ponty/PyVirtualDisplay/
.. |License| image:: https://img.shields.io/pypi/l/PyVirtualDisplay.svg
   :target: https://pypi.python.org/pypi/PyVirtualDisplay/
