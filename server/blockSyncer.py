from server.responseHelpers import get_serializable_block
from typing import List
from core.blockchainConstants import Block
from server.models.endpoints import BlockchainEndpoints
from server.models.syncer import Syncer
import requests


class BlockSync(Syncer):
    def __init__(self, peer_nodes: List[str], path=BlockchainEndpoints.BROADCAST_BLOCK) -> None:
        super().__init__(peer_nodes, path)

    def broadcast(self, block: Block) -> bool:
        for node in self.peer_nodes:
            url = self.get_url(node)

            try:
                response = requests.post(
                    url, json={'block': get_serializable_block(block)})
                if response.status_code >= 400 and response.status_code < 600:
                    return False
            except requests.exceptions.ConnectionError:
                continue

            return True
