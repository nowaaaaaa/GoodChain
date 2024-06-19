from Networking import *

class BlockServer(Server):
    def __init__(self, goodChain):
        HOST = socket.gethostbyname('localhost')
        PORT = 50005
        Server.__init__(self, HOST, PORT, goodChain)
    
    def handle_data(self, command, data):
        if command == 'add':
            (block, transactions) = data
            self.goodChain.add_block(block, transactions, False)
        elif command == "remove":
            block = data
            self.goodChain.network_remove_invalid_block(block, False)
        elif command == "remove_invalidated":
            block = data
            self.goodChain.network_remove_invalid_block(block, True)
        elif command == "validate":
            (block_id, public_key, sig) = data
            self.goodChain.add_network_validation(block_id, public_key, sig)
        elif command == "invalidate":
            (block_id, public_key, sig) = data
            self.goodChain.add_network_invalidation(block_id, public_key, sig)

class BlockClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50004
        Client.__init__(self, HOST, PORT)

    def send_add_block(self, block, transactions):
        command = 'add'
        data = (block, transactions)
        self.send_data(command, data)
    
    def send_remove_block(self, block):
        command = 'remove'
        self.send_data(command, block)

    def send_remove_invalidated_block(self, block):
        command = 'remove_invalidated'
        self.send_data(command, block)

    def send_validation(self, block_id, public_key, sig):
        data = (block_id, public_key, sig)
        command = 'validate'
        self.send_data(command, data)
    
    def send_invalidation(self, block_id, public_key, sig):
        data = (block_id, public_key, sig)
        command = 'invalidate'
        self.send_data(command, data)