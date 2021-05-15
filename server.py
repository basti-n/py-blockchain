from blockchain import *
from core.blockchainWallet import Wallet
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

wallet = Wallet()

host = '0.0.0.0'
port = 5000


@app.route('/', methods=['GET'])
def get_ui():
    return '<h1>Blockchain Server</h1><p>Welcome to the server!</p>'


if __name__ == '__main__':
    app.run(host, port)
