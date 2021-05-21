from typing import List, Tuple, Type
from utils.blockchainLogger import warn_no_wallet
from core.blockchainMiner import get_mined_block
from core.blockchainConstants import Block, GenesisBlock
from core.blockchainTx import append_transaction
from core.blockchainWallet import Wallet
from core.blockchainFactory import BlockchainFactory


class Blockchain:
    def __init__(self, factory: Type[BlockchainFactory]) -> None:
        factory_instance = factory()
        self.storage = factory_instance.get_storage()
        self.wallet = factory_instance.get_wallet()
        self.owner = factory_instance.get_owner()
        self.__initialize()
        pass

    @property
    def blockchain(self):
        return self.__blockchain

    @blockchain.setter
    def blockchain(self, blockchain: List[Block]) -> None:
        self.__blockchain = blockchain

    @property
    def open_transactions(self):
        return self.__open_transactions

    @property
    def open_transactions_size(self):
        return len(self.__open_transactions)

    @property
    def has_wallet(self):
        return self.wallet != None and self.owner != None

    def mine(self) -> bool:
        """ Mines a block and saves the blockchain and open transactions """
        if self.has_wallet:
            self.__blockchain, self.__open_transactions = get_mined_block(
                self.__blockchain, self.__open_transactions, self.owner)
            return self.__save()
        else:
            warn_no_wallet('mining')
            return False

    def add_transaction(self, sender: str, recipient: str, amount=1.0, participants: set = set()) -> bool:
        """ Adds new transactions to open transactions and save it to storage  """
        if self.has_wallet:
            signature = self.wallet.create_signature(sender, recipient, amount)
            initial_tx_size = self.open_transactions_size
            self.__open_transactions = append_transaction(
                sender, recipient, amount, chain=self.__blockchain, signature=signature, open_tx=self.__open_transactions, participants=participants)
            self.__save()
            return self.open_transactions_size > initial_tx_size
        else:
            warn_no_wallet('adding transaction')
            return False

    def create_wallet(self) -> Tuple[str, str]:
        """ Sets private key and owner (public key) """
        if self.wallet == None:
            self.wallet = Wallet()

        private_key, public_key = self.wallet.create_keys()
        self.owner = public_key
        return private_key, public_key

    def save_wallet(self) -> bool:
        if not self.has_wallet:
            print('Error: Wallet does not exist.')
            return False

        return self.wallet.save_keys()

    def load_wallet(self) -> None:
        """ Loads owner (public key) from storage """
        if self.wallet == None:
            self.wallet = Wallet()

        if self.wallet.load_keys():
            self.owner = self.wallet.public_key
        else:
            self.__reset_owner()

    def __initialize(self) -> None:
        """ Initializes the blockchain and open transactions by using the provided storage """
        self.__blockchain, self.__open_transactions = self.storage.load()
        if len(self.blockchain) < 1:
            self.blockchain = [GenesisBlock()]

    def __save(self) -> bool:
        return self.storage.save(self.__blockchain, self.__open_transactions)

    def __reset_owner(self) -> None:
        self.owner = None
