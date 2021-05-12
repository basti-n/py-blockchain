import binascii


class BinaryConverter:
    @staticmethod
    def to_ascii(data: bytes) -> str:
        return binascii.hexlify(data).decode('ascii')

    @staticmethod
    def to_binary(data: str) -> bytes: 
        return binascii.unhexlify(data)
