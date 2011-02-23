from easyprocess import EasyProcess
from path import path
import logging
import os
import time

log = logging.getLogger(__name__)

class AbstractDisplay(EasyProcess):
    '''
    Common parent for Xvfb and Xephyr
    '''
    
    @property
    def new_display_var(self):
        return ':{display}'.format(display=self.display)
    
    @property
    def cmd(self):
        raise NotImplementedError()

    def search_for_display(self):
        # search for free display
        ls = path('/tmp').files('.X*-lock')
        ls = map(lambda x:int(x.split('X')[1].split('-')[0]), ls)
        if len(ls):
            display = max(ls) + 1
        else:
            display = 100
        return display
                
    def redirect_display(self, on):
        '''
        on:
         * True -> set $DISPLAY to virtual screen
         * False -> set $DISPLAY to original screen
        
        :param on: bool
        '''
        d = self.new_display_var if on else self.old_display_var
        log.debug('DISPLAY=' + d)
        os.environ['DISPLAY'] = d

    def start(self):
        '''
        start display
        
        :rtype: self
        '''
        self.display=self.search_for_display()
        EasyProcess.__init__(self,self.cmd)
        EasyProcess.start(self)
        self.old_display_var = os.environ['DISPLAY']
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

        
        
        
        
        
        
        
        
        
