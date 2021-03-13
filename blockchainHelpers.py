from blockchainTx import Transaction
from json.encoder import JSONEncoder
from typing import Union
from blockchainConstants import Block, initial_block_value


class BlockEncoder(JSONEncoder):
    def default(_, o):
        return o.__dict__


def get_last_block(chain: list[Block]) -> Block:
    """  Returns the last block for the provided chain """
    return chain[-1]


def get_tx_without_reward_tx(transactions: list[Transaction]) -> list[Transaction]:
    """ Returns all transacitons except the last (reward transaction) """
    return transactions[:-1]


def getLatestValueFromPreviousValue(prevValue: Union[None, list]) -> list:
    """ Returns the latest blockchain value from the previous value (list or None) """
    return initial_block_value if prevValue == None else prevValue


def manipulate_chain(chain: list) -> list:
    if len(chain):
        chain[0] = Block('fakeRandomHash', 0, transactions=[])
    return chain


def serialize_block(block: Block) -> str:
    """ Returns the block as JSON  """
    return BlockEncoder(sort_keys=True).encode(block).encode()
