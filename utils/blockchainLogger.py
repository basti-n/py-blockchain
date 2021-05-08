from core.blockchainConstants import Block
from typing import List


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
