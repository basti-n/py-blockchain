from typing import Any, Tuple
from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self, bits=1024) -> None:
        self.__bits = bits
        self.__private_key = None
        self.__public_key = None

    @property
    def public_key(self):
        return self.__public_key

    def generate_keys(self) -> Tuple[str, str]:
        """ Generates a pair of private-public key """
        try:
            private_key = RSA.generate(
                self.__bits, Crypto.Random.new().read)
            public_key = private_key.publickey()

            return (self.__to_ascii(private_key), self.__to_ascii(public_key))
        except Exception as error:
            print('Error generating keys (Message: {})'.format(error))
            return ()

    def load_keys(self) -> Any:
        pass

    def create_keys(self) -> None:
        """ Creates and sets private and public key """
        self.__private_key, self.__public_key = self.generate_keys()

    def __to_ascii(self, key) -> str:
        return binascii.hexlify(key.exportKey(format='DER')).decode('ascii')
