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
        self.miner = None
        self.mine_time = None
        self.nonce = 0


    def compute_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previous_hash),'utf8'))
        digest.update(bytes(str(self.nonce),'utf8'))
        return digest.finalize()

# 3 = Min time: 10.49948763847351, Max time: 177.64776468276978, Average time: 89.72544753551483
# 2, 1000000 = Min time: 10.516226768493652, Max time: 16.234838247299194, Average time: 14.786657094955444
# 2, 300000 = Min time: 5.411425352096558, Max time: 22.437660455703735, Average time: 12.940696859359742
# 2, 1000000 (+1) = Min time: 4.336809873580933, Max time: 16.184622764587402, Average time: 11.672398400306701
# 2, 1300000 (+1) = Min time: 4.279385328292847, Max time: 18.343408823013306, Average time: 14.090123772621155
    def mine(self, leading_zeros, public_key):
        from time import time
        start = time()
        computed = self.compute_hash()
        while not computed[:leading_zeros] == b'\x00'*leading_zeros or str(computed[leading_zeros]) > chr(ord('0')+(self.nonce//400000)):
            self.nonce += 1
            computed = self.compute_hash()
        end = time()
        print(f"Block mined: {str(computed[leading_zeros])} {chr(ord('0')+(self.nonce//400000))} {self.nonce} {self.compute_hash()}")
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
        if self.validated_by(public_key):
            return False
        if self.is_valid():
            self.sigs.append((sign(self.compute_hash(), private_key), public_key))
            return True
    
    def validated_by(self, public_key):
        for sig, key in self.sigs:
            if key == public_key:
                return True
        return False

    def is_validated(self):
        count = 0
        for sig, public_key in self.sigs:
            if verify(self.compute_hash(), sig, public_key) and public_key != self.miner:
                count += 1
        return count >= 3