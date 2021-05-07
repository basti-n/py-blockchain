from typing import Type
from core.blockchainMiner import get_mined_block
from core.blockchainConstants import GenesisBlock
from core.blockchainStorage import Storage
from core.blockchainTx import append_transaction


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

    @property
    def open_transactions_size(self):
        return len(self.__open_transactions)

    def mine(self) -> None:
        self.__blockchain, self.__open_transactions = get_mined_block(
            self.__blockchain, self.__open_transactions, self.owner)
        self.__save()

    def add_transaction(self, sender: str, recipient: str, value=1.0, participants: set = set()) -> bool:
        """ Adds new transactions to open transactions and save it to storage  """
        initial_tx_size = self.open_transactions_size
        self.__open_transactions = append_transaction(
            sender, recipient, value, chain=self.__blockchain, open_tx=self.__open_transactions, participants=participants)
        self.__save()
        return self.open_transactions_size > initial_tx_size

    def __initialize(self) -> None:
        """ Initializes the blockchain and open transactions by using the provided storage """
        self.__blockchain, self.__open_transactions = self.storage.load()
        if(len(self.blockchain) < 1):
            self.blockchain = [GenesisBlock()]

    def __save(self) -> None:
        self.storage.save(self.__blockchain, self.__open_transactions)
