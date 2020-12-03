from unittest import TestCase
from pyutility import limit_memory, memoryit


def func1(x):
    x = [i for i in range(x)]
    return -1


def func2():
    # error function
    return "a" / 2


def func3(*args, **kwagrs):
    # args and kwargs function
    return list(args) + list(kwagrs.values())


class MemoryitTest(TestCase):
    def setUp(self):
        self.er_func = memoryit(func2)
        self.func = memoryit(func1)
        self.ka_func = memoryit(func3)

    def test_memoryit_1(self):
        self.assertIsInstance(self.func(5), int)

    def test_memoryit_2(self):
        self.assertRaises(Exception, self.er_func)


class LimitMemoryTest(TestCase):
    def setUp(self):
        self.er_func = limit_memory()(func2)
        self.func = limit_memory()(func1)
        self.ka_func = limit_memory()(func3)

    def test_limit_memory_1(self):
        self.assertEqual(self.func(3), -1)

    def test_limit_memory_2(self):
        self.assertRaises(Exception, self.er_func)

    def test_limit_memory_3(self):
        self.assertRaises(MemoryError, self.func, 100_000_000)

    def test_limit_memory_4(self):
        self.assertEqual(self.ka_func(
            1, 2, 3, four=4, five=5), [1, 2, 3, 4, 5])
