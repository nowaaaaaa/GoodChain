import socket

class Server:

    HOST = socket.gethostbyname('localhost')
    PORT = 50007
    ADDR = (HOST, PORT)
    HEADER_SIZE = 64
    DATA_FORMAT = 'utf-8'
    DISC_MSG = '!END'
    RET_MSG = 'Server received your message!'