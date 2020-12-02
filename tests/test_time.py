from unittest import TestCase
from pyutility import limit_time, timeit


def func1(x):
    # recursive function to find xth fibonacci number
    if x < 3:
        return 1
    return func1(x-1) + func1(x-2)


def func2():
    # error function
    return "a" / 2


def func3(*args, **kwagrs):
    # args and kwargs function
    return list(args) + list(kwagrs.values())


class TimeitTest(TestCase):
    def setUp(self):
        self.er_func = timeit(func2)
        self.func = timeit(func1)
        self.ka_func = timeit(func3)

    def test_timeit1(self):
        self.assertIsInstance(self.func(5), float)

    def test_timeit2(self):
        self.assertRaises(Exception, self.er_func)
