from pyvirtualdisplay.abstractdisplay import AbstractDisplay
from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay
from pyvirtualdisplay.xvnc import XvncDisplay

class_map = {"xvfb": XvfbDisplay, "xvnc": XvncDisplay, "xephyr": XephyrDisplay}


class Display(AbstractDisplay):
    """
    Common class

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
        check_startup=False,
        randomizer=None,
        **kwargs
    ):
        self.color_depth = color_depth
        self.size = size
        self.bgcolor = bgcolor
        self.screen = 0
        self.process = None
        self.display = None
        self.visible = visible
        self.backend = backend

        if not self.backend:
            if self.visible:
                self.backend = "xephyr"
            else:
                self.backend = "xvfb"

        if not self.backend:
            raise ValueError("missing backend")

        cls = class_map.get(self.backend)
        if not cls:
            raise ValueError("unknown backend: %s" % self.backend)

        # TODO: check only once
        cls.check_installed()

        self._obj = cls(
            size=size,
            color_depth=color_depth,
            bgcolor=bgcolor,
            randomizer=randomizer,
            **kwargs
        )
        AbstractDisplay.__init__(
            self,
            use_xauth=use_xauth,
            check_startup=check_startup,
            randomizer=randomizer,
        )

    @property
    def _cmd(self):
        self._obj.display = self.display
        self._obj.check_startup = self.check_startup
        if self.check_startup:
            self._obj.check_startup_fd = self.check_startup_fd
        return self._obj._cmd

    def __enter__(self):
        """used by the :keyword:`with` statement"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """used by the :keyword:`with` statement"""
        self.stop()

    def is_alive(self):
        return self.proc.is_alive()

    @property
    def return_code(self):
        return self.proc.return_code
