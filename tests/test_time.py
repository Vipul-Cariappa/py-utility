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
    return args + kwagrs.values()


class TimeUtilTest(TestCase):
    def test_timeit1(self):
        func = timeit(func1)
        self.assertIsInstance(func(5), float)

        # func = timeit(func1)
        # self.assertIsInstance(func(35), float)

        # func = timeit(func2)
        # # self.assertIsInstance(func(5), int)
        # self.assertRaises(Exception, func)

        # # func = timeit(func1)
        # # self.assertIsInstance(func(5), int)
