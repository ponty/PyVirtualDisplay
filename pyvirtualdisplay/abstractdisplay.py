from easyprocess import EasyProcess, EasyProcessError
import fnmatch
import logging
import os
import time
import tempfile
from threading import Lock
import select
try:
    import fcntl
except ImportError:
    fcntl = None

from pyvirtualdisplay import xauth

mutex = Lock()

log = logging.getLogger(__name__)

MIN_DISPLAY_NR = 1000
USED_DISPLAY_NR_LIST=[]

X_START_TIMEOUT = 10
X_START_TIME_STEP = 0.1
X_START_WAIT = 0.1

class XStartTimeoutError(Exception):
    pass

class AbstractDisplay(EasyProcess):
    '''
    Common parent for Xvfb and Xephyr
    '''
    def __init__(self, use_xauth=False, check_startup=False, randomizer=None):
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
        self.check_startup = check_startup
        if check_startup and not fcntl:
            self.check_startup = False
            log.warning("fcntl module can't be imported, 'check_startup' parameter has been disabled")
            log.warning("fnctl module does not exist on Windows")
        if self.check_startup:
            rp, wp = os.pipe()
            fcntl.fcntl(rp, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
            #to properly allow to inherit fds to subprocess on
            #python 3.2+ the easyprocess needs small fix..
            fcntl.fcntl(wp, fcntl.F_SETFD, 0)
            self.check_startup_fd = wp
            self._check_startup_fd = rp
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
        if self.check_startup:
            rp = self._check_startup_fd
            display_check = None
            rlist, wlist, xlist = select.select((rp,), (), (), X_START_TIMEOUT)
            if rlist:
                display_check = os.read(rp, 10).rstrip()
            else:
                msg = 'No display number returned by X server'
                raise XStartTimeoutError(msg)
            dnbs = str(self.display)
            if bytes != str:
                dnbs = bytes(dnbs, 'ascii')
            if display_check != dnbs:
                msg = 'Display number "%s" not returned by X server' + str(display_check)
                raise XStartTimeoutError(msg % self.display)

        d = self.new_display_var
        ok = False
        while True:
            try:
                xdpyinfo = EasyProcess('xdpyinfo')
                xdpyinfo.enable_stdout_log = False
                xdpyinfo.enable_stderr_log = False
                exit_code = xdpyinfo.call().return_code
            except EasyProcessError:
                log.warning('xdpyinfo was not found, X start can not be checked! Please install xdpyinfo!')
                time.sleep(X_START_WAIT)    # old method
                ok = True
                break

            if exit_code != 0:
                pass
            else:
                log.info('Successfully started X with display "%s".', d)
                ok = True
                break

            if time.time() - start_time >= X_START_TIMEOUT:
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
