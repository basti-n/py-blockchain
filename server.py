from server.response import Response
from blockchain import *
from flask import Flask
from flask_cors import CORS
from server.responseHelpers import jsonify_chain, stringify_blocks
from core.blockchainFactory import BlockchainFileStorageFactory

app = Flask(__name__)
CORS(app)

blockchain = Blockchain(BlockchainFileStorageFactory)

host = '0.0.0.0'
port = 5000


@app.route('/', methods=['GET'])
def get_ui():
    return '<h1>Blockchain Server</h1><p>Welcome to the server!</p>'


@app.route('/wallet', methods=['POST'])
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
    message = 'Success: [Post] creating wallet succeeded' if success else 'Error: [Post] creating wallet failed'
    status = 201 if success else 500
    return Response({'public_key': public_key, 'private_key': private_key, 'savedWallet': saved}, message, status).get()


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.blockchain
    return jsonify_chain(chain_snapshot), 200


@app.route('/mine', methods=['POST'])
def mine():
    try:
        miningSuccessful = blockchain.mine()
        chain_snapshot = blockchain.blockchain
        return Response({'blockchain': stringify_blocks(chain_snapshot)}, 'Success: [Post] mining succeeded', 200).get() if miningSuccessful else Response({'error': True}, 'Error: [Post] mining failed', 400).get()
    except Exception as error:
        message = 'Error: [POST] minining failed (Message; {}'.format(error)
        return Response({}, message, 500).get()


if __name__ == '__main__':
    app.run(host, port)
