from blockchainHasher import createHashedBlock


def is_verified(chain: list) -> bool:
    """ Verifies the provided chain (True or False) """
    for (block_index, block) in enumerate(chain):
        if block_index <= 0:
            continue

        if block.previous_hash != createHashedBlock(chain[block_index - 1]):
            print(
                f'Detected invalid chain at index {block_index}', chain[block_index])
            return False

    return True
