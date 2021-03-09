from blockchainHasher import createHashedBlock
from blockchainTx import add_reward_transaction, clear_transactions
from blockchainConstants import Block


def mine_block(chain: list[Block], open_tx: list, owner: str) -> None:
    """ Appends created block to chain """
    last_block = chain[-1]
    hashed_block = createHashedBlock(last_block)
    add_reward_transaction(owner, open_tx)

    index = len(open_tx)
    block = Block(hashed_block, index, open_tx.copy())
    chain.append(block)
    clear_transactions(open_tx)
