from utils.blockchainHelpers import get_balance, get_participants_from_transactions
from core.models.transaction import Transaction
from core.models.verifier import Verifier
from core.blockchainWallet import Wallet
from typing import List


class TransactionVerifier(Verifier):
    @staticmethod
    def is_verified(transaction: Transaction) -> bool:
        if Transaction.is_root_sender(transaction.sender):
            return True

        verifier = Wallet.sign_transaction(transaction.sender)
        hashed_tx = Wallet.hash_transaction(
            transaction.sender, transaction.recipient, transaction.amount)

        return verifier.verify(hashed_tx, Wallet.to_binary(transaction.signature))

    @staticmethod
    def verify_funds(tx: Transaction, chain: list, open_transactions: List[Transaction]) -> bool:
        """ Checks whether sufficient funds for the transaction are present """
        if(Transaction.is_root_sender(tx.sender)):
            return True

        balance_sender = get_balance(tx.sender, chain, open_transactions)
        return balance_sender >= tx.amount

    @staticmethod
    def verify_transactions(chain: list, open_transactions: List[Transaction]) -> bool:
        """ Checks all transactions for valid funds """
        balances = [get_balance(participant, chain, open_transactions)
                    for participant in get_participants_from_transactions(open_transactions)]

        return all([balance > 0 for balance in balances])

    
