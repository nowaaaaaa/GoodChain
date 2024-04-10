from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class CBlock:

    data = None
    previousHash = None
    previousBlock = None
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()
    
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf8'))
        digest.update(bytes(str(self.previousHash),'utf8'))
        return digest.finalize()

    # def mine(self, leading_zeros):
    #     while not self.computeHash()[:leading_zeros] == b'\x00'*leading_zeros:
    #         self.nonce += 1
    #     self.hash = self.computeHash()

    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash and self.previousBlock.is_valid()