from utils.binaryConverters import BinaryConverter
from core.blockchainConstants import MINING_ROOT_SENDER
from core.models.transaction import Transaction
from core.models.verifier import Verifier
from core.blockchainWallet import Wallet


class TransactionVerifier(Verifier):
    @staticmethod
    def is_verified(transaction: Transaction) -> bool:
        if Transaction.is_root_sender(transaction.sender):
            return True

        verifier = Wallet.sign_transaction(transaction.sender)
        hashed_tx = Wallet.hash_transaction(
            transaction.sender, transaction.recipient, transaction.amount)

        return verifier.verify(hashed_tx, Wallet.to_binary(transaction.signature))
