from blockchainMiner import get_mined_block
from typing import Type
from blockchainConstants import GenesisBlock
from blockchainStorage import Storage


class Blockchain:
    def __init__(self, storage: Type[Storage], owner: str) -> None:
        self.storage = storage()
        self.owner = owner
        self.__initialize()
        pass

    def mine(self) -> None:
        self.blockchain, self.open_transactions = get_mined_block(
            self.blockchain, self.open_transactions, self.owner)
        self.storage.save(self.blockchain, self.open_transactions)

    def __initialize(self) -> None:
        """ Initializes the blockchain and open transactions by using the provided storage """
        self.blockchain, self.open_transactions = self.storage.load()
        if(len(self.blockchain) < 1):
            self.blockchain = [GenesisBlock()]
