from Networking import *
import pickle

class TransactionServer(Server):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50000
        Server.__init__(self, HOST, PORT)
    
    def handle_client(self, conn, addr):
        print('Connected by', addr)
        data_length = conn.recv(HEADER_SIZE).decode(DATA_FORMAT)
        if data_length:
            data_length = int(data_length)
        data = conn.recv(data_length)
        transaction = pickle.loads(data)
        conn.send(f'Message received: {data}'.encode(DATA_FORMAT))
        conn.close()
        

class TransactionClient(Client):
    def __init__(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 50001
        Client.__init__(self, HOST, PORT)

    def send_transaction(self, tx):
        tx = pickle.dumps(tx)
        self.send_data(tx)