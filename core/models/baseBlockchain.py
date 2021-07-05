from abc import ABC, abstractproperty
from core.blockchainConstants import Block
from core.models.transaction import Transaction
from typing import Any, List, Set, Union


class BaseBlockchain(ABC):
    def __init__(self, peer_nodes: Union[Set[str], None] = None) -> None:
        self.peer_nodes = peer_nodes

    @abstractproperty
    def blockchain(self) -> Union[List[Block], Any]:
        pass

    @abstractproperty
    def open_transactions(self) -> List[Transaction]:
        pass
