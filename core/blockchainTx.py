import core.blockchainConstants as blockchainConstants
from core.models.transaction import Transaction
from core.transactionVerifier import TransactionVerifier
from utils.blockchainErrorHandler import ErrorHandler
from utils.blockchainLogger import warn_invalid_tx
from typing import Union, List, Tuple
import functools


def verify_transaction(tx: Transaction, chain: list, open_transactions: List[Transaction]) -> bool:
    """ Checks whether sufficient funds for the transaction are present """
    if(Transaction.is_root_sender(tx.sender)):
        return True

    balance_sender = get_balance(tx.sender, chain, open_transactions)
    return balance_sender >= tx.amount


def verify_transactions(chain: list, open_transactions: List[Transaction]) -> bool:
    """ Checks all transactions for valid funds """
    balances = [get_balance(participant, chain, open_transactions)
                for participant in get_participants_from_transactions(open_transactions)]

    return all([balance > 0 for balance in balances])


def append_transaction(sender: str, recipient: str, value=1.0, *, signature: str = '', chain: list = [], open_tx=[], participants: set = set()) -> List[Transaction]:
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
    is_verified = TransactionVerifier.is_verified(tx)

    if is_verified and verify_transaction(tx, chain, open_tx):
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

    append_transaction(sender, owner, reward, open_tx=open_tx)


def ask_for_tx() -> Tuple[float, str]:
    tx_amount: Union[float, None] = None
    while type(tx_amount) is not float:
        try:
            tx_amount = float(input('Your transaction amount: '))
        except ValueError as valueError:
            ErrorHandler.logValueError(
                valueError, msgPrefix='Invalid input: ', msgPostfix='. Please provide a valid number (e.g. 12)')
    tx_recipient = input('Your transaction recipient: ')
    return tx_amount, tx_recipient


def get_tx_data(sender: str, recipient: str, signature: str, value: float = 1.0) -> Transaction:
    """ Transform sender, recipient, signature and value to Transaction Data """
    return Transaction(sender, recipient, value, signature)


def clear_transactions(open_transactions: list) -> None:
    """ Removes all open transactions """
    open_transactions.clear()


def get_balance(participant: str, chain: list, open_transactions: List[Transaction] = []) -> float:
    tx_amounts_received = [[tx.amount for tx in block.transactions if tx.recipient ==
                            participant] for block in chain]

    tx_amounts_sent = [[tx.amount for tx in block.transactions if tx.sender ==
                        participant] for block in chain]

    if len(open_transactions):
        tx_amounts_sent.append([
            tx.amount for tx in open_transactions if tx.sender == participant])
        tx_amounts_received.append([
            tx.amount for tx in open_transactions if tx.recipient == participant])

    amount_received = calculate_balance(tx_amounts_received)
    amount_sent = calculate_balance(tx_amounts_sent)

    return amount_received - amount_sent


def calculate_balance(amounts: List[tuple]) -> float:
    """ Calculates the sum for the provided amounts """
    return functools.reduce(lambda acc, curr: acc +
                            (sum(curr) if len(curr) else 0), amounts, 0)


def get_participants_from_transactions(transactions: List[Transaction]) -> List[str]:
    return list(set([tx.sender for tx in transactions] +
                    [tx.recipient for tx in transactions]))
