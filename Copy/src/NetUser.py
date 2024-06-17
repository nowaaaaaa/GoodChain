from Networking import *

class UserServer(Server):
    def __init__(self, goodChain):
        HOST = socket.gethostbyname('localhost')
        PORT = 50003
        Server.__init__(self, HOST, PORT, goodChain)
    
    def handle_data(self, command, data):
        if command == 'add':
            user = data
            self.goodChain.add_network_user(user)
        
class UserClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50002
        Client.__init__(self, HOST, PORT)

    def send_add_user(self, user):
        command = 'add'
        self.send_data(command, user)