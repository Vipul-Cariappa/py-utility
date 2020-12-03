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


class LimitTimeTest(TestCase):
    def setUp(self):
        self.er_func = limit_time(2)(func2)
        self.func = limit_time(2)(func1)
        self.ka_func = limit_time(2)(func3)

    def test_limit_time_1(self):
        self.assertEqual(self.func(10), 55)

    def test_limit_time_2(self):
        self.assertRaises(Exception, self.er_func)

    def test_limit_time_3(self):
        self.assertRaises(TimeoutError, self.func, 50)

    def test_limit_time_4(self):
        self.assertEqual(self.ka_func(
            1, 2, 3, four=4, five=5), [1, 2, 3, 4, 5])
