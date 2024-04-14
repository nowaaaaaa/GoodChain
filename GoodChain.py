from Database import *
from User import User
from Menu import Menu
from MenuMain import MenuMain
import pickle

class GoodChain:
    path = './Data/blockchain.dat'


    def __init__(self):
        self.database = Database()
        self.last_block = None
        # self.make_test_blocks()
        self.load_block()
        for block in self.last_block.data:
            print(block)
        for block in self.last_block.previousBlock.data:
            print(block)
        # self.menu = MenuMain(self)

    def make_test_blocks(self):
        from Transaction import Transaction
        tx = Transaction()
        tx.add_input('mike111', 1)
        tx.add_output('rose222', 1)
        tx.sign(User(self.database.verify_user('mike111', 'mike111')).get_private_key())
        from Block import Block
        self.add_block(Block([], None))
        self.last_block.add_tx(tx)
        self.add_block(Block([], self.last_block))
        tx = Transaction()
        tx.add_input('rose222', 1)
        tx.add_output('alex333', 1)
        tx.sign(User(self.database.verify_user('rose222', 'rose222')).get_private_key())
        self.last_block.add_tx(tx)
        self.save_block()

    def run(self):
        print("Welcome to GoodChain!")
        while self.menu:
            self.menu.show()
        # self.database.cursor.execute("SELECT * FROM users")
        # for data in self.database.verify_user('mike111', 'mike111'):
        #     print(data)
    
    def logIn(self, user_list):
        self.user = User(user_list)
    
    def log_out(self):
        self.user = None

    def setMenu(self, menu):
        self.menu = menu
    
    def load_block(self):
        try:
            self.last_block = pickle.load(open(self.path, 'rb'))
        except:
            return
    
    def save_block(self):
        pickle.dump(self.last_block, open(self.path, 'wb'))

    def check_balance(self):
        return 0
    
    def add_block(self, block):
        if block.previousBlock != self.last_block:
            return
        if self.last_block != None:
            self.last_block.nextBlock = block
        self.last_block = block