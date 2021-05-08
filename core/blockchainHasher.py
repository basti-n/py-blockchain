import hashlib
import core.blockchainConstants as blockchainConstants
import utils.blockchainHelpers as blockchainHelpers
import core.blockchainTx as blockchainTx
from typing import List


def createHashedBlock(block: blockchainConstants.Block) -> str:
    """ Creates a hashed block (string) """
    hashed_block = hashlib.sha256(
        blockchainHelpers.serialize_block(block)).hexdigest()

    return hashed_block


def valid_proof(txs: List[blockchainTx.Transaction], previous_hash: str, proof: int) -> bool:
    guess = (str(txs) +
             str(previous_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[0:2] == '00'


def proof_of_work(chain: List[blockchainConstants.Block], open_tx: List[blockchainTx.Transaction]) -> int:
    """ Returns the proof of work result (integer) """
    last_block = blockchainHelpers.get_last_block(chain)
    last_hash = createHashedBlock(last_block)
    proof = 0

    while not valid_proof(open_tx, last_hash, proof):
        proof += 1

    return proof
