# importing flask to show our data on webpage using the frame
# importing datetime to get the realtime
# importing hashlib to convert our data into hash value
# importing urlparse to parse the url into subpart to work easily on that
# importing json to access and use the data in json format
from flask import Flask, jsonify, request
import requests
import datetime
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse

# creating a class and initializing a list named chain & transaction , set named as nodes in constructor
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.nodes = set()
        self.create_block(proof = 1, previous_hash = '0')

# creating a function to create the block in which our data is stored and adding it to our chain
# this function will be used by miner to append the block to chain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                  'timeStamp': str(datetime.datetime.now()),
                  'proof': proof,
                  'previous_hash': previous_hash,
                  'transaction': self.transaction}
        self.transaction = []
        self.chain.append(block)
        return block

    # function to return the last block in the chain
    def get_previous_block(self):
        return self.chain[-1]

# generating a proof value which help to create hash value for every block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        # an infinite loop to find out the nonce value
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                break
            else:
                new_proof = new_proof + 1
        return new_proof

# creating the hash value
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# checking whether our chain is valid or not on basis of some values like proof and hash
    def chain_validity(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            # check if nonce is correct or not
            if hash_operation[:5] != '00000':
                return False

            # check if the previous hash is correctly stored or not
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_block = block
            block_index += 1
        return True

# function to add transactions data in transaction list and store it until it added to a block
    def add_transaction(self,sender,receiver,amount):
        self.transaction.append({'sender': sender,
                                 'receiver': receiver,
                                 'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index']+1

# function to add multiple nodes and connect them
# this is required so that if someone else makes a request saying he has mined the block before us
# then we can take care of that too
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

# function to replace the chain of every node  with the longest chain
# by default we assume our chain is the longest chain and comparing it with chain's of other nodes
# if we found any another node has longer chain than our one then we replicate that on every node
    def replace_chain(self):
        network = self.nodes()
        max_length = len(self.chain)
        longest_chain = None
        for node in network:
            response = request.get(f'https://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.chain_validity(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# initialize flask and creating object of class Blockchain

app = Flask(__name__)
blockchain = Blockchain()


# route used by miner to mine the block and append in blockchain
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': "congratulations!..your block is inserted successfully...",
                'index': block['index'],
                'timeStamp': block['timeStamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                }
    return jsonify(response), 200

# route to get the full chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 201

# route to check if the chain is valid or not
@app.route('/chain_validity', methods = ['GET'])
def chain_validity():
    is_valid = blockchain.chain_validity(blockchain.chain)
    if is_valid:
        response = {'message': 'Your chain is valid'}
        return jsonify(response),200
    else:
        response = {'message': 'Your chain is not valid'}
        return jsonify(response),400


# By making a post request and adding data to the body as json object one can add transaction
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some values are missing in data', 400
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message': f'congratulations!..  Your transaction added to chain successfully.  {index}'}
    return jsonify(response), 200

# connecting all the nodes provided in the list of nodes in body of request
@app.route('/connect_nodes', methods = ['POST'])
def connect_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        response = {'message', 'You do not have any node'}
        return jsonify(response),400
    for node in nodes:
        blockchain.add_nodes(nodes)
    response = {'message': 'All nodes are inserted and connected successfully....',
                'Your nodes are': list(blockchain.nodes)}
    return jsonify(response),200

# check if one's own chain is largest or not
# if not then replace his chain with longest chain
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Congrats!...Your chain is replaced with the longest chain..',
                    'Chain': blockchain.chain}
        return jsonify(response), 200
    else:
        response = {'message': 'Existing chain is itself the longest chain',
                    'Chain': blockchain.chain}
        return jsonify(response), 201

# launching the app on localhost at port number 5000
# one may go to http://127.0.0.1:8000/ or http://localhost:8000/
app.run(host='localhost',port=5000)
