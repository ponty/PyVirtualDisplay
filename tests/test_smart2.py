from easyprocess import EasyProcess

from pyvirtualdisplay.smartdisplay import SmartDisplay

# from path import path
# import pyscreenshot


def check_double(backend1, backend2=None):
    if not backend2:
        backend2 = backend1

    with SmartDisplay(visible=0, bgcolor="black") as disp:
        disp.pyscreenshot_backend = backend1
        disp.pyscreenshot_childprocess = True  # error if FALSE
        with EasyProcess("xmessage hello1"):
            img = disp.waitgrab()
            assert img is not None

    with SmartDisplay(visible=0, bgcolor="black") as disp:
        disp.pyscreenshot_backend = backend2
        disp.pyscreenshot_childprocess = True  # error if FALSE
        with EasyProcess("xmessage hello2"):
            img = disp.waitgrab()
            assert img is not None


#     def test_double_wx():
#         .check_double('wx')

#     def test_double_pygtk():
#         .check_double('pygtk')

#     def test_double_pyqt():
#         .check_double('pyqt')

#     def test_double_imagemagick():
#         .check_double('imagemagick')


def test_double_scrot():
    check_double("scrot")


#     def test_double_imagemagick_scrot():
#         .check_double('imagemagick', 'scrot')

#     def test_double_wx_pygtk():
#         .check_double('wx', 'pygtk')

#     def test_double_wx_pyqt():
#         .check_double('wx', 'pyqt')

#     def test_double_pygtk_pyqt():
#         .check_double('pygtk', 'pyqt')
