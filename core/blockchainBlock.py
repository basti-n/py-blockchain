from core.blockchainConstants import Block
from core.blc import Blockchain


def is_next_block(blockchain: Blockchain, block: Block) -> bool:
    """ Checks whether the block is the next block in the chain """
    return block.index == get_latest_block_index(blockchain) + 1


def is_future_block(blockchain: Blockchain, block: Block) -> bool:
    """ Checks whether the block is larger than the next expected block in the chain """
    return block.index > get_latest_block_index(blockchain) + 1


def is_previous_block(blockchain: Blockchain, block: Block) -> bool:
    """ Checks whether the block is larger than the next expected block in the chain """
    return block.index < get_latest_block_index(blockchain) + 1


def get_latest_block_index(blockchain: Blockchain) -> int:
    """ Returns the index of the latest block in blockchain """
    if blockchain.latest_block != None:
        return blockchain.latest_block.index

    return 0
