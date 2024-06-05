from Networking import *

class TransactionServer:
    def __init__(self):
        self.HOST = socket.gethostbyname('localhost')
        self.PORT = 50001
        self.ADDR = (self.HOST, self.PORT)

    def start_listening(self):
        with socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDRADDR)
            s.listen()
            print(f'Server is listening to {self.ADDR}...')
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"A new connection has been established. Total connections: {threading.activeCount() - 1}")
    
    def handle_client(self, conn, addr):
        print('Connected by', addr)
        data_length = conn.recv(HEADER_SIZE).decode(DATA_FORMAT)
        if data_length:
            data_length = int(data_length)
        data = conn.recv(data_length).decode(DATA_FORMAT)
        print(f'Received: {data}')
        conn.send(f'Message received: {data}'.encode(DATA_FORMAT))
        conn.close()

class TransactionClient:
    def __init__(self):
        self.HOST = socket.gethostbyname('localhost')
        self.PORT = 50000
        self.ADDR = (self.HOST, self.PORT)
    
    def send_data(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        try:
            client_socket.connect(self.ADDR)
        except OSError:
            print(f'Error connecting to {self.ADDR}')
            return
        formatted = data.encode(DATA_FORMAT)
        message_length = len(formatted)
        message_header = str(message_length)
        message_header += ' ' * (HEADER_SIZE - len(message_header))
        message_header = message_header.encode(DATA_FORMAT)
        client_socket.send(message_header)
        client_socket.send(formatted)
        client_socket.close()
