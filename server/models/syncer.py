from abc import abstractmethod
from typing import List, Tuple


class Syncer():
    def __init__(self, peer_nodes: List[str], path: str) -> None:
        self.peer_nodes = peer_nodes
        self.path = path

    @abstractmethod
    def broadcast(self) -> Tuple[bool, bool]:
        pass

    def get_url(self, node: str) -> str:
        return f'http://{node}{self.path}'
