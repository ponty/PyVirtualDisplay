from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay
from pyvirtualdisplay.xvnc import XvncDisplay

class_map = {"xvfb": XvfbDisplay, "xvnc": XvncDisplay, "xephyr": XephyrDisplay}


class Display(object):
    """
    Proxy class

    :param color_depth: [8, 16, 24, 32]
    :param size: screen size (width,height)
    :param bgcolor: background color ['black' or 'white']
    :param visible: True -> Xephyr, False -> Xvfb
    :param backend: 'xvfb', 'xvnc' or 'xephyr', ignores ``visible``
    :param xauth: If a Xauthority file should be created.
    """

    def __init__(
        self,
        backend=None,
        visible=False,
        size=(1024, 768),
        color_depth=24,
        bgcolor="black",
        use_xauth=False,
        # check_startup=False,
        randomizer=None,
        retries=10,
        **kwargs
    ):
        self.color_depth = color_depth
        self.size = size
        self.bgcolor = bgcolor
        self.visible = visible
        self.backend = backend

        if not self.backend:
            if self.visible:
                self.backend = "xephyr"
            else:
                self.backend = "xvfb"

        cls = class_map.get(self.backend)
        if not cls:
            raise ValueError("unknown backend: %s" % self.backend)

        self._obj = cls(
            size=size,
            color_depth=color_depth,
            bgcolor=bgcolor,
            randomizer=randomizer,
            use_xauth=use_xauth,
            # check_startup=check_startup,
            **kwargs
        )

    def start(self):
        """
        start display

        :rtype: self
        """
        self._obj.start()
        self.display = self._obj.display
        self.new_display_var = self._obj.new_display_var
        return self

    def stop(self):
        """
        stop display

        :rtype: self
        """
        self._obj.stop()
        return self

    def __enter__(self):
        """used by the :keyword:`with` statement"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """used by the :keyword:`with` statement"""
        self.stop()

    def is_alive(self):
        return self._obj.is_alive()

    @property
    def return_code(self):
        return self._obj.return_code

    @property
    def pid(self):
        """
        PID (:attr:`subprocess.Popen.pid`)

        :rtype: int
        """
        return self._obj.pid
