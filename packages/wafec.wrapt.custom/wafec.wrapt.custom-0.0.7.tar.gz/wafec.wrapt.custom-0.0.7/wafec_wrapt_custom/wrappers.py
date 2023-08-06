from abc import ABC

import wrapt
import copy

_simple_types = (str, int, type(None), bool, float)


class WrapperTest(wrapt.ObjectProxy, ABC):
    def __init__(self, wrapped):
        super(WrapperTest, self).__init__(WrapperTest.unwrap(wrapped))
        self._validate_type()

    def _validate_type(self):
        if isinstance(self.__wrapped__, _simple_types):
            raise TypeError('Cannot be simple')

    def __getitem__(self, item):
        return WrapperTest.will_wrap(super(WrapperTest, self).__getitem__(item))

    def __setitem__(self, item, value):
        if isinstance(value, WrapperTest):
            super(WrapperTest, self).__setitem__(item, value.__wrapped__)
        else:
            super(WrapperTest, self).__setitem__(item, value)

    def __getattr__(self, name):
        return WrapperTest.will_wrap(super(WrapperTest, self).__getattr__(name))

    def __setattr__(self, name, value):
        if isinstance(value, WrapperTest):
            super(WrapperTest, self).__setattr__(name, value.__wrapped__)
        else:
            super(WrapperTest, self).__setattr__(name, value)

    def __copy__(self):
        return WrapperTest.will_wrap(copy.copy(self.__wrapped__))

    def __deepcopy__(self, memodict={}):
        return WrapperTest.will_wrap(copy.deepcopy(self.__wrapped__, memodict))

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

    @staticmethod
    def wrap_kwargs(kwargs):
        for argname, argvalue in kwargs.items():
            kwargs[argname] = WrapperTest.will_wrap(argvalue)
        return kwargs

    @staticmethod
    def unwrap(obj):
        if obj is not None and isinstance(obj, WrapperTest):
            return obj.__wrapped__
        return obj

    @staticmethod
    def will_wrap(obj):
        if isinstance(obj, _simple_types):
            return obj
        return WrapperTest(obj)

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)
