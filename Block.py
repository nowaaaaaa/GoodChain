from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Signature import *
from datetime import datetime

class Block:

    data = []
    previous_hash = None
    previous_block = None
    next_block = None
    sigs = []
    miner = None
    mine_time = None
    nonce = 0

    def __init__(self, data, previous_block):
        self.data = data
        self.previous_block = previous_block
        if previous_block != None:
            self.previous_hash = previous_block.compute_hash()
    
    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previous_hash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        return digest.finalize()

    def mine(self, leading_zeros, public_key):
        from time import time
        start = time()
        while not self.compute_hash()[:leading_zeros] == b'\x00'*leading_zeros:
            self.nonce += 1
        end = time()
        self.miner = public_key
        self.mine_time = datetime.now()
        return end - start

    def is_valid(self):
        if not self.verify_reward():
            return False
        if self.previous_block == None:
            return True
        for transaction in self.data:
            if not transaction.is_valid():
                return False
        return self.previous_block.compute_hash() == self.previous_hash and self.previous_block.is_valid()
    
    def verify_reward(self):
        reward = 50
        actual = 0
        for tx in self.data:
            if tx.ingoing[0] == None:
                actual = tx.ingoing[1]
            reward += tx.get_reward()
        return reward == actual

    def add_tx(self, transaction):
        self.data.append(transaction)
    
    def validate_block(self, private_key, public_key):
        if self.is_valid():
            self.sigs.append((sign(self.compute_hash(), private_key), public_key))
            return True
    
    def is_validated(self):
        count = 0
        for sig, public_key in self.sigs:
            if verify(self.compute_hash(), sig, public_key) and public_key != self.miner:
                count += 1
        return count >= 3