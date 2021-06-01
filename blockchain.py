from core.blc import Blockchain
from ui.blockchainGui import GUI
from core.blockchainVerifier import BlockchainVerifier
from core.blockchainFactory import BlockchainFileStorageFactory

# Globals
open_transactions = []
participants = set()

if __name__ == '__main__':
    blockchain = Blockchain(BlockchainFileStorageFactory)
    gui = GUI(blockchain=blockchain, participants=participants,
              verifier=BlockchainVerifier)
    gui.start()

    print('Done!')
