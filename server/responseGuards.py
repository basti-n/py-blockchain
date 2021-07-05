from server.models.httpMethods import HttpMethods
from typing import Dict, List, Union
from core.blc import Blockchain
from server.response import Response
from server.responseHelpers import get_message, get_missing_fields, has_all_required_fields

def ensure_wallet(blockchain: Blockchain, *, action_subject: str) -> Union[None, Response]:
    """ Handles Response for Requests with missing wallet """
    if not blockchain.has_wallet:
        message = get_message(HttpMethods.POST, False,
                              action_subject, additional_info='No Wallet found!')
        return Response({action_subject: None}, message, 500).get()


def ensure_required_fields(data: Union[Dict, None], required_fields: List[str], *, action_subject: str) -> Union[None, Response]:
    """ Handles Response for Requests with missing fields """
    if not has_all_required_fields(data, required_fields):
        missing_fields = get_missing_fields(data, required_fields)
        missing_fields_stringified = ', '.join(missing_fields)
        message = get_message(HttpMethods.POST, False,
                              action_subject, additional_info=f'Please Provide complete {action_subject}. Missing Fields: {missing_fields_stringified}')
        return Response({action_subject: None, 'missing_fields': missing_fields, "transactions_synced": False}, message, 400).get()


def ensure_tx_appended(add_transaction_success: bool) -> Union[None, Response]:
    if not add_transaction_success:
        message = get_message(HttpMethods.POST, False, 'transaction')
        return Response({'transaction': None, 'missing_fields': None, "transactions_synced": False}, message, 500).get()
