from Networking import *

class UserServer(Server):
    def __init__(self, goodChain):
        HOST = socket.gethostbyname('localhost')
        PORT = 50002
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

class UserClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50003
        Client.__init__(self, HOST, PORT)

    def send_add_user(self, user):
        command = 'add'
        self.send_data(command, user)