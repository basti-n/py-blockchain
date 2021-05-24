from typing import Dict, List, Union
from core.models.transaction import Transaction
from core.blockchainConstants import Block
from flask.json import jsonify
from server.models.statusCodes import HttpStatusCodes


def jsonify_chain(chain: List[Block]):
    """ Returns the chain as jsonfied Response """
    return jsonify(stringify_blocks(chain))


# TODO: Fix return type of stringify functions
def stringify_blocks(chain: List[Block]) -> str:
    """ Returns the chain as JSON """
    return [stringify_block(block) for block in chain]


def stringify_block(block: Block) -> str:
    """ Returns the block as JSON """
    base_block = block.__dict__.copy()
    base_block['transactions'] = [stringify_transaction(tx)
                                  for tx in base_block['transactions']]
    return base_block


def stringify_transaction(tx: Transaction) -> str:
    """ Returns the transaction as JSON """
    return tx.__dict__.copy()


def get_message(type: HttpStatusCodes, is_success: bool, subject: str, *, additional_info: Union[str, None] = None) -> str:
    verb = get_verb_for_message(type)
    result = 'succeeded' if is_success else 'failed'
    additional_info = f' ({additional_info})' if additional_info and len(
        additional_info) else ''
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


def get_missing_fields(body: Dict, required_fields: List[str]) -> List[str]:
    """ Returns the list of required field not contained in request body """
    if len(body.keys()) < 1:
        return []
    return list(filter(lambda f: body.get(f) == None, required_fields))


def has_all_required_fields(body: Dict, required_fields: List[str]) -> bool:
    """ Returns a boolean indicating whether all required fields are set """
    return all(field in body for field in required_fields)
