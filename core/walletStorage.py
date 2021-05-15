
from core.models.storage import StorageAction
from typing import Tuple, Union
from core.blockchainStorage import Storage


STORAGE_FILE = 'wallet.txt'


class WalletStorage(Storage):
    def __init__(self, path=STORAGE_FILE) -> None:
        super().__init__(path)

    def load(self) -> Union[Tuple[str, str], None]:
        """ Loads the public and private key from the stored file """

        try:
            with open(self.path, mode="r") as file:
                keys = file.readlines()

                if len(keys) < 2:
                    print('No keys found in {}.'.format(self.path))
                    return None

                public_key = keys[0][:-1]
                private_key = keys[1]

                print('===' * 30)
                print(public_key)
                print(private_key)
                print('===' * 30)

                self.print_success(StorageAction.LOADING)
                return (public_key, private_key)

        except (IOError, IndexError):
            self.print_error(StorageAction.LOADING)
            print('Fallback: Returning None result')
            return None

    def save(self, public_key: str, private_key: str) -> bool:
        """ Saves the public and private key to the storage file """
        try:
            with open(self.path, mode="w") as file:
                file.write(public_key)
                file.write('\n')
                file.write(private_key)
                self.print_success(StorageAction.SAVING)
                return True

        except (IOError, IndexError):
            self.print_error(StorageAction.SAVING)
            return False
