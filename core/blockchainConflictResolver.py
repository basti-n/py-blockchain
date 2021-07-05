from core.models.transaction import Transaction
from core.blockchainTx import clear_transactions
from core.blockchainVerifier import BlockchainVerifier
from core.blockchainConstants import Block
from typing import List, Union
from utils.blockchainHelpers import block_from_deserialized_block
from core.models.resolver import Resolver
from server.models.endpoints import BlockchainEndpoints
from core.models.baseBlockchain import BaseBlockchain
import requests


class ConflictResolver(Resolver):
    def __init__(self, blockchain: BaseBlockchain, path=BlockchainEndpoints.CHAIN) -> None:
        super().__init__()
        self.blockchain = blockchain
        self.peer_nodes = blockchain.peer_nodes
        self.path = path

    @ property
    def open_transactions(self) -> List[Transaction]:
        return self.blockchain.open_transactions

    @ property
    def chain(self) -> List[Transaction]:
        return self.blockchain.blockchain

    def resolve(self) -> bool:
        """ Resolves conflicts on the blockchain """
        winner_chain = self.chain
        chain_replaced = False

        for node in self.peer_nodes:
            try:
                response: Union(List[Block.__dict__], None) = requests.get(
                    self.get_url(node)).json()
                if response:
                    chain: List[Block] = [block_from_deserialized_block(
                        block) for block in response]
                    if self.replace_chain(chain):
                        winner_chain = chain
                        chain_replaced = True

            except requests.exceptions.ConnectionError:
                continue

        self.update_blockchain(winner_chain)
        if chain_replaced:
            self.reset_open_tx()

        return chain_replaced

    def get_url(self, node: str) -> str:
        return f'http://{node}{self.path}'

    def replace_chain(self, chain: List[Block]) -> bool:
        """ Returns whether the chain needs to be replaced """
        return len(chain) > len(self.chain) and BlockchainVerifier.is_verified(chain)

    def reset_open_tx(self) -> None:
        clear_transactions(self.open_transactions)

    def update_blockchain(self, newChain: List[Block]) -> None:
        self.blockchain.blockchain = newChain
