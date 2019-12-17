from easyprocess import EasyProcess
from pyvirtualdisplay.abstractdisplay import AbstractDisplay
import logging

log = logging.getLogger(__name__)

PROGRAM = 'Xvnc'


class XvncDisplay(AbstractDisplay):
    '''
    Xvnc wrapper
    '''
    def __init__(self, size=(1024, 768), color_depth=24, bgcolor='black', rfbport=5900, rfbauth=None, randomizer=None):
        '''
        :param bgcolor: 'black' or 'white'
        :param rfbport: Specifies the TCP port on which Xvnc listens for connections from viewers (the protocol used in VNC is called RFB - "remote framebuffer"). The default is 5900 plus the display number.
        :param rfbauth: Specifies the file containing the password used to authenticate viewers.
        '''
        self.screen = 0
        self.size = size
        self.color_depth = color_depth
        self.process = None
        self.bgcolor = bgcolor
        self.display = None
        self.rfbport = rfbport
        self.rfbauth = rfbauth
        AbstractDisplay.__init__(self, randomizer=randomizer)

    @classmethod
    def check_installed(cls):
        p = EasyProcess([PROGRAM, '-help'])
        p.enable_stdout_log = False
        p.enable_stderr_log = False
        p.call()

    @property
    def _cmd(self):
        cmd = [PROGRAM,
               '-depth', str(self.color_depth),
               '-geometry', '%dx%d' % (self.size[0], self.size[1]),
               '-rfbport', str(self.rfbport)]
        
        if self.rfbauth:
               cmd += ['-rfbauth', str(self.rfbauth)]
        
        cmd += [self.new_display_var,]
        
        if self.check_startup:
            cmd += ['-displayfd', str(self.check_startup_fd)]
        return cmd
