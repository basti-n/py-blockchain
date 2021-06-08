from utils.blockchainHelpers import get_last_block, get_tx_without_reward_tx
from core.blockchainHasher import createHashedBlock, proof_of_work, valid_proof
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


def get_added_block(chain: List[Block], block: Block) -> Tuple[List[Block], Union[Block, None]]:
    """ Appends block to chain and returns chain and appended block"""

    try:
        is_valid = valid_proof(
            get_tx_without_reward_tx(block.transactions), block.previous_hash, block.proof)
        hashes_match = createHashedBlock(
            get_last_block(chain)) == block.previous_hash

        if is_valid and hashes_match:
            chain.append(block)
            return (chain, block)

        print('Invalid Block! ...returning unchanged values.')
        return (chain, get_last_block(chain))

    except Exception as error:
        print('Warning! Error adding block! ({})'.format(error))
        return (chain, None)
