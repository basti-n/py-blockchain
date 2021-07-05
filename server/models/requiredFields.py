from typing import List
from server.models.endpoints import BlockchainEndpoints


class RequiredFields:
    @staticmethod
    def get_required_fields(endpoint: BlockchainEndpoints) -> List[str]:
        if endpoint == BlockchainEndpoints.BROADCAST_TRANSACTION or endpoint == BlockchainEndpoints.TRANSACTION:
            return ['sender', 'recipient', 'amount']

        if endpoint == BlockchainEndpoints.BROADCAST_BLOCK:
            return ['block']

        return []
