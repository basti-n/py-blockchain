from core.models.storage import StorageAction
from utils.binaryConverters import BinaryConverter
from utils.blockchainLogger import warn_no_key
from core.walletStorage import WalletStorage
from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random


class Wallet:
    def __init__(self, bits=1024) -> None:
        self.__bits = bits
        self.__private_key = None
        self.__public_key = None
        self.storage = WalletStorage()

    @property
    def public_key(self):
        return self.__public_key

    @property
    def has_keys(self):
        return self.__public_key != None and self.__private_key != None

    def generate_keys(self) -> Tuple[str, str]:
        """ Generates a pair of private-public key """
        try:
            private_key = RSA.generate(
                self.__bits, Crypto.Random.new().read)
            public_key = private_key.publickey()

            return (Wallet.to_ascii(private_key), Wallet.to_ascii(public_key))

        except Exception as error:
            print('Error generating keys (Message: {})'.format(error))
            return ()

    def load_keys(self) -> bool:
        """ Loads private and public key from file """
        keys = self.storage.load()
        if not keys == None and len(keys) > 1:
            self.__private_key, self.__public_key = keys
            return True

        return False

    def save_keys(self) -> bool:
        """ Saves private and public key to file """
        if self.has_keys:
            return self.storage.save(self.__private_key, self.__public_key)
        else:
            warn_no_key(StorageAction.SAVING)

    def create_keys(self) -> None:
        """ Creates and sets private and public key """
        self.__private_key, self.__public_key = self.generate_keys()

    def create_signature(self, sender: str, recipient: str, amount: int) -> str:
        """ Signs and returns a stringified version of the hashed transaction """
        signer: PKCS1_v1_5.PKCS115_SigScheme = Wallet.sign_transaction(
            self.__private_key)
        hashed_tx = Wallet.hash_transaction(sender, recipient, amount)
        return BinaryConverter.to_ascii(signer.sign(hashed_tx))

    @classmethod
    def to_ascii(cls, key) -> str:
        return BinaryConverter.to_ascii(key.exportKey(format='DER'))

    @classmethod
    def to_binary(cls, key: str) -> bytes:
        return BinaryConverter.to_binary(key)

    @classmethod
    def import_key(cls, key: str):
        return RSA.importKey(cls.to_binary(key))

    @classmethod
    def sign_transaction(cls, key: str):
        return PKCS1_v1_5.new(
            cls.import_key(key))

    @classmethod
    def hash_transaction(cls, sender: str, recipient: str, amount: int, *, encoding='utf8') -> SHA256.SHA256Hash:
        return SHA256.new((str(sender) + str(recipient) + str(amount)).encode(encoding))
