from Networking import *

HOST = socket.gethostbyname('localhost')
PORT = 50007
ADDR = (HOST, PORT)
class TransactionServer:
    def start_listening(self):
        with socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDR)
            s.listen()
            print(f'Server is listening to {ADDR}...')
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                print(f"A new connection has been established. Total connections: {threading.activeCount() - 1}")
    
    def handle_client(self, conn, addr):