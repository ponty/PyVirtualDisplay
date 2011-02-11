Usage
==================

GUI Test
----------

Testing ``abiword`` on low resolution:

.. literalinclude:: ../pyvirtualdisplay/examples/lowres.py

.. program-screenshot:: python -m pyvirtualdisplay.examples.lowres
    :prompt:
    :wait: 3


Screenshot
-----------

Create screenshot of ``xmessage`` in background,
pyscreenshot_ and PIL_ should be installed:

.. literalinclude:: ../pyvirtualdisplay/examples/screenshot.py

.. program-screenshot:: python -m pyvirtualdisplay.examples.screenshot
    :prompt:


The same with wrap() function:

.. literalinclude:: ../pyvirtualdisplay/examples/screenshot2.py

.. program-screenshot:: python -m pyvirtualdisplay.examples.screenshot2
    :prompt:


.. _pyscreenshot: https://github.com/ponty/pyscreenshot
.. _PIL: http://www.pythonware.com/library/pil/
