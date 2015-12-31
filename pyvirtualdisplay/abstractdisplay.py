from easyprocess import EasyProcess
import fnmatch
import logging
import os
import time

log = logging.getLogger(__name__)

# TODO: not perfect
# randomize to avoid possible conflicts
RANDOMIZE_DISPLAY_NR = True
if RANDOMIZE_DISPLAY_NR:
    import random
    random.seed()

MIN_DISPLAY_NR = 1000


class AbstractDisplay(EasyProcess):
    '''
    Common parent for Xvfb and Xephyr
    '''

    def __init__(self):
        self.display = self.search_for_display()
        EasyProcess.__init__(self, self._cmd)

    def __del__(self):
        # Stop the display on delete to avoid 
        # "orphaned" dbus processes
        self.stop()

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
            display = max(MIN_DISPLAY_NR, max(ls) + 1)
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
        return self
