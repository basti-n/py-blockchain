from abc import ABC, abstractstaticmethod
from blockchainHelpers import get_tx_without_reward_tx
from blockchainConstants import Block
from blockchainHasher import createHashedBlock, valid_proof


class Verifier(ABC):
    @abstractstaticmethod
    def isVerified(args: any) -> bool:
        pass


class BlockchainVerifier(Verifier):
    @staticmethod
    def is_verified(chain: list[Block]) -> bool:
        """ Verifies the provided chain (True or False) """
        for (block_index, block) in enumerate(chain):

            if block_index <= 0:
                continue

            if block.previous_hash != createHashedBlock(chain[block_index - 1]):
                print(
                    f'Detected invalid chain at index {block_index}', chain[block_index])
                return False

            if not valid_proof(get_tx_without_reward_tx(block.transactions), block.previous_hash, block.proof):
                print(
                    f'Detected invalid proof at {block.transactions}. Expected proof: {block.proof}')
                return False

        return True
