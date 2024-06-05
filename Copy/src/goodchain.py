from Chain import *

if __name__ == '__main__':
    app = GoodChain()
    from NetTransaction import TransactionServer
    server = TransactionServer(app)
    import threading
    server_thread = threading.Thread(target=server.start_listening)
    server.start_listening()
