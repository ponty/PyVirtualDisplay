from pyvirtualdisplay.abstractdisplay import AbstractDisplay
from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay


class Display(AbstractDisplay):
    '''
    Common class for XvfbDisplay and XephyrDisplay
    
    '''
    def __init__(self, visible=False, size=(1024, 768), color_depth=24, bgcolor='black'):
        '''
        :param color_depth: [8, 16, 24, 32] 
        :param size: screen size (width,height)
        :param bgcolor: background color ['black' or 'white']
        :param visible: True -> Xephyr, False -> Xvfb
        '''
        self.color_depth = color_depth
        self.size = size
        self.bgcolor = bgcolor
        self.screen = 0
        self.process = None
        self.display = None

        self.visible = visible
        self._obj = self.display_class( 
              size=size,
              color_depth=color_depth,
              bgcolor=bgcolor)
    
    @property
    def display_class(self):
        if self.visible:
            return XephyrDisplay
        else:
            return XvfbDisplay

    @property
    def cmd(self):
        self._obj.display=self.display
        return self._obj.cmd


