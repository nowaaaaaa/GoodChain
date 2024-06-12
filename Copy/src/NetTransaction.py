from Networking import *

class TransactionServer(Server):
    def __init__(self, goodChain):
        HOST = socket.gethostbyname('localhost')
        PORT = 50001
        Server.__init__(self, HOST, PORT, goodChain)
    
    def handle_data(self, command, data):
        if command == 'add':
            transaction = pickle.loads(data)
            self.goodChain.add_to_pool(transaction, False)
        elif command == "replace":
            old, new = pickle.loads(data)
            self.goodChain.replace_in_pool(old, new, False)
        elif command == "remove":
            transaction = pickle.loads(data)
            self.goodChain.remove_from_pool(transaction, False)
        

class TransactionClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50000
        Client.__init__(self, HOST, PORT)

    def send_add_transaction(self, tx):
        tx = pickle.dumps(tx)
        header = pickle.dumps(Header(len(tx), 'add'))
        self.send_data(header, tx)
    
    def send_replace_transaction(self, old, new):
        data = pickle.dumps((old, new))
        header = pickle.dumps(Header(len(data), 'replace'))
        self.send_data(header, data)
    
    def send_remove_transaction(self, tx):
        tx = pickle.dumps(tx)
        header = pickle.dumps(Header(len(tx), 'remove'))
        self.send_data(header, tx)