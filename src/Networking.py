import socket
import threading
HEADER_SIZE = 64
DATA_FORMAT = 'utf-8'
DISC_MSG = '!END'
RET_MSG = '!VLD'

class Server:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST, self.PORT)

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDR)
            s.listen()
            print(f'Server is listening to {self.ADDR}...')
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"A new connection has been established. Total connections: {threading.activeCount() - 1}")


class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST, self.PORT)

    def send_data(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        try:
            client_socket.connect(self.ADDR)
        except OSError:
            print(f'Error connecting to {self.ADDR}')
            return
        formatted = data
        message_length = len(formatted)
        message_header = str(message_length)
        message_header += ' ' * (HEADER_SIZE - len(message_header))
        message_header = message_header.encode(DATA_FORMAT)
        client_socket.send(message_header)
        client_socket.send(formatted)
        client_socket.close()
    