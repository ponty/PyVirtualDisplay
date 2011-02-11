from pyvirtualdisplay.xephyr import XephyrDisplay
from pyvirtualdisplay.xvfb import XvfbDisplay


def Display(visible=False, size=(1024, 768), color_depth=24, bgcolor='black'):
    '''
    Factory for XvfbDisplay and XephyrDisplay
    
    :param color_depth: [8, 16, 24, 32] 
    :param size: screen size (width,height)
    :param bgcolor: background color ['black' or 'white']
    :param visible: True -> Xephyr, False -> Xvfb
    '''
    #d = dict(nested=NestedDisplay, virtual=VirtualDisplay)
    ls = [XvfbDisplay, XephyrDisplay]
    cl = ls[visible]
    return cl(size=size,
              color_depth=color_depth,
              bgcolor=bgcolor)

    


