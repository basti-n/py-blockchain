from core.blockchainTx import get_latest_transaction
import os
from server.models.requiredFields import RequiredFields
from server.responseGuards import ensure_required_fields, ensure_tx_appended, ensure_wallet
from server.models.endpoints import BlockchainEndpoints
from server.txSyncer import TransactionSync
from typing import Dict, Union
from utils.argumentParser import CommandLineArgumentParser
from server.response import Response
from blockchain import *
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from server.responseHelpers import get_message, get_missing_fields, get_serializable_block, get_serializable_peer_nodes, get_serializable_transaction, has_all_required_fields, jsonify_chain
from server.models.statusCodes import HttpStatusCodes
from server.requestHelpers import get_param
from core.blockchainFactory import BlockchainFileStorageFactory

app = Flask(__name__)
CORS(app)

host = '0.0.0.0'
port = int(os.environ.get('PORT', 5000))


@app.route(BlockchainEndpoints.INDEX, methods=[HttpStatusCodes.GET])
def get_home():
    return send_from_directory('ui/templates', 'node.html')


@ app.route(BlockchainEndpoints.NETWORK, methods=[HttpStatusCodes.GET])
def get_network():
    return send_from_directory('ui/templates', 'network.html')


@ app.route(BlockchainEndpoints.TRANSACTION, methods=[HttpStatusCodes.POST])
def add_transaction():
    ensure_wallet(blockchain, action_subject='transaction')

    transaction_data: Union(Dict, None) = request.get_json()

    ensure_required_fields(transaction_data, RequiredFields.get_required_fields(BlockchainEndpoints.TRANSACTION),
                           action_subject='transaction')

    ensure_tx_appended(blockchain.add_transaction(**transaction_data))

    tx_syncer = TransactionSync(blockchain.peer_nodes)
    broadcast_tx_succes = tx_syncer.broadcast_transactions(
        blockchain.latest_transaction)

    message = get_message(HttpStatusCodes.POST,
                          True, 'transaction')
    return Response({'transaction': get_serializable_transaction(blockchain.latest_transaction), 'missing_fields': None, "transactions_synced": broadcast_tx_succes}, message, 200).get()


@ app.route(BlockchainEndpoints.BROADCAST_TRANSACTION, methods=[HttpStatusCodes.POST])
def broadcast_transactions():
    transaction_data: Union(Dict, None) = request.get_json()

    ensure_required_fields(transaction_data, RequiredFields.get_required_fields(BlockchainEndpoints.TRANSACTION),
                           action_subject='broadcast transaction')

    ensure_tx_appended(blockchain.add_transaction(
        **transaction_data, is_broadcast_tx=True))

    message = get_message(HttpStatusCodes.POST,
                          True, 'broadcast transaction')
    return Response({'transaction': get_serializable_transaction(blockchain.latest_transaction), 'missing_fields': None, "transactions_synced": True}, message, 200).get()


@ app.route(BlockchainEndpoints.TRANSACTIONS, methods=[HttpStatusCodes.GET])
def get_open_transactions():
    if not blockchain.has_wallet:
        message = get_message(HttpStatusCodes.GET, False,
                              'open transaction', additional_info='No Wallet found!')
        return Response({'open_transactions': None}, message, 500).get()

    message = get_message(HttpStatusCodes.GET, True, 'open transaction', )
    return Response({'open_transactions': get_serializable_transaction(blockchain.open_transactions)}, message, 200).get()


@ app.route('/wallet', methods=[HttpStatusCodes.POST])
def create_wallet():
    saved = False
    error = False

    try:
        _, private_key = blockchain.create_wallet()
    except:
        error = True

    should_save = get_param(request, 'save')
    if(should_save and not error):
        try:
            saved = blockchain.save_wallet()
        except:
            error = True

    success = error is False
    message = get_message(HttpStatusCodes.POST, success, 'wallet')
    status = 201 if success else 500
    return Response({'public_key': blockchain.owner, 'private_key': private_key, 'savedWallet': saved}, message, status).get()


@ app.route('/wallet', methods=[HttpStatusCodes.GET])
def load_wallet():
    blockchain.load_wallet()
    if blockchain.has_wallet:
        message = get_message(HttpStatusCodes.GET, True, 'wallet')
        return Response({'public_key': blockchain.owner, 'savedWallet': True}, message, 200).get()

    message = get_message(HttpStatusCodes.GET, False, 'wallet')
    return Response({'public_key': blockchain.owner, 'savedWallet': False}, message, 500).get()


@ app.route('/balance', methods=[HttpStatusCodes.GET])
def get_balance():
    if not blockchain.has_wallet:
        message = get_message(HttpStatusCodes.GET, False, 'balance')
        return Response({'funds': 0, 'hasOwner': False}, message, 500).get()

    message = message = get_message(HttpStatusCodes.GET, True, 'balance')
    return Response({'funds': blockchain.balance, 'hasOwner': True}, message, 200).get()


@ app.route('/chain', methods=[HttpStatusCodes.GET])
def get_chain():
    chain_snapshot = blockchain.blockchain
    return jsonify_chain(chain_snapshot), 200


@ app.route('/mine', methods=[HttpStatusCodes.POST])
def mine():
    try:
        miningSuccessful = blockchain.mine()
        created_block = blockchain.latest_block
        return Response({'block': get_serializable_block(created_block)}, get_message(HttpStatusCodes.POST, True, 'block'), 200).get() if miningSuccessful else Response({'error': True}, get_message(HttpStatusCodes.POST, False, 'block'), 400).get()
    except Exception as error:
        message = get_message(HttpStatusCodes.POST, False, 'block', error)
        return Response({}, message, 500).get()


@ app.route('/node', methods=[HttpStatusCodes.POST])
def create_node():
    """ Adds a node to the blockchain peer nodes """
    body: Dict = request.get_json()
    node_to_add = body.get('node')
    if not body or not node_to_add:
        return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.POST, False, 'node', additional_info='Please provide a valid node to add.'), 400).get()

    if blockchain.add_peer_node(node_to_add):
        return Response({'node': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.POST, True, 'node'), 200).get()

    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.POST, False, 'node', additional_info=f'Saving peer node {node_to_add} failed!'), 400).get()


@ app.route('/node/<path:peer_node>', methods=[HttpStatusCodes.DELETE])
def delete_node(peer_node: str):
    """ Deletes a node from the blockchain peer nodes """
    node_to_delete = peer_node
    if not len(node_to_delete):
        return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.DELETE, False, 'node', additional_info='Please provide a valid node to delete.'), 400).get()

    if not node_to_delete in blockchain.peer_nodes:
        return Response({'node': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.DELETE, False, 'node', additional_info=f'Delete peer node {node_to_delete} failed. No peer node found!'), 500).get()

    blockchain.remove_peer_node(node_to_delete)
    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.DELETE, True, 'node'), 200).get()


@ app.route('/nodes', methods=[HttpStatusCodes.GET])
def get_nodes():
    """ Returns all peer nodes associated with blockchain """
    all_nodes = blockchain.peer_nodes
    if all_nodes is None:
        return Response({'nodes': None}, get_message(HttpStatusCodes.GET, False, 'node'), 500).get()

    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpStatusCodes.GET, True, 'node'), 200).get()


if __name__ == '__main__':
    parser = CommandLineArgumentParser(
        {'port': {'default': port, 'type': int}})
    port = parser.arguments.port
    blockchain = Blockchain(BlockchainFileStorageFactory, node_id=port)

    print('Starting Server on PORT {}'.format(port))
    app.run(host, port, debug=True)
