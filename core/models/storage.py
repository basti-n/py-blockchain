from abc import abstractmethod
from io import TextIOWrapper
from utils.metaclasses.singletonMeta import SingletonMeta
from typing import Any, Union
from enum import Enum


class StorageAction(Enum):
    SAVING = 'saving'
    LOADING = 'loading'


class Storage(metaclass=SingletonMeta):
    def __init__(self, path: str) -> None:
        self.path = path

    @abstractmethod
    def load() -> Any:
        pass

    @abstractmethod
    def save() -> bool:
        pass

    @classmethod
    def generate_path(cls, *, prefix: str = '', suffix: str = '', id: Union[str, int] = '', divider: str = '-', format: str = '.txt') -> str:
        """ Generates a file storage path """
        beginning = f'{prefix}{divider}' if len(prefix) else ''
        end = f'{divider}{suffix}' if len(suffix) else ''
        return f'{beginning}{id}{end}{format}'

    def print_success(self, action: StorageAction) -> None:
        print(
            f'Completed: {action.value.capitalize()} {self.path} successful!')

    def print_error(self, action: StorageAction) -> None:
        print(f'Alert: {action.value.capitalize()} {self.path} failed!')

    def add_line_break(self, file: TextIOWrapper) -> int:
        return file.write('\n')
