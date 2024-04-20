import pickle
class Pool:
    path = 'Data/pool.dat'
    
    def __init__(self):
        self.transactions = []
        self.invalid = []
        self.load_pool()

    def load_pool(self):
        try:
            with open(self.path, 'rb') as f:
                self.transactions = pickle.load(f)
                self.invalid = pickle.load(f)
        except:
            return
    
    def save_pool(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.transactions, f)
            pickle.dump(self.invalid, f)

    def add_tx(self, tx):
        self.transactions.append(tx)
        self.save_pool()
    
    def get_mandatory(self):
        result = []
        valid = 4
        invalid = 0
        for tx in self.transactions:
            if tx.is_valid():
                result.append(tx)
                valid -= 1
                if valid == 0:
                    break
            else:
                self.invalid.append(tx)
                self.transactions.remove(tx)
                self.save_pool()
                invalid += 1
        return result, invalid
    
    def get_optional(self):
        tx = self.transactions[4:]
        res = []
        for t in tx:
            if t.is_valid():
                res.append(t)
            else:
                self.transactions.remove(t)
                self.invalid.append(t)
                self.save_pool()
        return res, len(tx) - len(res)
    
    def remove_invalid(self, tx):
        self.invalid.remove(tx)
        self.save_pool()

