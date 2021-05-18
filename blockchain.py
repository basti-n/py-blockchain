from core.blc import Blockchain
from ui.blockchainGui import GUI
from core.blockchainVerifier import BlockchainVerifier
from core.blockchainFactory import BlockchainFileStorageFactory

# Globals
open_transactions = []
participants = set()
blockchain = Blockchain(BlockchainFileStorageFactory)

if __name__ == '__main__':
    gui = GUI(blockchain=blockchain, participants=participants,
              verifier=BlockchainVerifier)
    gui.start()

    print('Done!')
