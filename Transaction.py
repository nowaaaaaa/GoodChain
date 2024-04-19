from Signature import *
from uuid import *

class Transaction:
    ingoing = None
    outputs = None
    sigs = None
    def __init__(self):
        self.outputs = []
        self.sigs = []
        self.id = uuid4()

    def set_input(self, from_addr, amount):
        self.ingoing = (from_addr, amount)

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))
    
    def set_reward(self, amount):
        for output in self.outputs:
            if output[0] == None:
                output = (None, amount)
                return
        self.add_output(None, amount)

    def sign(self, private):
        message = self.__gather()
        newsig = sign(message, private)
        self.sigs.append(newsig)
               
    def is_valid(self):
        total_in = self.ingoing[1]
        total_out = 0
        message = self.__gather()
        if self.ingoing[0] != None and not verify(message, self.sigs[0], self.ingoing[0]):
            return False
        for addr,amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount
        if total_out != total_in:
            return False        
        return True

    def __gather(self):
        data=[]
        data.append(self.ingoing)
        data.append(self.outputs)
        return data
    
    def get_reward(self):
        for addr, amt in self.outputs:
            if addr == None:
                return amt
        return 0

    def __repr__(self):
        result = "INPUT:\n"
        result += str(self.ingoing[1]) + " from " + str(self.ingoing[0]) + "\n"
        result += "OUTPUTS:\n"
        for addr, amt in self.outputs:
            result += str(amt) + " to " + str(addr) + "\n"
        result += "SIGNATURES:\n"
        for s in self.sigs:
            result += str(s) + "\n"
        result += "END"
        return result
    
    def get_net_gain(self, addr):
        net = 0
        for a, amt in self.outputs:
            if a == addr:
                net += amt
        if self.ingoing[0] == addr:
            net -= self.ingoing[1]
        return net
    
    def sig_found(self, addr):
        for sig in self.sigs:
            if verify(self.__gather(), sig, addr):
                return True
        return False

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        if self.ingoing == None and other.ingoing == None and self.outputs == None and other.outputs == None and self.sigs == None and other.sigs == None:
            return True
        if self.ingoing == None or other.ingoing == None or self.outputs == None or other.outputs == None or self.sigs == None or other.sigs == None or self.id == None or other.id == None:
            return False
        if self.ingoing[0] != other.ingoing[0] or self.ingoing[1] != other.ingoing[1]:
            return False
        for i in range(len(self.outputs)):
            if self.outputs[i][0] != other.outputs[i][0] or self.outputs[i][1] != other.outputs[i][1]:
                return False
        for i in range(len(self.sigs)):
            if self.sigs[i] != other.sigs[i]:
                return False
        return self.id == other.id