from blockchainGui import GUI
from blockchainStorage import load
import blockchainConstants
from blockchainVerifier import BlockchainVerifier

# Globals
open_transactions = []
owner = 'fips'
participants = set()

blockchain, open_transactions = load()
if(len(blockchain) < 1):
    blockchain = [blockchainConstants.GenesisBlock()]

gui = GUI(owner=owner, blockchain=blockchain,
          open_transactions=open_transactions, participants=participants, verifier=BlockchainVerifier)
gui.start()

print('Done!')
