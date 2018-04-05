from easyprocess import EasyProcess, EasyProcessError
import fnmatch
import logging
import os
import time
import tempfile
from threading import Lock

from pyvirtualdisplay import xauth

mutex = Lock()

log = logging.getLogger(__name__)

MIN_DISPLAY_NR = 1000
USED_DISPLAY_NR_LIST=[]

X_START_TIMEOUT = 1
X_START_TIME_STEP = 0.1
X_START_WAIT = 0.1

class XStartTimeoutError(Exception):
    pass

class AbstractDisplay(EasyProcess):
    '''
    Common parent for Xvfb and Xephyr
    '''

    def __init__(self, use_xauth=False, randomizer=None):
        with mutex:
            self.display = self.search_for_display(randomizer=randomizer)

            while self.display in USED_DISPLAY_NR_LIST:
                self.display+=1

            USED_DISPLAY_NR_LIST.append(self.display)

        if use_xauth and not xauth.is_installed():
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

    def search_for_display(self, randomizer=None):
        # search for free display
        ls = list(map(
            lambda x: int(x.split('X')[1].split('-')[0]), self.lock_files()))
        if len(ls):
            display = max(MIN_DISPLAY_NR, max(ls) + 3)
        else:
            display = MIN_DISPLAY_NR

        if randomizer:
            display = randomizer.generate()

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
        start_time = time.time()
        ok = False
        d = self.new_display_var
        while time.time() - start_time < X_START_TIMEOUT:
            try:
                exit_code = EasyProcess('xdpyinfo').call().return_code
            except EasyProcessError:
                log.warn('xdpyinfo was not found, X start can not be checked! Please install xdpyinfo!')
                time.sleep(X_START_WAIT)    # old method
                ok = True
                break

            if exit_code != 0:
                pass
            else:
                log.info('Successfully started X with display "%s".', d)
                ok = True
                break

            time.sleep(X_START_TIME_STEP)
        if not ok:
            msg = 'Failed to start X on display "%s" (xdpyinfo check failed).'
            raise XStartTimeoutError(msg % d)
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
