from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Signature import *
from datetime import datetime

class Block:

    def __init__(self, data, previous_block):
        self.data = data
        self.previous_block = previous_block
        self.block_id = 0
        if previous_block != None:
            self.previous_hash = previous_block.compute_hash()
            self.block_id = previous_block.block_id + 1
        else:
            self.previous_hash = None
        self.next_block = None
        self.sigs = []
        self.inv_sigs = []
        self.miner = None
        self.mine_time = None
        self.nonce = 0
        self.hash = None

    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previous_hash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        return digest.finalize()

    def mine(self, leading_zeros, public_key):
        from time import time
        start = time()
        computed = self.compute_hash()
        elapsed = 0
        easiness = 0
        while not computed[:leading_zeros] == b'\x00'*leading_zeros or str(computed[leading_zeros]) > chr(ord('0') + easiness):
            self.nonce += 1
            computed = self.compute_hash()
            elapsed = time() - start
            easiness = int(elapsed//(10-elapsed//2) if elapsed < 19.5 else 255)
        end = time()
        self.miner = public_key
        self.mine_time = datetime.now()
        self.hash = self.compute_hash()
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
        if not self.tamper_check():
            return 0
        if self.validated_by(public_key):
            return 1
        self.sigs.append((sign(self.compute_hash(), private_key), public_key))
        return 2
    
    def validated_by(self, public_key):
        for sig, key in self.sigs:
            if key == public_key:
                return True
        for sig, key in self.inv_sigs:
            if key == public_key:
                return True
        return False

    def sign_inv(self, private_key, public_key):
        self.inv_sigs.append((sign(self.compute_hash(), private_key), public_key))

    def is_validated(self):
        count = 0
        for sig, public_key in self.sigs:
            if verify(self.compute_hash(), sig, public_key) and public_key != self.miner:
                count += 1
        return count >= 3
    
    def tamper_check(self):
        return self.hash == self.compute_hash() and self.is_valid()
    
    def get_user_input(self, public_key):
        amount = 0
        for tx in self.data:
            if tx.ingoing[0] == public_key:
                amount += tx.ingoing[1]
        return amount