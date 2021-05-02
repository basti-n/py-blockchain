from utils.metaclasses.singletonMeta import SingletonMeta
from blockchainConstants import Block
from blockchainTx import Transaction, ask_for_tx, add_transaction, verify_transactions, get_balance
from blockchainVerifier import BlockchainVerifier, Verifier
from blockchainHelpers import manipulate_chain
from blockchainOutput import printDependingOn
from blockchainMiner import mine_block
from blockchainLogger import print_blocks, print_participants


class GUI(metaclass=SingletonMeta):
    def __init__(self, *, owner: str, blockchain: list[Block], open_transactions: list[Transaction], participants: set[str], verifier: Verifier):
        self.owner = owner
        self.blockchain = blockchain
        self.open_transactions = open_transactions
        self.participants = participants
        self.verifier = verifier
        pass

    def start(self) -> None:
        waiting_for_input = True
        while waiting_for_input:
            command = self.__get_user_choice()

            if command == -1:
                manipulate_chain(self.blockchain)

            elif command == 1:
                transaction_verified = self.__request_tx_data()
                printDependingOn(
                    transaction_verified, 'Transaction verified.', 'Transaction rejected.')

            elif command == 2:
                mine_block(
                    self.blockchain, self.open_transactions, self.owner)

            elif command == 3:
                print_participants(self.participants)

            elif command == 4:
                print_blocks(self.blockchain)

            elif command == 5:
                transactions_verified = verify_transactions(
                    self.blockchain, self.open_transactions)
                printDependingOn(
                    transactions_verified, 'All transactions are valid', 'Invalid transaction found!')

            elif command == 0:
                print('Exiting Program.')
                break

            is_valid = self.verifier.is_verified(self.blockchain)
            if not is_valid:
                print('Invalid blockchain... exiting!')
                waiting_for_input = False

            print('Balance: ', get_balance(self.owner, self.blockchain))

    def __request_tx_data(self) -> bool:
        """ Adds transaction amount and recipient to open transactions """
        tx_amount, tx_recipient = ask_for_tx()
        return add_transaction(
            self.owner, tx_recipient, tx_amount, chain=self.blockchain, open_tx=self.open_transactions, participants=self.participants)

    def __get_user_choice(
            self,
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
