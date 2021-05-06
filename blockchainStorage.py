from utils.metaclasses.singletonMeta import SingletonMeta
import blockchainConstants
import blockchainTx
import blockchainHelpers
import json
from abc import abstractmethod

STORAGE_FILE = 'storage.txt'


class Storage(metaclass=SingletonMeta):
    @abstractmethod
    def load() -> tuple[list[blockchainConstants.Block], list[blockchainTx.Transaction]]:
        pass

    @abstractmethod
    def save() -> None:
        pass


class FileStorage(Storage):

    def __init__(self, path=STORAGE_FILE):
        self.path = path

    def load(self) -> tuple[list[blockchainConstants.Block], list[blockchainTx.Transaction]]:
        """ Loads and returns the blockchain and open transactions from stored file """
        fallback: tuple[list[blockchainConstants.Block],
                        list[blockchainTx.Transaction]] = ([], [])

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
            print(f'Alert: Error reading file {self.path}')
            print('Fallback: Returning empty Block and Transactions')
            return fallback

    def save(self, blockchain: list[blockchainConstants.Block], open_tx: list[blockchainTx.Transaction]) -> None:
        """ Saves the blockchain and open transactions from stored file """
        try:
            with open(self.path, mode='w') as file:
                file.write(blockchainHelpers.stringify_block(blockchain))
                file.write('\n')
                file.write(blockchainHelpers.stringify_block(open_tx))
        except IOError:
            print(f'Alert: Saving {self.path} failed!')
