import json
from core.storage import Storage, StorageAction
import core.blockchainConstants as blockchainConstants
import core.blockchainTx as blockchainTx
import utils.blockchainHelpers as blockchainHelpers
from typing import Tuple, List

STORAGE_FILE = 'storage.txt'


class FileStorage(Storage):

    def __init__(self, path=STORAGE_FILE) -> None:
        super().__init__(path)

    def load(self) -> Tuple[List[blockchainConstants.Block], List[blockchainTx.Transaction]]:
        """ Loads and returns the blockchain and open transactions from stored file """
        fallback: Tuple[List[blockchainConstants.Block],
                        List[blockchainTx.Transaction]] = ([], [])

        try:
            with open(self.path, mode='r') as file:
                deserialized_file = [json.loads(file)
                                     for file in file.readlines()]

                if(len(deserialized_file) < 1):
                    return fallback

                blocks = [blockchainHelpers.block_from_deserialized_block(
                    block) for block in deserialized_file[0][:-1]]
                transactions = [blockchainHelpers.trx_from_deserialized_trx(
                    trx) for trx in deserialized_file[1]]

                print('===' * 30)
                print(transactions)
                print('===' * 30)

                return (blocks, transactions)

        except (IOError, IndexError):
            self.print_error_saving(StorageAction.LOADING)
            print('Fallback: Returning empty Block and Transactions')
            return fallback

    def save(self, blockchain: List[blockchainConstants.Block], open_tx: List[blockchainTx.Transaction]) -> bool:
        """ Saves the blockchain and open transactions from stored file """
        try:
            with open(self.path, mode='w') as file:
                file.write(blockchainHelpers.stringify_block(blockchain))
                file.write('\n')
                file.write(blockchainHelpers.stringify_block(open_tx))
                return True

        except IOError:
            self.print_error_saving(StorageAction.SAVING)
            return False
