from collections import OrderedDict


class OrderedDictMixin:
    def __str__(self) -> str:
        return str(OrderedDict(self.__dict__.items()))
