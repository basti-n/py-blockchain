from core.blockchainConstants import Block
from typing import List
from flask.json import jsonify


def jsonify_chain(chain: List[Block]):
    """ Returns the chain as jsonfied Response """
    return jsonify(stringify_blocks(chain))


def stringify_blocks(chain: List[Block]) -> str:
    """ Returns the chain as JSON """
    stringified_blocks = [block.__dict__.copy() for block in chain]
    for block in stringified_blocks:
        block['transactions'] = [tx.__dict__ for tx in block['transactions']]
    return stringified_blocks
