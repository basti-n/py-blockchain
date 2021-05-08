from core.blockchainHasher import createHashedBlock, proof_of_work
from core.blockchainTx import add_reward_transaction, clear_transactions
from core.blockchainConstants import Block
from typing import Tuple, List


def get_mined_block(chain: List[Block], open_tx: list, owner: str) -> Tuple[List[Block], list]:
    """ Appends created block to chain and returns chain and open transactions """
    last_block = chain[-1]
    hashed_block = createHashedBlock(last_block)
    proof = proof_of_work(chain, open_tx)

    add_reward_transaction(owner, open_tx)

    index = len(open_tx)
    block = Block(hashed_block, index, open_tx.copy(), proof)
    chain.append(block)
    clear_transactions(open_tx)
    return (chain, open_tx)