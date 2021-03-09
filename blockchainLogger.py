def print_blocks(chain, *, verbose=False) -> None:
    if verbose:
        for block in chain:
            print('Print Block')
            print(block)
        else:
            print(' - ' * 20)

    print(f'Chain: {chain}')
    print(' - ' * 20)


def print_participants(participants: set) -> None:
    print(20 * ' - ')
    print('Participants: ', participants)
    print(20 * ' - ')
