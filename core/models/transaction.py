import core.blockchainConstants as blockchainConstants
from utils.mixins.orderDictMixin import OrderedDictMixin
from utils.mixins.iterMixin import IterMixin


class Transaction(IterMixin, OrderedDictMixin):
    def __init__(self, sender: str, recipient: str, amount: float, signature: str) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    @staticmethod
    def is_root_sender(sender: str) -> bool:
        return sender == blockchainConstants.MINING_ROOT_SENDER
