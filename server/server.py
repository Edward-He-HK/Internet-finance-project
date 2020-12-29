from flask import Flask, jsonify, request
import sys

from project.blockchain import *
from project.wallet import *
from project.transaction import *
import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii
import json
import requests
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import datetime
import sys
from hashlib import sha256

app = Flask(__name__)
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    values = request.form
    required = ['recipient_address', 'amount']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction = Transaction(myWallet.identity, values['recipient_address'], values['amount'])
    transaction.add_signature(myWallet.sign_transaction(transaction))
    transaction_result = blockchain.add_new_transaction(transaction)
    if transaction_result:
        response = {'message': 'Transaction will be added to Block '}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    # Get transactions from transactions pool
    transactions = blockchain.unconfirmed_transactions
    response = {'transactions': transactions}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def part_chain():
    response = {
        'chain': blockchain.chain[-10:],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/fullchain', methods=['GET'])
def full_chain():
    response = {
        'chain': json.dumps(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/fullchain2', methods=['GET'])
def full_chain2():
    response = {
        'chain': json.dumps(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return json.dumps(response).replace('\\', '').replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}'), 200
    
    
    
@app.route('/fullchain3', methods=['POST'])
def full_chain3():
    response = {
        'chain': json.dumps(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return json.dumps(response).replace('\\', '').replace('"[', '[').replace(']"', ']').replace('"{', '{').replace('}"', '}'), 200

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200


@app.route('/register_node', methods=['POST'])
def register_node():
    values = request.form
    node = values.get('node')
    com_port = values.get('com_port')
    # handle type B request
    if com_port is not None:
        blockchain.register_node(request.remote_addr + ":" + com_port)
        return "ok", 200
    # handle type A request
    if node is None and com_port is None:
        return "Error: Please supply a valid nodes", 400
    blockchain.register_node(node)
    # retrieve nodes list
    node_list = requests.get('http://' + node + '/get_nodes')
    if node_list.status_code == 200:
        node_list = node_list.json()['nodes']
        for node in node_list:
            blockchain.register_node(node)
    for new_nodes in blockchain.nodes:
        # sending type B request
        requests.post('http://' + new_nodes + '/register_node', data={'com_port': str(port)})
    # check if our chain is authoritative from other nodes
    replaced = blockchain.consensus()
    if replaced:
        response = {
            'message': 'Longer authoritative chain found from peers,replacing ours',
            'total_nodes': [node for node in blockchain.nodes]
        }
    else:
        response = {
            'message': 'New nodes have been added, but our chain is authoritative',
            'total_nodes': [node for node in blockchain.nodes]
        }
    return jsonify(response), 201


@app.route('/consensus', methods=['GET'])
def consensus():
    replaced = blockchain.consensus()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
        }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    
    newblock = blockchain.mine(myWallet)
    for node in blockchain.nodes:
        requests.get('http://' + node + '/consensus')
    response = {
        'index': newblock.index,
        'transactions': newblock.transactions,
        'timestamp': newblock.timestamp,
        'nonce': newblock.nonce,
        'hash': newblock.hash,
        'previous_hash': newblock.previous_hash,
        'difficulty': newblock.difficulty

    }
    return jsonify(response), 200

@app.route('/check_balance', methods=['POST'])
def check_balance():
    values = request.form
    required = ['address']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    address = values.get('address')
    balance = blockchain.check_balance(address)
    return jsonify(balance), 200

@app.route('/balance', methods=['GET'])
def balance():
    balance = blockchain.check_balance(myWallet.identity)
    return jsonify(balance), 200

@app.route('/check_my_balance', methods=['POST'])
def check_my_balance():
    balance = blockchain.check_balance(myWallet.identity)
    return jsonify(balance), 200

@app.route('/return_address', methods=['POST'])
def return_address():
    address = myWallet.identity
    return str(address), 200

@app.route('/return_address2', methods=['GET'])
def return_address2():
    address = myWallet.identity
    return str(address), 200

'''@app.route('/interest1', methods=['GET'])
def interest1():
    isMine=False
    newblock = blockchain.mine(myWallet,isMine)
    for node in blockchain.nodes:
        requests.get('http://' + node + '/consensus')
    response = {
        'index': newblock.index,
        'transactions': newblock.transactions,
        'timestamp': newblock.timestamp,
        'nonce': newblock.nonce,
        'hash': newblock.hash,
        'previous_hash': newblock.previous_hash,
        'difficulty': newblock.difficulty,
        
        }
    return jsonify(response), 200 
        
@app.route('/interest2', methods=['POST'])
def interest2():
    isMine=False
    newblock = blockchain.mine(myWallet,isMine)
    for node in blockchain.nodes:
        requests.get('http://' + node + '/consensus')
    response = {
        'index': newblock.index,
        'transactions': newblock.transactions,
        'timestamp': newblock.timestamp,
        'nonce': newblock.nonce,
        'hash': newblock.hash,
        'previous_hash': newblock.previous_hash,
        'difficulty': newblock.difficulty
        }
    return jsonify(response), 200 '''

if __name__ == '__main__':
    myWallet = Wallet()
    blockchain = Blockchain()
    print(myWallet.identity)

    bal = blockchain.check_balance(myWallet.identity)
    print(bal)

    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)




