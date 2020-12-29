import json
from hashlib import sha256

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, hashs=None, nonce=0,difficulty=1):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = hashs
        self.nonce = nonce
        self.difficulty = difficulty
        self.merkle_root = ""

    def to_dict(self):
        return ({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'difficulty': self.difficulty,
            'merkle_root': self.merkle_root}
        )

    def to_json(self):
        return json.dumps(self.__dict__)

    def compute_hash(self):
        self.merkle_root = self.compute_merkle_root()
        payload = str(self.to_dict()).encode()
        return sha256(payload).hexdigest()
        
#(Add)-------------------------------------------------------------------------#
    def compute_merkle_root(self):
        '''method to return merkle root of all transaction in this block'''
        transactionHashes = self.transactionHashes(self.transactions)
        root = self.merkleRoot(transactionHashes)
        return root

    def hash_sum(self, a, b):
        '''simple method to get sum hash of two strings'''
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    def transactionHashes(self, transactions):
        '''method to return hashed string from given list of transaction strings'''
        return [sha256(str(transaction).encode()).hexdigest() for transaction in transactions]

    def merkleRoot(self, leaves):
        '''recursive method to calculate merkle root'''
        if len(leaves) <= 1:
            return leaves[0]

        roots = []
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index + 1] if index + 1 < len(leaves) else leaves[index]
            root = self.hash_sum(a, b)
            roots.append(root)
            index += 2

        return self.merkleRoot(roots)

