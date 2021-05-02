from blockchainStorage import load
from typing import Union
import blockchainLogger
import blockchainConstants
import blockchainTx
import blockchainHelpers
import blockchainMiner
from blockchainVerifier import BlockchainVerifier
import blockchainOutput
import blockchainStorage

# Globals
open_transactions = []
owner = 'fips'
participants = set()

blockchain, open_transactions = blockchainStorage.load()
if(len(blockchain) < 1):
    blockchain = [blockchainConstants.GenesisBlock()]


def get_last_blockchain_value() -> Union[None, list]:
    """ Returns the latest value of the blockchain (default [1])
    """
    if len(blockchain):
        return blockchain[-1]
    return None


def request_tx_data() -> bool:
    """ Adds transaction amount and recipient to open transactions """
    tx_amount, tx_recipient = blockchainTx.ask_for_tx()
    return blockchainTx.add_transaction(
        owner, tx_recipient, tx_amount, chain=blockchain, open_tx=open_transactions, participants=participants)


def get_user_choice(
        firstOption: str = 'Add transaction',
        secondOption: str = 'Mine Blocks',
        thirdOption: str = 'Print Participants',
        fourthOption: str = 'Print Blocks',
        fifthOption: str = 'Verify open transactions',
        offerQuit: bool = True,
        offerManipulate: bool = True) -> int:
    """ Returns the user choise as an integer """
    print('Please enter your desired command.')
    print(f'Option 1: {firstOption}')
    print(f'Option 2: {secondOption}')
    print(f'Option 3: {thirdOption}')
    print(f'Option 4: {fourthOption}')
    print(f'Option 5: {fifthOption}')

    if offerQuit == True:
        print(f'Quit: Press "q" for quitting')
    if offerManipulate == True:
        print(f'Manipulate: Press "m" for manipulating')

    reply = input('Enter your command? ')
    if reply.lower() == 'm':
        return -1
    return 0 if reply.lower() == 'q' else int(reply)


waiting_for_input = True
while waiting_for_input:
    command = get_user_choice()

    if command == -1:
        blockchainHelpers.manipulate_chain(blockchain)

    elif command == 1:
        transaction_verified = request_tx_data()
        blockchainOutput.printDependingOn(
            transaction_verified, 'Transaction verified.', 'Transaction rejected.')

    elif command == 2:
        blockchainMiner.mine_block(blockchain, open_transactions, owner)

    elif command == 3:
        blockchainLogger.print_participants(participants)

    elif command == 4:
        blockchainLogger.print_blocks(blockchain)

    elif command == 5:
        transactions_verified = blockchainTx.verify_transactions(
            blockchain, open_transactions)
        blockchainOutput.printDependingOn(
            transactions_verified, 'All transactions are valid', 'Invalid transaction found!')

    elif command == 0:
        print('Exiting Program.')
        break

    is_valid = BlockchainVerifier.is_verified(blockchain)
    if not is_valid:
        print('Invalid blockchain... exiting!')
        waiting_for_input = False

    print('Balance: ', blockchainTx.get_balance(owner, blockchain))

print('Done!')
