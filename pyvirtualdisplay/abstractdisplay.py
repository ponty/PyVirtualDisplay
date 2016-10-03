from easyprocess import EasyProcess
import fnmatch
import logging
import os
import time
import tempfile
from threading import Lock

from pyvirtualdisplay import xauth

mutex = Lock()

log = logging.getLogger(__name__)

# TODO: not perfect
# randomize to avoid possible conflicts
RANDOMIZE_DISPLAY_NR = False
if RANDOMIZE_DISPLAY_NR:
    import random
    random.seed()

MIN_DISPLAY_NR = 1000
USED_DISPLAY_NR_LIST=[]

class AbstractDisplay(EasyProcess):
    '''
    Common parent for Xvfb and Xephyr
    '''

    def __init__(self, use_xauth=False):
        mutex.acquire()
        try:
            self.display = self.search_for_display()
            while self.display in USED_DISPLAY_NR_LIST:
                self.display+=1
            USED_DISPLAY_NR_LIST.append(self.display)
        finally:
            mutex.release()
        if xauth and not xauth.is_installed():
            raise xauth.NotFoundError()
        self.use_xauth = use_xauth
        self._old_xauth = None
        self._xauth_filename = None
        EasyProcess.__init__(self, self._cmd)

    @property
    def new_display_var(self):
        return ':%s' % (self.display)

    @property
    def _cmd(self):
        raise NotImplementedError()

    def lock_files(self):
        tmpdir = '/tmp'
        pattern = '.X*-lock'
#        ls = path('/tmp').files('.X*-lock')
        # remove path.py dependency
        names = fnmatch.filter(os.listdir(tmpdir), pattern)
        ls = [os.path.join(tmpdir, child) for child in names]
        ls = [p for p in ls if os.path.isfile(p)]
        return ls

    def search_for_display(self):
        # search for free display
        ls = map(
            lambda x: int(x.split('X')[1].split('-')[0]), self.lock_files())
        if len(ls):
            display = max(MIN_DISPLAY_NR, max(ls) + 3)
        else:
            display = MIN_DISPLAY_NR

        if RANDOMIZE_DISPLAY_NR:
            display += random.randint(0, 100)
        return display

    def redirect_display(self, on):
        '''
        on:
         * True -> set $DISPLAY to virtual screen
         * False -> set $DISPLAY to original screen

        :param on: bool
        '''
        d = self.new_display_var if on else self.old_display_var
        if d is None:
            log.debug('unset DISPLAY')
            del os.environ['DISPLAY']
        else:
            log.debug('DISPLAY=%s', d)
            os.environ['DISPLAY'] = d

    def start(self):
        '''
        start display

        :rtype: self
        '''
        if self.use_xauth:
            self._setup_xauth()
        EasyProcess.start(self)

        # https://github.com/ponty/PyVirtualDisplay/issues/2
        # https://github.com/ponty/PyVirtualDisplay/issues/14
        self.old_display_var = os.environ.get('DISPLAY', None)

        self.redirect_display(True)
        # wait until X server is active
        # TODO: better method
        time.sleep(0.1)
        return self

    def stop(self):
        '''
        stop display

        :rtype: self
        '''
        self.redirect_display(False)
        EasyProcess.stop(self)
        if self.use_xauth:
            self._clear_xauth()
        return self

    def _setup_xauth(self):
        '''
        Set up the Xauthority file and the XAUTHORITY environment variable.
        '''
        handle, filename = tempfile.mkstemp(prefix='PyVirtualDisplay.',
                                            suffix='.Xauthority')
        self._xauth_filename = filename
        os.close(handle)
        # Save old environment
        self._old_xauth = {}
        self._old_xauth['AUTHFILE'] = os.getenv('AUTHFILE')
        self._old_xauth['XAUTHORITY'] = os.getenv('XAUTHORITY')

        os.environ['AUTHFILE'] = os.environ['XAUTHORITY'] = filename
        cookie = xauth.generate_mcookie()
        xauth.call('add', self.new_display_var, '.', cookie)

    def _clear_xauth(self):
        '''
        Clear the Xauthority file and restore the environment variables.
        '''
        os.remove(self._xauth_filename)
        for varname in ['AUTHFILE', 'XAUTHORITY']:
            if self._old_xauth[varname] is None:
                del os.environ[varname]
            else:
                os.environ[varname] = self._old_xauth[varname]
        self._old_xauth = None
