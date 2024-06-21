from Networking import *

class TransactionServer(Server):
    def __init__(self, goodChain):
        HOST = socket.gethostbyname('localhost')
        PORT = 50000
        Server.__init__(self, HOST, PORT, goodChain)
    
    def handle_data(self, command, data):
        if command == 'add':
            transaction = data
            self.goodChain.add_to_pool(transaction, False)
        elif command == "replace":
            old, new = data
            self.goodChain.replace_in_pool(old, new, False)
        elif command == "remove":
            transaction = data
            self.goodChain.remove_from_pool(transaction, False)

class TransactionClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50001
        Client.__init__(self, HOST, PORT)

    def send_add_transaction(self, tx):
        command = 'add'
        self.send_data(command, tx)
    
    def send_replace_transaction(self, old, new):
        data = (old, new)
        command = 'replace'
        self.send_data(command, data)
    
    def send_remove_transaction(self, tx):
        command = 'remove'
        self.send_data(command, tx)