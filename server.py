import os
from server.models.statusCodes import HttpStatusCodes
from server.models.httpMethods import HttpMethods
from utils.blockchainHelpers import block_from_deserialized_block
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
from server.responseHelpers import get_message, get_serializable_block, get_serializable_peer_nodes, get_serializable_transaction, jsonify_chain
from server.requestHelpers import get_param
from server.blockSyncer import BlockSync
from core.blockchainFactory import BlockchainFileStorageFactory
from core.blockchainBlock import is_future_block, is_next_block, is_previous_block

app = Flask(__name__)
CORS(app)

host = '0.0.0.0'
port = int(os.environ.get('PORT', 5000))


@app.route(BlockchainEndpoints.INDEX, methods=[HttpMethods.GET])
def get_home():
    return send_from_directory('ui/templates', 'node.html')


@ app.route(BlockchainEndpoints.NETWORK, methods=[HttpMethods.GET])
def get_network():
    return send_from_directory('ui/templates', 'network.html')


@ app.route(BlockchainEndpoints.BROADCAST_BLOCK, methods=[HttpMethods.POST])
def broadcast_block():
    block_data: Union(Dict, None) = request.get_json()

    ensure_required_fields(block_data, RequiredFields.get_required_fields(BlockchainEndpoints.BROADCAST_BLOCK),
                           action_subject='broadcast block')

    broadcast_block = block_from_deserialized_block(block_data['block'])
    successMessage = get_message(HttpMethods.POST, True, 'broadcast block')
    errorMessage = get_message(HttpMethods.POST, False, 'broadcast block')

    if is_next_block(blockchain, broadcast_block):
        blockchain_added = blockchain.add_block(broadcast_block)

        if blockchain_added:
            return Response({}, successMessage, 200).get()

        return Response({}, errorMessage, 400).get()

    elif is_future_block(blockchain, broadcast_block):
        blockchain.has_conflicts = True
        return Response({}, errorMessage, 200).get()

    elif is_previous_block(blockchain, broadcast_block):
        return Response({}, errorMessage, HttpStatusCodes.CONFLICT).get()


@ app.route(BlockchainEndpoints.TRANSACTION, methods=[HttpMethods.POST])
def add_transaction():
    ensure_wallet(blockchain, action_subject='transaction')

    transaction_data: Union(Dict, None) = request.get_json()

    ensure_required_fields(transaction_data, RequiredFields.get_required_fields(BlockchainEndpoints.TRANSACTION),
                           action_subject='transaction')

    ensure_tx_appended(blockchain.add_transaction(**transaction_data))

    tx_syncer = TransactionSync(blockchain.peer_nodes)
    broadcast_tx_succes, _ = tx_syncer.broadcast(
        blockchain.latest_transaction)

    message = get_message(HttpMethods.POST,
                          True, 'transaction')
    return Response({'transaction': get_serializable_transaction(blockchain.latest_transaction), 'missing_fields': None, "transactions_synced": broadcast_tx_succes}, message, 200).get()


@ app.route(BlockchainEndpoints.BROADCAST_TRANSACTION, methods=[HttpMethods.POST])
def broadcast_transactions():
    transaction_data: Union(Dict, None) = request.get_json()

    ensure_required_fields(transaction_data, RequiredFields.get_required_fields(BlockchainEndpoints.TRANSACTION),
                           action_subject='broadcast transaction')

    ensure_tx_appended(blockchain.add_transaction(
        **transaction_data, is_broadcast_tx=True))

    message = get_message(HttpMethods.POST,
                          True, 'broadcast transaction')
    return Response({'transaction': get_serializable_transaction(blockchain.latest_transaction), 'missing_fields': None, "transactions_synced": True}, message, 200).get()


@ app.route(BlockchainEndpoints.TRANSACTIONS, methods=[HttpMethods.GET])
def get_open_transactions():
    if not blockchain.has_wallet:
        message = get_message(HttpMethods.GET, False,
                              'open transaction', additional_info='No Wallet found!')
        return Response({'open_transactions': None}, message, 500).get()

    message = get_message(HttpMethods.GET, True, 'open transaction', )
    return Response({'open_transactions': get_serializable_transaction(blockchain.open_transactions)}, message, 200).get()


@ app.route('/wallet', methods=[HttpMethods.POST])
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
    message = get_message(HttpMethods.POST, success, 'wallet')
    status = 201 if success else 500
    return Response({'public_key': blockchain.owner, 'private_key': private_key, 'savedWallet': saved}, message, status).get()


@ app.route('/wallet', methods=[HttpMethods.GET])
def load_wallet():
    blockchain.load_wallet()
    if blockchain.has_wallet:
        message = get_message(HttpMethods.GET, True, 'wallet')
        return Response({'public_key': blockchain.owner, 'savedWallet': True}, message, 200).get()

    message = get_message(HttpMethods.GET, False, 'wallet')
    return Response({'public_key': blockchain.owner, 'savedWallet': False}, message, 500).get()


@ app.route('/balance', methods=[HttpMethods.GET])
def get_balance():
    if not blockchain.has_wallet:
        message = get_message(HttpMethods.GET, False, 'balance')
        return Response({'funds': 0, 'hasOwner': False}, message, 500).get()

    message = message = get_message(HttpMethods.GET, True, 'balance')
    return Response({'funds': blockchain.balance, 'hasOwner': True}, message, 200).get()


@ app.route(BlockchainEndpoints.CHAIN, methods=[HttpMethods.GET])
def get_chain():
    chain_snapshot = blockchain.blockchain
    return jsonify_chain(chain_snapshot), 200


@ app.route('/mine', methods=[HttpMethods.POST])
def mine():
    if blockchain.has_conflicts:
        message = get_message(HttpMethods.POST, False,
                              'block', additional_info='Conflict: Please resolve the conflict first!')
        return Response({'blockSynced': False, 'conflict': True}, message, HttpStatusCodes.CONFLICT).get()

    try:
        mining_successful = blockchain.mine()
        created_block = blockchain.latest_block
        if mining_successful and created_block:
            blockSyncer = BlockSync(blockchain.peer_nodes)
            broadcast_tx_succes, has_conflicts = blockSyncer.broadcast(
                created_block)
            blockchain.has_conflicts = has_conflicts

        return Response({'block': get_serializable_block(created_block), 'blockSynced': broadcast_tx_succes, 'conflict': blockchain.has_conflicts}, get_message(HttpMethods.POST, True, 'block'), HttpStatusCodes.SUCCESS).get() if mining_successful else Response({'error': True}, get_message(HttpMethods.POST, False, 'block'), 400).get()
    except Exception as error:
        message = get_message(HttpMethods.POST, False,
                              'block', additional_info=f'(Error: {error})')
        return Response({'blockSynced': False}, message, HttpStatusCodes.SERVER_ERROR).get()


@app.route(BlockchainEndpoints.RESOLVE_CONFLICTS, methods=[HttpMethods.POST])
def resolve_conflicts():
    blockchain_replaced = blockchain.resolve_conflicts()

    if blockchain_replaced:
        blockchain.has_conflicts = False

    conflict_message = 'Conflict succesfully resolved.' if blockchain_replaced else 'No Conflict found. Blockchain unchanged.'
    message = get_message(HttpMethods.POST, blockchain_replaced,
                          'conflict', additional_info=conflict_message)
    return Response({'conflictResolved': blockchain_replaced}, message, HttpStatusCodes.SUCCESS).get()


@ app.route('/node', methods=[HttpMethods.POST])
def create_node():
    """ Adds a node to the blockchain peer nodes """
    body: Dict = request.get_json()
    node_to_add = body.get('node')
    if not body or not node_to_add:
        return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.POST, False, 'node', additional_info='Please provide a valid node to add.'), 400).get()

    if blockchain.add_peer_node(node_to_add):
        return Response({'node': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.POST, True, 'node'), 200).get()

    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.POST, False, 'node', additional_info=f'Saving peer node {node_to_add} failed!'), 400).get()


@ app.route('/node/<path:peer_node>', methods=[HttpMethods.DELETE])
def delete_node(peer_node: str):
    """ Deletes a node from the blockchain peer nodes """
    node_to_delete = peer_node
    if not len(node_to_delete):
        return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.DELETE, False, 'node', additional_info='Please provide a valid node to delete.'), 400).get()

    if not node_to_delete in blockchain.peer_nodes:
        return Response({'node': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.DELETE, False, 'node', additional_info=f'Delete peer node {node_to_delete} failed. No peer node found!'), 500).get()

    blockchain.remove_peer_node(node_to_delete)
    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.DELETE, True, 'node'), 200).get()


@ app.route('/nodes', methods=[HttpMethods.GET])
def get_nodes():
    """ Returns all peer nodes associated with blockchain """
    all_nodes = blockchain.peer_nodes
    if all_nodes is None:
        return Response({'nodes': None}, get_message(HttpMethods.GET, False, 'node'), 500).get()

    return Response({'nodes': get_serializable_peer_nodes(blockchain.peer_nodes)}, get_message(HttpMethods.GET, True, 'node'), 200).get()


if __name__ == '__main__':
    parser = CommandLineArgumentParser(
        {'port': {'default': port, 'type': int}})
    port = parser.arguments.port
    blockchain = Blockchain(BlockchainFileStorageFactory, node_id=port)

    print('Starting Server on PORT {}'.format(port))
    app.run(host, port, debug=True)
