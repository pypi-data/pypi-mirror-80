from abc import ABC

import wrapt
import copy


class WrapperTest(wrapt.ObjectProxy, ABC):
    def __init__(self, wrapped):
        super(WrapperTest, self).__init__(wrapped)

    def __getitem__(self, item):
        return WrapperTest(super(WrapperTest, self).__getitem__(item))

    def __setitem__(self, item, value):
        if isinstance(value, WrapperTest):
            super(WrapperTest, self).__setitem__(item, value.__wrapped__)
        else:
            super(WrapperTest, self).__setitem__(item, value)

    def __getattr__(self, name):
        return WrapperTest(super(WrapperTest, self).__getattr__(name))

    def __setattr__(self, name, value):
        if isinstance(value, WrapperTest):
            super(WrapperTest, self).__setattr__(name, value.__wrapped__)
        else:
            super(WrapperTest, self).__setattr__(name, value)

    def __copy__(self):
        return WrapperTest(copy.copy(self.__wrapped__))

    def __deepcopy__(self, memodict={}):
        return WrapperTest(copy.deepcopy(self.__wrapped__, memodict))

    def __iter__(self):
        self._self_n = 0
        return self

    def __next__(self):
        if self._self_n < len(self):
            n = self._self_n
            self._self_n += 1
            return self[n]
        else:
            raise StopIteration
