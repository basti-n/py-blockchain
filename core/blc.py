from typing import Type
from core.blockchainMiner import get_mined_block
from core.blockchainConstants import GenesisBlock
from core.blockchainStorage import Storage


class Blockchain:
    def __init__(self, storage: Type[Storage], owner: str) -> None:
        self.storage = storage()
        self.owner = owner
        self.__initialize()
        pass

    @property
    def blockchain(self):
        return self.__blockchain

    @property
    def open_transactions(self):
        return self.__open_transactions

    def mine(self) -> None:
        self.__blockchain, self.__open_transactions = get_mined_block(
            self.__blockchain, self.__open_transactions, self.owner)
        self.storage.save(self.__blockchain, self.__open_transactions)

    def __initialize(self) -> None:
        """ Initializes the blockchain and open transactions by using the provided storage """
        self.__blockchain, self.__open_transactions = self.storage.load()
        if(len(self.blockchain) < 1):
            self.blockchain = [GenesisBlock()]
