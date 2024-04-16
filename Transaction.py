from Signature import *

class Transaction:
    ingoing = None
    outputs = None
    sigs = None
    def __init__(self):
        self.outputs = []
        self.sigs = []

    def set_input(self, from_addr, amount):
        self.ingoing = (from_addr, amount)

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))
    
    def set_reward(self, amount):
        self.add_output((None, amount))

    def sign(self, private):
        message = self.__gather()
        newsig = sign(message, private)
        self.sigs.append(newsig)
               
    def is_valid(self):
        total_in = self.ingoing[1]
        total_out = 0
        message = self.__gather()
        if not verify(message, self.sigs[0], addr) and self.ingoing[0] != None:
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
    
    def give_reward(self, addr):
        for output in self.outputs:
            if output[0] == None:
                output = (addr, output[1])
                break

    def __repr__(self):
        result = "INPUT:\n"
        result += str(amt) + " from " + str(addr) + "\n"
        result += "OUTPUTS:\n"
        for addr, amt in self.outputs:
            result += str(amt) + " to " + str(addr) + "\n"
        result += "SIGNATURES:\n"
        for s in self.sigs:
            result += str(s) + "\n"
        result += "END"
        return result