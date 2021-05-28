from core.models.storage import Storage, StorageAction
import json
import core.blockchainConstants as blockchainConstants
import core.blockchainTx as blockchainTx
import utils.blockchainHelpers as blockchainHelpers
from typing import Set, Tuple, List

STORAGE_FILE = 'storage.txt'


class FileStorage(Storage):

    def __init__(self, path=STORAGE_FILE) -> None:
        super().__init__(path)

    def load(self) -> Tuple[List[blockchainConstants.Block], List[blockchainTx.Transaction], Set[str]]:
        """ Loads and returns the blockchain, open transactions and peer nodes from stored file """
        fallback: Tuple[List[blockchainConstants.Block],
                        List[blockchainTx.Transaction], Set[str]] = ([], [], set())

        try:
            with open(self.path, mode='r') as file:
                deserialized_file = [json.loads(file)
                                     for file in file.readlines()]

                if(len(deserialized_file) < 1):
                    return fallback

                blocks = [blockchainHelpers.block_from_deserialized_block(
                    block) for block in deserialized_file[0]]
                transactions = [blockchainHelpers.trx_from_deserialized_trx(
                    trx) for trx in deserialized_file[1]]
                peer_nodes = set(deserialized_file[2])

                print('===' * 30)
                print(transactions)
                print(peer_nodes)
                print('===' * 30)

                self.print_success(StorageAction.LOADING)
                return (blocks, transactions, peer_nodes)

        except (IOError, IndexError):
            self.print_error(StorageAction.LOADING)
            print('Fallback: Returning empty Block and Transactions')
            return fallback

    def save(self, blockchain: List[blockchainConstants.Block], open_tx: List[blockchainTx.Transaction], peer_nodes: Set[str]) -> bool:
        """ Saves the blockchain, open transactions and peer nodes to stored file """
        try:
            with open(self.path, mode='w') as file:
                file.write(blockchainHelpers.stringify_block(blockchain))
                self.add_line_break(file)
                file.write(blockchainHelpers.stringify_block(open_tx))
                self.add_line_break(file)
                file.write(blockchainHelpers.stringify_block(list(peer_nodes)))

                self.print_success(StorageAction.SAVING)
                return True

        except IOError:
            self.print_error(StorageAction.SAVING)
            return False
