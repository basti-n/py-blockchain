from core.models.storage import StorageAction
from core.blockchainConstants import Block
from core.models.transaction import Transaction
from typing import Any, List


def print_blocks(chain: List[Block], *, verbose=False) -> None:
    if verbose:
        for block in chain:
            print('Print Block')
            print(block)
        else:
            print(' - ' * 20)

    print(f'Chain: {[str(block) for block in chain]}')
    print(' - ' * 20)


def print_participants(participants: set) -> None:
    print(20 * ' - ')
    print('Participants: ', participants)
    print(20 * ' - ')


def warn_no_wallet(action: StorageAction) -> None:
    print('\n----  E R R O R  ---- ')
    print('Error when {}: Blockchain has no wallet or owner.'.format(action))
    print('----  E R R O R  ---- \n')


def warn_no_key(action: StorageAction) -> None:
    print('\n----  W A R N I N G ---- ')
    print('Error when {} keys: No keys are available'.format(action))
    print('---- W A R N I N G ---- \n')


def warn_invalid_tx(tx: Transaction) -> None:
    print('\n----  W A R N I N G ---- ')
    print('Error when validating {}.'.format(tx))
    print('---- W A R N I N G ---- \n')


def debug_log(content: Any, *, messageType='W A R N I N G') -> None:
    print(f'\n----  {messageType} ---- ')
    print(content)
    print(f'---- {messageType} ---- \n')
