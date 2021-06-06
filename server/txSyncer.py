from server.responseHelpers import get_serializable_transaction
from server.models.endpoints import BlockchainEndpoints
import requests
from typing import Dict, List
from core.models.transaction import Transaction


class TransactionSync:
    def __init__(self, peer_nodes: List[str], path=BlockchainEndpoints.BROADCAST_TRANSACTION) -> None:
        self.peer_nodes = peer_nodes
        self.path = path

    def broadcast_transactions(self, transaction: Transaction) -> bool:
        for node in self.peer_nodes:
            url = self.__get_url(node)
            try:
                response = requests.post(
                    url, json=get_serializable_transaction(transaction))
                if response.status_code >= 400 and response.status_code < 600:
                    return False
            except requests.exceptions.ConnectionError:
                continue

            return True

    def __get_url(self, node: str) -> str:
        return f'http://{node}{self.path}'
