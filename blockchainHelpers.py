from typing import Union
from blockchainConstants import Block, initial_block_value


def getLatestValueFromPreviousValue(prevValue: Union[None, list]) -> list:
    """ Returns the latest blockchain value from the previous value (list or None) """
    return initial_block_value if prevValue == None else prevValue


def manipulate_chain(chain: list) -> list:
    if len(chain):
        chain[0] = Block('fakeRandomHash', 0, transactions=[])
    return chain
