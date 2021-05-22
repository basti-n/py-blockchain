from core.blockchainConstants import Block
from typing import List, Union
from flask.json import jsonify
from server.models.statusCodes import HttpStatusCodes


def jsonify_chain(chain: List[Block]):
    """ Returns the chain as jsonfied Response """
    return jsonify(stringify_blocks(chain))


def stringify_blocks(chain: List[Block]) -> str:
    """ Returns the chain as JSON """
    stringified_blocks = [block.__dict__.copy() for block in chain]
    for block in stringified_blocks:
        block['transactions'] = [tx.__dict__ for tx in block['transactions']]
    return stringified_blocks


def get_message(type: HttpStatusCodes, is_success: bool, subject: str, *, additional_info: Union[str, None] = None) -> str:
    verb = get_verb_for_message(type)
    result = 'succeeded' if is_success else 'failed'
    additional_info = f' ({additional_info})' if additional_info and len(additional_info) else ''
    return f'[{type}] {verb} {subject} {result}{additional_info}'


def get_verb_for_message(type: HttpStatusCodes) -> str:
    if type == HttpStatusCodes.PUT:
        return 'updating'
    if type == HttpStatusCodes.POST:
        return 'creating'
    if type == HttpStatusCodes.GET:
        return 'getting'

    print('Warning: Unknown status code ({}) received!'.format(type))
    return 'unknown operation'
