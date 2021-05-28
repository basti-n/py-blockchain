from typing import Union
from utils.blockchainErrorHandler import ErrorHandler


def ask_for_peer_nodes(phrase='Please input the peer node: ') -> Union[str, None]:
    """ Asks for user input about peer node """
    peer_node: Union[str, None] = None
    try:
        peer_node = input(phrase)
    except Exception as error:
        ErrorHandler.logError(
            error, msgPrefix='Invalid input: ', msgPostfix='. Please provide a valid string (e.g. "test-account.de"')
    return peer_node
