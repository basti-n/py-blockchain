from abc import ABC, abstractmethod


class Resolver(ABC):
    @abstractmethod
    def resolve(self) -> bool:
        pass
