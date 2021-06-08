from typing import List, Tuple, Type
from core.models.storage import Storage
from utils.blockchainHelpers import get_balance, get_last_block
from utils.blockchainLogger import warn_no_wallet
from core.blockchainMiner import get_added_block, get_mined_block
from core.blockchainConstants import Block, GenesisBlock
from core.blockchainTx import append_transaction, get_latest_transaction
from core.blockchainWallet import Wallet
from core.blockchainFactory import BlockchainFactory


class Blockchain:
    def __init__(self, factory: Type[BlockchainFactory], node_id: str = '__internal__') -> None:
        factory_instance = factory()
        self.node_id = node_id
        self.storage = factory_instance.get_storage(
            Storage.generate_path(prefix='storage', id=self.node_id))
        self.wallet = factory_instance.get_wallet()
        self.owner = factory_instance.get_owner()
        self.peer_nodes = factory_instance.get_peer_nodes()
        self.__initialize()
        pass

    @property
    def blockchain(self):
        return self.__blockchain

    @property
    def latest_block(self):
        return self.__latest_block

    @property
    def latest_transaction(self):
        return get_latest_transaction(self.__open_transactions)

    @property
    def balance(self):
        return get_balance(self.owner, self.blockchain, self.open_transactions)

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
            self.__blockchain, self.__open_transactions, self.__latest_block = get_mined_block(
                self.__blockchain, self.__open_transactions, self.owner)
            return self.__save()
        else:
            warn_no_wallet('mining')
            return False

    def add_block(self, block: Block) -> bool:
        if self.has_wallet:
            self.__blockchain, self.__latest_block = get_added_block(
                self.blockchain, block)
            return self.__save()
        else:
            warn_no_wallet('adding block')
            return False

    def add_transaction(self, sender: str, recipient: str, amount=1.0, participants: set = set(), signature: str = None, *, is_broadcast_tx=False) -> bool:
        """ Adds new transactions to open transactions and save it to storage  """
        if self.has_wallet:
            signature = self.wallet.create_signature(
                sender, recipient, amount) if signature is None else signature
            initial_tx_size = self.open_transactions_size
            self.__open_transactions = append_transaction(
                sender, recipient, amount, chain=self.__blockchain, signature=signature, open_tx=self.__open_transactions, participants=participants, skip_verification=is_broadcast_tx)
            self.__save()
            return self.open_transactions_size > initial_tx_size
        else:
            warn_no_wallet('adding transaction')
            return False

    def create_wallet(self) -> Tuple[str, str]:
        """ Sets private key and owner (public key) """
        if self.wallet == None:
            self.wallet = Wallet(node_id=self.node_id)

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
            self.wallet = Wallet(node_id=self.node_id)

        if self.wallet.load_keys():
            self.owner = self.wallet.public_key
        else:
            self.__reset_owner()

    def add_peer_node(self, node: str) -> bool:
        """ Adds a peer node.

        Arguments:
            :node: The url of the node to add.
        """
        self.peer_nodes.add(node)
        return self.__save()

    def remove_peer_node(self, node: str) -> bool:
        """ Deletes a peer node.

        Arguments:
            :node: The url of the node to remove.
        """
        self.peer_nodes.discard(node)
        return self.__save()

    def __initialize(self) -> None:
        """ Initializes the blockchain, open transactions and peer nodes by using the provided storage """
        self.__blockchain, self.__open_transactions, self.peer_nodes = self.storage.load()
        if len(self.blockchain) < 1:
            self.blockchain = [GenesisBlock()]

        self.__latest_block = get_last_block(
            self.blockchain)

    def __save(self) -> bool:
        return self.storage.save(self.__blockchain, self.__open_transactions, self.peer_nodes)

    def __reset_owner(self) -> None:
        self.owner = None
