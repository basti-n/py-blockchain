import blockchainConstants


def createHashedBlock(block: blockchainConstants.Block, separator: str = '-') -> str:
    """ Creates a hashed block (string) """
    hashed_block = separator.join([str(value) for _, value in block])

    return hashed_block
