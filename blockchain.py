from core.blc import Blockchain
from ui.blockchainGui import GUI
from core.blockchainStorage import FileStorage
from core.blockchainVerifier import BlockchainVerifier

# Globals
open_transactions = []
owner = 'fips'
participants = set()
blockchain = Blockchain(FileStorage, owner)

gui = GUI(blockchain=blockchain, participants=participants,
          verifier=BlockchainVerifier)
gui.start()

print('Done!')
