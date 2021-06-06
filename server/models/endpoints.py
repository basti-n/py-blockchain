from enum import Enum


class BlockchainEndpoints(str, Enum):
    INDEX = '/'
    NETWORK = '/network'
    TRANSACTION = '/transaction'
    TRANSACTIONS = '/transactions'
    BROADCAST_TRANSACTION = '/broadcast-transactions'
