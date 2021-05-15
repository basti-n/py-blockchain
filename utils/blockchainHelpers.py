from json.encoder import JSONEncoder
from typing import Union
from core.blockchainConstants import Block, initial_block_value
from core.models.transaction import Transaction
from typing import List
import functools


class BlockEncoder(JSONEncoder):
    def default(_, o):
        return o.__dict__


def block_from_deserialized_block(deserializedBlock: Block.__dict__) -> Block:
    """ Deserializes the JSON to the Block instance """
    deserializedBlock['transactions'] = [trx_from_deserialized_trx(
        trx) for trx in deserializedBlock['transactions']]
    return Block(**deserializedBlock)


def trx_from_deserialized_trx(deserializedTrx: Transaction.__dict__) -> Transaction:
    """ Deserializes the JSON to the Transaction instance """
    return Transaction(**deserializedTrx)


def get_last_block(chain: List[Block]) -> Block:
    """  Returns the last block for the provided chain """
    return chain[-1]


def get_tx_without_reward_tx(transactions: List[Transaction]) -> List[Transaction]:
    """ Returns all transacitons except the last (reward transaction) """
    return transactions[:-1]


def getLatestValueFromPreviousValue(prevValue: Union[None, list]) -> list:
    """ Returns the latest blockchain value from the previous value (list or None) """
    return initial_block_value if prevValue == None else prevValue


def manipulate_chain(chain: list) -> list:
    if len(chain):
        chain[0] = Block('fakeRandomHash', 0, transactions=[])
    return chain


def serialize_block(block: Block) -> bytes:
    """ Returns the block as JSON  """
    return BlockEncoder(sort_keys=True).encode(block).encode()


def stringify_block(block: Block) -> str:
    """ Returns a stringified Block """
    return serialize_block(block).decode()


def get_last_blockchain_value(blockchain: List[Block]) -> Union[None, list]:
    """ Returns the latest value of the blockchain (default [1]) """
    if len(blockchain):
        return blockchain[-1]
    return None


def get_balance(participant: str, chain: list, open_transactions: List[Transaction] = []) -> float:
    tx_amounts_received = [[tx.amount for tx in block.transactions if tx.recipient ==
                            participant] for block in chain]

    tx_amounts_sent = [[tx.amount for tx in block.transactions if tx.sender ==
                        participant] for block in chain]

    if len(open_transactions):
        tx_amounts_sent.append([
            tx.amount for tx in open_transactions if tx.sender == participant])
        tx_amounts_received.append([
            tx.amount for tx in open_transactions if tx.recipient == participant])

    amount_received = calculate_balance(tx_amounts_received)
    amount_sent = calculate_balance(tx_amounts_sent)

    return amount_received - amount_sent


def calculate_balance(amounts: List[tuple]) -> float:
    """ Calculates the sum for the provided amounts """
    return functools.reduce(lambda acc, curr: acc +
                            (sum(curr) if len(curr) else 0), amounts, 0)


def get_participants_from_transactions(transactions: List[Transaction]) -> List[str]:
    return list(set([tx.sender for tx in transactions] +
                    [tx.recipient for tx in transactions]))
