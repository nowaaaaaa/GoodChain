from Signature import *

class Transaction:
    inputs = None
    outputs =None
    sigs = None
    reqd = None
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = sign(message, private)
        self.sigs.append(newsig)
               
    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        for addr,amount in self.inputs:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False
            total_in = total_in + amount
        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
            if not found:
                return False
        for addr,amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount
        if total_out > total_in:
            return False        
        return True

    def get_sender_output(self):
        if not len(self.inputs) == 1:
            return None
        sender = self.inputs[0]
        output = sum([amount for addr, amount in self.outputs])
        return sender[1] - output

    def __gather(self):
        data=[]
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

    def add_reward(self, amount):
        self.outputs.append((None, amount))
    
    def give_reward(self, addr):
        for output in self.outputs:
            if output[0] == None:
                output = (addr, output[1])
                break

    def __repr__(self):
        result = "INPUTS:\n"
        for addr, amt in self.inputs:
            result += str(amt) + " from " + str(addr) + "\n"
        result += "OUTPUTS:\n"
        for addr, amt in self.outputs:
            result += str(amt) + " to " + str(addr) + "\n"
        result += "EXTRA REQUIRED SIGNATURES:\n"
        for r in self.reqd:
            result += str(r) + "\n"
        result += "SIGNATURES:\n"
        for s in self.sigs:
            result += str(s) + "\n"
        result += "END"
        return result