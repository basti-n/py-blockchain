from server.response import Response
from blockchain import *
from flask import Flask
from flask_cors import CORS
from server.responseHelpers import jsonify_chain
from core.blockchainFactory import BlockchainFileStorageFactory

app = Flask(__name__)
CORS(app)

blockchain = Blockchain(BlockchainFileStorageFactory)

host = '0.0.0.0'
port = 5000


@app.route('/', methods=['GET'])
def get_ui():
    return '<h1>Blockchain Server</h1><p>Welcome to the server!</p>'


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.blockchain
    return jsonify_chain(chain_snapshot), 200


@app.route('/mine', methods=['POST'])
def mine():
    try:
        miningSuccessful = blockchain.mine()
        chain_snapshot = blockchain.blockchain
        return Response({'blockchain': jsonify_chain(chain_snapshot)}, 'Success: [Post] mining succeeded', 200).get() if miningSuccessful else Response({'error': True}, 'Error: [Post] mining failed', 400).get()
    except Exception as error:
        message = 'Error: [POST] minining failed (Message; {}'.format(error)
        return Response({}, message, 500).get()


if __name__ == '__main__':
    app.run(host, port)
