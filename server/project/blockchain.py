import requests
from urllib.parse import urlparse
import datetime
from typing import List
from project.wallet import *
from project.transaction import *
from project.block import *

class Blockchain:
    difficulty = 1
    nodes = set()
    INTEREST=0.01

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        myWallet = Wallet()
        block_reward = Transaction("Block_Reward", myWallet.identity, "5.0").to_json()
        genesis_block = Block(0, block_reward, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block.to_json())
    '''
    def add_new_transaction(self, transaction: Transaction):
        if transaction.verify_transaction_signature():
            self.unconfirmed_transactions.append(transaction.to_json())
            return True
        else:
            return False
    '''
    def add_block(self, block, proof):
        previous_hash = self.last_block['hash']
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block.to_json())
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine(self, myWallet):
        
        #addresses = self.get_addresses_from_transactions()
        # create Transaction objects for interest
        interest_tx = self.create_interest_transactions(myWallet.identity)
        #for interest_tx in interest_txs:
        self.unconfirmed_transactions.insert(0, interest_tx.to_json())
            
        block_reward = Transaction("Block_Reward",
                                   myWallet.identity, "5.0").to_json()

        self.unconfirmed_transactions.insert(0, block_reward)
        if not self.unconfirmed_transactions:
            return False

        new_block = Block(index=self.last_block['index'] + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                          previous_hash=self.last_block['hash'])
                          
                          
        new_block.difficulty = self.next_difficulty(self.last_block)

        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.unconfirmed_transactions = []
            return new_block
        else:
            return False
    
    def create_interest_transactions(self, address) -> Transaction:
        '''check balance of each address and generate interest transaction'''
        #interest_txs = []
        #for address in addresses:
        balance = self.check_balance(address)
        interest = balance * self.INTEREST
        interest_tx = Transaction("Block_Reward", address, str(interest))
        #interest_txs.append(interest_tx)
        return interest_tx

    
    
    def register_node(self, node_url):
        # Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
            
    '''def get_addresses_from_transactions(self) -> List[str]:
        get all addresses by looping through all blocks and transactions
        addresses = set()
        fullchain = [json.loads(block) for block in self.chain]
        #if type(fullchain) == list:
        for block in fullchain:
            for trans in block['transactions']:
                trans = json.loads(trans)
                if trans['sender'] != 'Block_Reward':
                    addresses.add(trans['sender'])
                if trans['recipient'] != 'Block_Reward':
                    addresses.add(trans['recipient'])
                    
        print(addresses)
        return list(addresses)'''

    def consensus(self):
        neighbours = self.nodes
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://' + node + '/fullchain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # Replace our chain if longer chain is found
        if new_chain:
            self.chain = json.loads(new_chain)
            return True
        return False

    def valid_chain(self, chain): #Able to reject malformed blocks
        # check if a blockchain is valid
        current_index = 0
        chain = json.loads(chain)
        while current_index < len(chain):
            block = json.loads(chain[current_index])
            current_block = Block(block['index'],
                            block['transactions'],
                            block['timestamp'],
                            block['previous_hash'],
                            block['hash'],
                            block['nonce'])
            if current_index + 1 < len(chain):
                if current_block.compute_hash() != json.loads(chain[current_index + 1])['previous_hash']:
                    return False
            if isinstance(current_block.transactions, list):
                for transaction in current_block.transactions:
                    transaction = json.loads(transaction)
                    # skip Block reward because it does not have signature
                    if transaction['sender'] == 'Block_Reward':
                        continue
                    current_transaction = Transaction(transaction['sender'],
                                        transaction['recipient'],
                                        transaction['value'],
                                        transaction['signature'])
                    # validate digital signature of each transaction
                    if not current_transaction.verify_transaction_signature():
                        return False
                    if not self.is_valid_proof(current_block, block['hash']):
                        return False
                current_index += 1
            return True

    def check_balance(self, address: str):

        if len(self.chain) <= 0:
            return None

        balance = 0.0

        for block in self.chain:
            current_block = json.loads(block)
            all_transactions = current_block["transactions"]

            if type(all_transactions) == list:
                for current_transaction in all_transactions:
                    current_transaction = eval(current_transaction)
                    if current_transaction["recipient"] == address:
                        balance += float(current_transaction["value"])
                    elif current_transaction["sender"] == address:
                        balance -= float(current_transaction["value"])
                        balance -= float(current_transaction["fee"])
            else:
                current_transaction = eval(all_transactions)
                if current_transaction["recipient"] == address:
                    balance += float(current_transaction["value"])
                elif current_transaction["sender"] == address:
                    balance -= float(current_transaction["value"])
                    balance -= float(current_transaction["fee"])
        for transaction in self.unconfirmed_transactions:
            transaction = json.loads(transaction)
            if transaction["recipient"] == address:
                balance += float(transaction["value"])
            elif transaction["sender"] == address:
                balance -= float(transaction["value"])
                balance -= float(transaction["fee"])
        return balance
        
    def add_new_transaction(self, transaction: Transaction) -> bool:
        if transaction.verify_transaction_signature():
            # Check balance and fee before confirming a transaction
            total_charge = float(transaction.value) + float(transaction.fee)
            if transaction.sender != "Block_Reward" and \
                    self.check_balance(transaction.sender) >= total_charge:
                self.unconfirmed_transactions.append(transaction.to_json())
                return True
        return False
        
    @property
    def last_block(self):
        return json.loads(self.chain[-1])
        
    def next_difficulty(self, last_block):
        '''
        compare the 3rd last node and 1st last node timestamp
        to determine current new block's difficulty
        '''
        difficulty = last_block['difficulty']

        if len(self.chain) > 3:
            recent_blocks = [json.loads(block) for block in self.chain[-3:]]
            timestamps = list(map(lambda x: datetime.datetime.strptime(x["timestamp"], "%m/%d/%Y, %H:%M:%S"),
                                  recent_blocks))
            difference = timestamps[2] - timestamps[0]
            print(difference.seconds)
            # Safe range is 10 <= seconds <= 60
            if difference.total_seconds() < 0.001 and difficulty + 1 <= 10:
                difficulty += 1
            elif difference.total_seconds() > 0.1 and difficulty - 1 >= 1:
                difficulty -= 1

        return difficulty
        
#(NEW)--------------------------------------------------------------------------------------#        
    def hash_sum(self, a, b):
        '''simple method to get sum hash of two strings'''
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    def partialValidation(self, path, target):
        '''
        method to go through all the path with given transaction hash (target)
        and return final merkle root
        '''
        result = target
        for p in path:
            direction = int(p[0])
            h = p[1]

            if direction == 0:
                result = self.hash_sum(h, result)
            else:
                result = self.hash_sum(result, h)
        return result

