from server.response import Response
from blockchain import *
from flask import Flask
from flask_cors import CORS
from server.responseHelpers import get_message, jsonify_chain, stringify_blocks
from server.models.statusCodes import HttpStatusCodes
from core.blockchainFactory import BlockchainFileStorageFactory

app = Flask(__name__)
CORS(app)

blockchain = Blockchain(BlockchainFileStorageFactory)

host = '0.0.0.0'
port = 5000


@app.route('/', methods=[HttpStatusCodes.GET])
def get_ui():
    return '<h1>Blockchain Server</h1><p>Welcome to the server!</p>'


@app.route('/wallet', methods=[HttpStatusCodes.POST])
def create_wallet():
    public_key, private_key = blockchain.create_wallet()
    saved = False
    error = False
    # Todo: get data from params to also save
    if(True):
        try:
            saved = blockchain.save_wallet()
        except:
            error = True

    success = saved is True and error is False
    message = get_message(HttpStatusCodes.POST, success, 'wallet')
    status = 201 if success else 500
    return Response({'public_key': public_key, 'private_key': private_key, 'savedWallet': saved}, message, status).get()


@app.route('/wallet', methods=[HttpStatusCodes.GET])
def load_wallet():
    blockchain.load_wallet()
    if blockchain.owner != None:
        message = get_message(HttpStatusCodes.GET, True, 'wallet')
        return Response({'public_key': blockchain.owner, 'savedWallet': True}, message, 200).get()

    message = get_message(HttpStatusCodes.GET, False, 'wallet')
    return Response({'public_key': blockchain.owner, 'savedWallet': False}, message, 500).get()


@app.route('/chain', methods=[HttpStatusCodes.GET])
def get_chain():
    chain_snapshot = blockchain.blockchain
    return jsonify_chain(chain_snapshot), 200


@app.route('/mine', methods=[HttpStatusCodes.POST])
def mine():
    try:
        miningSuccessful = blockchain.mine()
        chain_snapshot = blockchain.blockchain
        return Response({'blockchain': stringify_blocks(chain_snapshot)}, get_message(HttpStatusCodes.POST, True, 'block'), 200).get() if miningSuccessful else Response({'error': True}, get_message(HttpStatusCodes.POST, False, 'block'), 400).get()
    except Exception as error:
        message = get_message(HttpStatusCodes.POST, False, 'block', error)
        return Response({}, message, 500).get()


if __name__ == '__main__':
    app.run(host, port)
