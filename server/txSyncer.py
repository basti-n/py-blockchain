from server.models.syncer import Syncer
from server.responseHelpers import get_serializable_transaction
from server.models.endpoints import BlockchainEndpoints
from typing import List, Tuple
from core.models.transaction import Transaction
import requests


class TransactionSync(Syncer):
    def __init__(self, peer_nodes: List[str], path=BlockchainEndpoints.BROADCAST_TRANSACTION) -> None:
        super().__init__(peer_nodes, path)

    def broadcast(self, transaction: Transaction) -> Tuple[bool, bool]:
        for node in self.peer_nodes:
            url = self.get_url(node)

            try:
                response = requests.post(
                    url, json=get_serializable_transaction(transaction))
                if response.status_code >= 400 and response.status_code < 600:
                    return (False, False)
            except requests.exceptions.ConnectionError:
                continue

            return (True, False)
