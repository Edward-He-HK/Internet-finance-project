from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii
import json
from flask import Flask, jsonify, request


class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.fee = self.transaction_fee()

    def to_dict(self):
        return ({
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value,
            'fee': self.fee
        })

    def add_signature(self, signature):
        self.signature = signature

    def verify_transaction_signature(self):
        if hasattr(self, 'signature'):
            public_key = RSA.importKey(binascii.unhexlify(self.sender))
            verifier = PKCS1_v1_5.new(public_key)
            h = SHA.new(str(self.to_dict()).encode('utf8'))
            return verifier.verify(h, binascii.unhexlify(self.signature))
        else:
            return False

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=False)

    def transaction_fee(self)->str:
        rate = 0.03
        fee = float(self.value) * float(rate)
        fee=str(fee)
        return fee
