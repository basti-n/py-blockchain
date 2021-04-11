import blockchainConstants
import blockchainTx
import blockchainHelpers
import json

STORAGE_FILE = 'storage.txt'


def load() -> tuple[list[blockchainConstants.Block], list[blockchainTx.Transaction]]:
    """ Loads and returns the blockchain and open transactions from stored file """
    with open(STORAGE_FILE, mode='r') as file:
        deserialized_file = [json.loads(file) for file in file.readlines()]

        if(len(deserialized_file) < 1):
            return ([], [])

        blocks = [blockchainHelpers.block_from_deserialized_block(
            block) for block in deserialized_file[0][:-1]]
        transactions = [blockchainHelpers.trx_from_deserialized_trx(
            trx) for trx in deserialized_file[1]]

        print('===' * 30)
        print(transactions)
        print('===' * 30)

        return (blocks, transactions)


def save(blockchain: list[blockchainConstants.Block], open_tx: list[blockchainTx.Transaction]) -> None:
    """ Saves the blockchain and open transactions from stored file """
    with open(STORAGE_FILE, mode='w') as file:
        file.write(blockchainHelpers.stringify_block(blockchain))
        file.write('\n')
        file.write(blockchainHelpers.stringify_block(open_tx))
