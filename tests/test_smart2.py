from unittest import TestCase

from easyprocess import EasyProcess
from nose.tools import eq_

from pyvirtualdisplay.smartdisplay import SmartDisplay

# from path import path
# import pyscreenshot


class Test(TestCase):
    def check_double(self, backend1, backend2=None):
        if not backend2:
            backend2 = backend1

        with SmartDisplay(visible=0, bgcolor='black') as disp:
            disp.pyscreenshot_backend = backend1
            disp.pyscreenshot_childprocess = True  # error if FALSE
            with EasyProcess('xmessage hello1'):
                img = disp.waitgrab()
                eq_(img is not None, True)

        with SmartDisplay(visible=0, bgcolor='black') as disp:
            disp.pyscreenshot_backend = backend2
            disp.pyscreenshot_childprocess = True  # error if FALSE
            with EasyProcess('xmessage hello2'):
                img = disp.waitgrab()
                eq_(img is not None, True)

#     def test_double_wx(self):
#         self.check_double('wx')

#     def test_double_pygtk(self):
#         self.check_double('pygtk')

#     def test_double_pyqt(self):
#         self.check_double('pyqt')

#     def test_double_imagemagick(self):
#         self.check_double('imagemagick')

    def test_double_scrot(self):
        self.check_double('scrot')

#     def test_double_imagemagick_scrot(self):
#         self.check_double('imagemagick', 'scrot')

#     def test_double_wx_pygtk(self):
#         self.check_double('wx', 'pygtk')

#     def test_double_wx_pyqt(self):
#         self.check_double('wx', 'pyqt')

#     def test_double_pygtk_pyqt(self):
#         self.check_double('pygtk', 'pyqt')
