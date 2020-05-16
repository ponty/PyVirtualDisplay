from threading import Thread

from pyvirtualdisplay import Display


def test_with():
    ls = [0, 0]

    def f1():
        ls[0] = Display()

    #         d1.start()

    def f2():
        ls[1] = Display()

    #         d2.start()

    t1 = Thread(target=f1)
    t2 = Thread(target=f2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    #     print ls

    dv1 = ls[0].new_display_var
    dv2 = ls[1].new_display_var

    #     print dv1
    #     print dv2

    assert dv1 != dv2


#     ok_(0)
