from utils.mixins.prettyPrint import PrettyPrintBlockMixin
from utils.mixins.iterMixin import IterMixin
import blockchainTx

# Constants
MINING_REWARD = 10
MINING_ROOT_SENDER = 'root_sender'
INITIAL_PROOF = 100


class Block(IterMixin, PrettyPrintBlockMixin):
    def __init__(self, previous_hash: str, index: int, transactions: list[blockchainTx.Transaction], proof: int):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.proof = proof


class GenesisBlock(Block):
    def __init__(self):
        self.previous_hash = ''
        self.index = 0
        self.transactions = []
        self.proof = INITIAL_PROOF


# Initial starting value for a block in an empty blockchain
initial_block_value = [1]
genesis_block = GenesisBlock()
