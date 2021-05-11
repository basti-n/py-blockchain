from abc import abstractmethod
import core.blockchainConstants as blockchainConstants
import core.blockchainTx as blockchainTx
from utils.metaclasses.singletonMeta import SingletonMeta
from typing import List, Tuple
from enum import Enum


class StorageAction(Enum):
    SAVING = 'saving'
    LOADING = 'loading'


class Storage(metaclass=SingletonMeta):
    def __init__(self, path: str) -> None:
        self.path = path

    @abstractmethod
    def load() -> Tuple[List[blockchainConstants.Block], List[blockchainTx.Transaction]]:
        pass

    @abstractmethod
    def save() -> bool:
        pass

    def print_success(self, action: StorageAction) -> None:
        print(f'Completed: {action.value.capitalize()} {self.path} successful!')

    def print_error(self, action: StorageAction) -> None:
        print(f'Alert: {action.value.capitalize()} {self.path} failed!')
