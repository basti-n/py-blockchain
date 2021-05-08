from core.blc import Blockchain
from utils.metaclasses.singletonMeta import SingletonMeta
from core.blockchainTx import ask_for_tx, verify_transactions, get_balance
from core.blockchainVerifier import Verifier
from utils.blockchainHelpers import manipulate_chain
from utils.blockchainOutput import printDependingOn
from utils.blockchainLogger import print_blocks, print_participants
from typing import Set


class GUI(metaclass=SingletonMeta):
    def __init__(self, *, blockchain: Blockchain, participants: Set[str], verifier: Verifier):
        self.blockchain = blockchain
        self.participants = participants
        self.verifier = verifier
        pass

    def start(self) -> None:
        waiting_for_input = True
        while waiting_for_input:
            command = self.__get_user_choice()

            if command == -1:
                manipulate_chain(self.blockchain.blockchain)

            elif command == 1:
                transaction_verified = self.__request_tx_data()
                printDependingOn(
                    transaction_verified, 'Transaction verified.', 'Transaction rejected.')

            elif command == 2:
                self.blockchain.mine()

            elif command == 3:
                print_participants(self.participants)

            elif command == 4:
                print_blocks(self.blockchain.blockchain)

            elif command == 5:
                transactions_verified = verify_transactions(
                    self.blockchain.blockchain, self.blockchain.open_transactions)
                printDependingOn(
                    transactions_verified, 'All transactions are valid', 'Invalid transaction found!')

            elif command == 6:
                self.blockchain.create_wallet()

            elif command == 7:
                pass

            elif command == 0:
                print('Exiting Program.')
                break

            is_valid = self.verifier.is_verified(self.blockchain.blockchain)
            if not is_valid:
                print('Invalid blockchain... exiting!')
                waiting_for_input = False

            print('Balance: ', get_balance(
                self.blockchain.owner, self.blockchain.blockchain, self.blockchain.open_transactions))

    def __request_tx_data(self) -> bool:
        """ Adds transaction amount and recipient to open transactions """
        tx_amount, tx_recipient = ask_for_tx()
        return self.blockchain.add_transaction(self.blockchain.owner, tx_recipient, tx_amount, participants=self.participants)

    def __get_user_choice(
            self,
            firstOption: str = 'Add transaction',
            secondOption: str = 'Mine Blocks',
            thirdOption: str = 'Print Participants',
            fourthOption: str = 'Print Blocks',
            fifthOption: str = 'Verify open transactions',
            sixthOption: str = 'Create Wallet',
            seventhOption: str = 'Load Wallet',
            offerQuit: bool = True,
            offerManipulate: bool = True) -> int:
        """ Returns the user choise as an integer """
        print('Please enter your desired command.')
        print(f'Option 1: {firstOption}')
        print(f'Option 2: {secondOption}')
        print(f'Option 3: {thirdOption}')
        print(f'Option 4: {fourthOption}')
        print(f'Option 5: {fifthOption}')
        print(f'Option 6: {sixthOption}')
        print(f'Option 7: {seventhOption}')

        if offerQuit == True:
            print(f'Quit: Press "q" for quitting')
        if offerManipulate == True:
            print(f'Manipulate: Press "m" for manipulating')

        reply = input('Enter your command? ')
        if reply.lower() == 'm':
            return -1
        return 0 if reply.lower() == 'q' else int(reply)
