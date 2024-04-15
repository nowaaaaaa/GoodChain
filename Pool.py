import pickle
class Pool:
    path = 'Data/pool.dat'
    
    def __init__(self):
        self.transactions = []
        self.invalid = []
        self.load_pool()

    # def load_pool(self):
    #     try:
    #         self.transactions = pickle.load(open(self.path, 'rb'))
    #     except:
    #         return
    
    # def save_pool(self):
    #     pickle.dump(self.transactions, open(self.path, 'wb'))

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
                invalid += 1
        return result, invalid

