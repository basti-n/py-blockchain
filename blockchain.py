from blc import Blockchain
from blockchainGui import GUI
from blockchainStorage import FileStorage
from blockchainVerifier import BlockchainVerifier

# Globals
open_transactions = []
owner = 'fips'
participants = set()
blockchain = Blockchain(FileStorage, owner)

gui = GUI(blockchain=blockchain, participants=participants,
          verifier=BlockchainVerifier)
gui.start()

print('Done!')
