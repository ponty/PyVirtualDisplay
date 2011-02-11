from pyvirtualdisplay.display import Display
from unittest import TestCase

class Test(TestCase):
    def test_virt(self):
        vd = Display().start().stop()
        self.assertEquals(vd.return_code, 0)
        
    def test_nest(self):
        vd = Display().start()

        nd = Display(visible=1).start().stop()
        
        self.assertEquals(nd.return_code, 0)

        vd.stop()
        
    def test_disp(self):
        vd = Display().start()

        d = Display(visible=1).start().stop()
        self.assertEquals(d.return_code, 0)

        d = Display(visible=0).start().stop()
        self.assertEquals(d.return_code, 0)
        
        vd.stop()
        
        
        
        
