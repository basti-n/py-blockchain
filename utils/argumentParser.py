from argparse import ArgumentParser, Namespace
from typing import Any, Dict


class CommandLineArgumentParser:
    def __init__(self, cliArgs: Dict[str, Dict[str, Any]] = {}) -> None:
        self.parser = ArgumentParser()
        self.__initialize(cliArgs)

    @property
    def arguments(self) -> Namespace:
        return self.parser.parse_args()

    def __initialize(self, cliArgs: Dict[str, Dict[str, Any]]) -> None:
        """ Registers cli arguments """
        for arg in cliArgs:
            abbreviated_name = arg[0]
            config = cliArgs[arg]
            default_value = config['default']
            type = config['type']
            self.parser.add_argument(
                self.__get_short_flag(abbreviated_name), self.__get_long_flag(arg), type=type, default=default_value)

    def __get_short_flag(self, name: str) -> str:
        return '-' + name

    def __get_long_flag(self, name: str) -> str:
        return '--' + name
