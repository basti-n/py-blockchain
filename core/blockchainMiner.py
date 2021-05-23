from core.blockchainHasher import createHashedBlock, proof_of_work
from core.blockchainTx import add_reward_transaction, clear_transactions
from core.blockchainConstants import Block
from core.transactionVerifier import TransactionVerifier
from core.models.transaction import Transaction
from utils.blockchainLogger import warn_invalid_tx
from typing import Tuple, List, Union


def get_mined_block(chain: List[Block], open_tx: List[Transaction], owner: str) -> Tuple[List[Block], List[Transaction], Union[Block, None]]:
    """ Appends created block to chain and returns chain, open transactions and created block"""
    last_block = chain[-1]

    for tx in open_tx:
        if not TransactionVerifier.is_verified(tx):
            warn_invalid_tx(tx)
            return (chain, open_tx, None)

    hashed_block = createHashedBlock(last_block)
    proof = proof_of_work(chain, open_tx)

    add_reward_transaction(owner, open_tx)

    index = len(chain)
    block = Block(hashed_block, index, open_tx.copy(), proof)

    chain.append(block)
    clear_transactions(open_tx)
    return (chain, open_tx, block)
