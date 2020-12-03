from unittest import TestCase
from pyutility import limit_resource, measureit


def func1a(x):
    x = [i for i in range(x)]
    return -1


def func1b(x):
    # recursive function to find xth fibonacci number
    if x < 3:
        return 1
    return func1b(x-1) + func1b(x-2)


def func2():
    # error function
    return "a" / 2


def func3(*args, **kwagrs):
    # args and kwargs function
    return list(args) + list(kwagrs.values())


class MeasureitTest(TestCase):
    def setUp(self):
        self.er_func = measureit(func2)
        self.func_m = measureit(func1a)
        self.func_t = measureit(func1b)
        self.ka_func = measureit(func3)

    def test_measureit_1(self):
        self.assertIsInstance(self.func_m(100), tuple)

    def test_measureit_2(self):
        x = self.func_t(10)
        self.assertIsInstance(x[0], int)
        self.assertIsInstance(x[1], float)

    def test_measureit_3(self):
        self.assertIsInstance(self.func_t(15), tuple)

    def test_measureit_4(self):
        self.assertRaises(Exception, self.er_func)


class LimitResourceTest(TestCase):
    def setUp(self):
        self.er_func = limit_resource(time=2)(func2)
        self.func_m = limit_resource(time=2)(func1a)
        self.func_t = limit_resource(time=2)(func1b)
        self.ka_func = limit_resource(time=2)(func3)

    def test_limit_resource_1(self):
        self.assertEqual(self.func_m(300), -1)

    def test_limit_resource_2(self):
        self.assertEqual(self.func_t(3), 2)

    def test_limit_resource_3(self):
        self.assertRaises(Exception, self.er_func)

    def test_limit_resource_4(self):
        self.assertRaises(MemoryError, self.func_m, 100_000_000)

    def test_limit_resource_5(self):
        self.assertRaises(TimeoutError, self.func_t, 50)

    def test_limit_resource_6(self):
        self.assertEqual(self.ka_func(
            1, 2, 3, four=4, five=5), [1, 2, 3, 4, 5])
