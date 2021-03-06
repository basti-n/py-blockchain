from server.models.httpMethods import HttpMethods
from typing import Any, Dict, List, Set, Union
from core.models.transaction import Transaction
from core.blockchainConstants import Block
from flask.json import jsonify


def jsonify_chain(chain: List[Block]):
    """ Returns the chain as jsonfied Response """
    return jsonify(get_serializable_blocks(chain))


def get_serializable_blocks(chain: List[Block]) -> List[Dict[str, Any]]:
    """ Returns the chain as JSON serializable dictionary """
    return [get_serializable_block(block) for block in chain]


def get_serializable_block(block: Block) -> Dict[str, Any]:
    """ Returns the block as JSON serializabledictionary """
    base_block = block.__dict__.copy()
    base_block['transactions'] = get_serializable_transaction(
        base_block['transactions'])

    return base_block


def get_serializable_transaction(tx: Union[Transaction, List[Transaction]]) -> Dict[str, Any]:
    """ Returns the transaction as JSON serializable dictionary """
    if type(tx) is list:
        return [get_serializable_transaction(transaction) for transaction in tx]
    return tx.__dict__.copy()


def get_serializable_peer_nodes(nodes: Set[str]) -> List[str]:
    """ Returns the nodes as a JSON serializable list """
    return list(nodes)


def get_message(type: HttpMethods, is_success: bool, subject: str, *, additional_info: Union[str, None] = None) -> str:
    verb = get_verb_for_message(type)
    result = 'succeeded' if is_success else 'failed'
    additional_info = f' ({additional_info})' if additional_info and len(
        additional_info) else ''
    return f'[{type}] {verb} {subject} {result}{additional_info}'


def get_verb_for_message(type: HttpMethods) -> str:
    if type == HttpMethods.PUT:
        return 'updating'
    if type == HttpMethods.POST:
        return 'creating'
    if type == HttpMethods.GET:
        return 'getting'
    if type == HttpMethods.DELETE:
        return 'deleting'

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
