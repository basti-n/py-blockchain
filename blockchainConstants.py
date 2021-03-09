import blockchainTx
from utils.mixins.iterMixin import IterMixin


class Block(IterMixin):
    def __init__(self, previous_hash: str, index: int, transactions: list[blockchainTx.Transaction]):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions


class GenesisBlock(Block):
    def __init__(self):
        self.previous_hash = ''
        self.index = 0
        self.transactions = []


# Initial starting value for a block in an empty blockchain
initial_block_value = [1]
genesis_block = GenesisBlock()
MINING_REWARD = 10
MINING_ROOT_SENDER = 'root_sender'
