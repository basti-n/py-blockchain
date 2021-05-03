from blockchainTx import Transaction


class PrettyPrintBlockMixin:
    def __str__(self) -> str:
        return str([f'{key}: {[item for item in value] if isinstance(value, list) else str(value)}' for (key, value) in self.__dict__.items()]).replace('\'', '')
