import unittest
from wafec_wrapt_custom.wrappers import WrapperTest


class Aux(object):
    def __init__(self):
        self.item1 = Item(1)
        self.item2 = Item(2)

    def __repr__(self):
        return '<Aux(item1={}, item2={})>'.format(self.item1.value, self.item2.value)


class Item(object):
    def __init__(self, value):
        self.value = value


class TestWrapperTest(unittest.TestCase):
    def test_hello(self):
        wrapped = Aux()
        wrapper = WrapperTest(wrapped)
        self.assertTrue(isinstance(wrapper, Aux))
        self.assertTrue(isinstance(wrapper, WrapperTest))
        self.assertTrue(isinstance(wrapper.item1, WrapperTest))
        item3 = Item(3)
        wrapper.item2 = item3
        self.assertTrue(isinstance(wrapper.item2, WrapperTest))
        self.assertEqual(3, wrapper.item2.value)
        self.assertTrue(isinstance(wrapper.item2.value, WrapperTest))
        self.assertTrue(isinstance(wrapper.item2.value, int))

    def test_list(self):
        wrapped = [Aux(), Aux(), Aux()]
        wrapper = WrapperTest(wrapped)
        for item in wrapper:
            self.assertTrue(isinstance(item, WrapperTest))

    def test_dict(self):
        wrapped = {'item1': Aux(), 'item2': Aux()}
        wrapper = WrapperTest(wrapped)
        self.assertTrue(isinstance(wrapper['item1'], WrapperTest))
        self.assertTrue(isinstance(wrapper['item2'], WrapperTest))
        self.assertEqual(2, wrapper['item1'].item2.value)

    def test_kwargs(self):
        def func(item1, item2):
            self.assertTrue(isinstance(item1, WrapperTest))
            self.assertTrue(isinstance(item2, WrapperTest))

        wrapped = {'item1': Aux(), 'item2': Aux()}
        wrapper = WrapperTest.wrap_kwargs(wrapped)
        func(**wrapper)


if __name__ == '__main__':
    unittest.main()
