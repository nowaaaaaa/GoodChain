from BlockChain import CBlock
from Signature import generate_keys, sign, verify

from Transaction import Tx

class TxBlock (CBlock):

    def __init__(self, previousBlock):
        self.data = []
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def addTx(self, Tx_in):
        self.data.append(Tx_in)

    def is_valid(self):
        if self.previousBlock == None:
            return True
        for transaction in self.data:
            if not transaction.is_valid():
                return False
        return self.previousBlock.computeHash() == self.previousHash and self.previousBlock.is_valid()