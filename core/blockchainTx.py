import core.blockchainConstants as blockchainConstants
from core.models.transaction import Transaction
from utils.blockchainErrorHandler import ErrorHandler
from utils.blockchainLogger import warn_invalid_tx
from core.transactionVerifier import TransactionVerifier
from typing import Union, List, Tuple


def append_transaction(sender: str, recipient: str, value=1.0, *, signature: str = '', chain: list = [], open_tx=[], participants: set = set(), skip_verification=False) -> List[Transaction]:
    """ Adds a value to the blockchain incl. the latest previous value.

    Arguments:
        :sender: The TXs sender
        :recipient: The TXs recipient
        :value: The TX amount (default 1.0)
        :signature: The TX signature (default: '')
        :chain: The blockchain
        :open_tx: List of open transactions
        :participants: Record of participants involved in blockchain
    """

    tx = get_tx_data(sender, recipient, signature, value)

    if skip_verification or (TransactionVerifier.verify_funds(tx, chain, open_tx) and TransactionVerifier.is_verified(tx)):
        open_tx.append(tx)
        participants.add(recipient)
        participants.add(sender)
        return open_tx

    warn_invalid_tx(tx)
    return open_tx


def add_reward_transaction(owner: str, open_tx=[], *, sender: str = None, reward: Union[int, float] = None) -> Transaction:
    """ Adds the mining reward transaction """
    if not sender:
        sender = blockchainConstants.MINING_ROOT_SENDER
    if not reward:
        reward = blockchainConstants.MINING_REWARD

    append_transaction(sender, owner, reward,
                       open_tx=open_tx, skip_verification=True)


def ask_for_tx() -> Tuple[float, str]:
    tx_amount: Union[float, None] = None
    while type(tx_amount) is not float:
        try:
            tx_amount = float(input('Your transaction amount: '))
        except ValueError as valueError:
            ErrorHandler.logError(
                valueError, msgPrefix='Invalid input: ', msgPostfix='. Please provide a valid number (e.g. 12)')
    tx_recipient = input('Your transaction recipient: ')
    return tx_amount, tx_recipient


def get_tx_data(sender: str, recipient: str, signature: str, value: float = 1.0) -> Transaction:
    """ Transform sender, recipient, signature and value to Transaction Data """
    return Transaction(sender, recipient, value, signature)


def clear_transactions(open_transactions: List[Transaction]) -> None:
    """ Removes all open transactions """
    open_transactions.clear()


def clear_dublicate_transactions(open_transactions: List[Transaction], reference_transactions: List[Transaction]) -> List[Transaction]:
    """ Removes dublicate transactions from the passed open transactipns """
    open_transactions_cleared = open_transactions[:]
    for open_tx in open_transactions_cleared:
        if is_dublicate_transaction(open_tx, reference_transactions):
            try:
                open_transactions_cleared.remove(open_tx)
            except ValueError:
                print('Warning! Trying to delete transaction from {} to {} (amount {}). Transaction already deleted'.format(
                    open_tx.sender, open_tx.recipient, open_tx.amount))

    return open_transactions_cleared


def get_latest_transaction(transactions: List[Transaction]) -> Union[None, Transaction]:
    """ Returns the latest transaction """
    if len(transactions) < 1:
        return None
    return transactions[-1]


def is_dublicate_transaction(transaction: Transaction, reference_transactions: List[Transaction]) -> bool:
    """ Returns whether the provided transaction is part of the reference transactions """
    return any(list(map(lambda tx: tx.amount == transaction.amount and tx.sender == transaction.sender and tx.signature == transaction.signature and tx.recipient == transaction.recipient, reference_transactions)))
