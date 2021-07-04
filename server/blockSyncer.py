from server.models.statusCodes import HttpStatusCodes
from server.responseHelpers import get_serializable_block
from typing import List, Tuple
from core.blockchainConstants import Block
from server.models.endpoints import BlockchainEndpoints
from server.models.syncer import Syncer
import requests


class BlockSync(Syncer):
    def __init__(self, peer_nodes: List[str], path=BlockchainEndpoints.BROADCAST_BLOCK) -> None:
        super().__init__(peer_nodes, path)

    def broadcast(self, block: Block) -> Tuple[bool, bool]:
        for node in self.peer_nodes:
            url = self.get_url(node)
            marked_for_conflict = False

            try:
                response = requests.post(
                    url, json={'block': get_serializable_block(block)})
                if response.status_code == HttpStatusCodes.CONFLICT:
                    marked_for_conflict = True
                if response.status_code >= HttpStatusCodes.BAD_REQUEST and response.status_code < 600:
                    return (False, marked_for_conflict)
            except requests.exceptions.ConnectionError:
                continue

            return (True, marked_for_conflict)
