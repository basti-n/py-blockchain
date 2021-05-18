from core.blockchainStorage import FileStorage
from core.blockchainWallet import Wallet
from core.models.storage import Storage
from typing import Union


class BlockchainFactory:
    def get_wallet(self) -> Union[Wallet, None]:
        return None

    def get_owner(self) -> Union[str, None]:
        return None

    def get_storage(self, path: Union[str, None] = None) -> Union[Storage, None]:
        return None


class BlockchainFileStorageFactory(BlockchainFactory):
    def get_storage(self, path: Union[str, None] = None) -> Union[Storage, None]:
        if path != None:
            return FileStorage(path)
        return FileStorage()
