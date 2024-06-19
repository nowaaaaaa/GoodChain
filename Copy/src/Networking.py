import socket
import threading
import pickle
from Chain import GoodChain

class Header:
    HEADER_SIZE = 256
    def __init__(self, data_length, command):
        self.data_length = data_length
        self.command = command
    
class Server:
    def __init__(self, host, port, goodChain):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST, self.PORT)
        self.goodChain = goodChain
        self.listen = True

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.ADDR)
            s.listen()
            while self.listen:
                conn, addr = s.accept()
                if not self.listen:
                    break
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
    
    def stop_listening(self):
        self.listen = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.ADDR)
        sock.close()
    
    def handle_client(self, conn, addr):
        header = pickle.loads(conn.recv(Header.HEADER_SIZE))
        if not isinstance(header, Header):
            conn.close()
            return
        data_length = header.data_length
        command = header.command
        received_data = conn.recv(data_length)
        data = pickle.loads(received_data)
        conn.close()
        self.handle_data(command, data)

class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.ADDR = (self.HOST, self.PORT)

    def send_data(self, command, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        try:
            client_socket.connect(self.ADDR)
        except OSError:
            print(f'Error connecting to {self.ADDR}')
            return
        formatted_data = pickle.dumps(data)
        header = Header(len(formatted_data), command)
        print(data) # NIET VERWIJDEREN/DON'T REMOVE - ALL NETWORKING CODE WILL BREAK OTHERWISE
        print(formatted_data)
        formatted_header = pickle.dumps(header)
        client_socket.send(formatted_header)
        client_socket.send(formatted_data)
        client_socket.close()
    