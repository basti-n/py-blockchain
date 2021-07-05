from core.blockchainStorage import FileStorage
from core.blockchainWallet import Wallet
from core.models.storage import Storage
from typing import Set, Union


class BlockchainFactory:
    def get_wallet(self) -> Union[Wallet, None]:
        return None

    def get_owner(self) -> Union[str, None]:
        return None

    def get_peer_nodes(self, use_default=True) -> Union[Set[str], None]:
        return set() if use_default else None

    def get_storage(self, path: Union[str, None] = None) -> Union[Storage, None]:
        return None

    def get_resolve_conflicts(self) -> bool:
        return False


class BlockchainFileStorageFactory(BlockchainFactory):
    def get_storage(self, path: Union[str, None] = None) -> Union[Storage, None]:
        if path != None:
            return FileStorage(path)
        return FileStorage()
