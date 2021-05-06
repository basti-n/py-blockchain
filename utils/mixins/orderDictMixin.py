from collections import OrderedDict


class OrderedDictMixin:
    def __str__(self) -> str:
        return str(OrderedDict(self.__dict__.items()))

    def __repr__(self) -> str:
        return str([f'{key}: {value}' for key, value in self.__dict__.items()]).replace('\'', '')
