from typing import Any


class SingletonMeta(type):
    __instances = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self not in self.__instances:
            instance = super().__call__(*args, **kwds)
            self.__instances[self] = instance

        return self.__instances[self]
