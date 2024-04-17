from Database import *
from User import User
from Menu import Menu
from MenuMain import MenuMain
from Pool import Pool
import pickle

class GoodChain:
    path = './Data/blockchain.dat'
    messages = []

    def __init__(self):
        self.database = Database()
        self.last_block = None
        self.make_test_blocks()
        self.load_block()
        self.menu = MenuMain(self)

    def make_test_blocks(self):
        from Transaction import Transaction
        tx = Transaction()
        mike = User(self.database.verify_user('mike111', 'mike111'))
        rose = User(self.database.verify_user('rose222', 'rose222'))
        alex = User(self.database.verify_user('alex333', 'alex333'))
        tx.set_input(mike.public_key, 1)
        tx.add_output(rose.public_key, 1)
        tx.sign(mike.get_private_key())
        from Block import Block
        self.add_block(Block([], None))
        self.last_block.add_tx(tx)
        self.last_block.validate_block(mike.get_private_key(), mike.public_key)
        self.last_block.validate_block(rose.get_private_key(), rose.public_key)
        self.last_block.validate_block(alex.get_private_key(), alex.public_key)
        self.add_block(Block([], self.last_block))
        tx = Transaction()
        tx.set_input(rose.public_key, 1)
        tx.add_output(alex.public_key, 1)
        tx.sign(rose.get_private_key())
        self.last_block.add_tx(tx)
        self.last_block.validate_block(mike.get_private_key(), mike.public_key)
        self.last_block.validate_block(rose.get_private_key(), rose.public_key)
        self.last_block.validate_block(alex.get_private_key(), alex.public_key)
        self.save_block()

    def run(self):
        print("Welcome to GoodChain!")
        while self.menu:
            self.menu.show()
        block = self.last_block
        while block:
            for tx in block.data:
                print(self.readable_transaction(tx))
            block = block.previous_block
    
    def log_in(self, user_list):
        self.user = User(user_list)
        pool = Pool()
        for tx in pool.invalid:
            if tx.ingoing[0] == self.user.public_key:
                self.add_message("Invalid transaction removed from pool")
                pool.remove_invalid(tx)
    
    def log_out(self):
        self.user = None
        self.messages = []

    def set_menu(self, menu):
        self.menu = menu
    
    def load_block(self):
        try:
            self.last_block = pickle.load(open(self.path, 'rb'))
        except:
            return
    
    def save_block(self):
        pickle.dump(self.last_block, open(self.path, 'wb'))
    
    def check_available(self, public_key, starting_block = None):
        from Transaction import Transaction
        if starting_block == None:
            if self.last_block == None:
                return 0
            starting_block = self.last_block
        amount = 0 if starting_block.previous_block == None else self.check_available(public_key, starting_block.previous_block)
        if starting_block.is_validated():
            for tx in starting_block.data:
                amount += tx.get_net_gain(public_key)
        return amount     

    def check_pool(self):
        public_key = self.user.public_key
        pool = Pool()
        return sum([tx.ingoing[1] for tx in pool.transactions if tx.ingoing[0] == public_key])
    
    def add_block(self, block):
        if block.previous_block != self.last_block:
            return
        if self.last_block != None:
            self.last_block.next_block = block
        self.last_block = block
    
    def add_to_pool(self, tx):
        pool = Pool()
        pool.add_tx(tx)
        pool.save_pool()
    
    def readable_transaction(self, tx):
        result = ""
        for addr, amt in tx.outputs:
            result += f"{amt} to {self.database.get_username(addr)}"
        result += f"\n{tx.ingoing[1]} from {self.database.get_username(tx.ingoing[0])}"
        return result

    def post_message(self, message):
        self.messages.append(message)
    
    def get_messages(self):
        res = self.messages.copy()
        self.messages = []
        return res
    
    def get_unconfirmed_transactions(self):
        tx = []
        block = self.last_block
        public_key = self.user.public_key
        while block != None:
            if block.is_validated():
                for t in block.data:
                    for addr, amt in t.outputs:
                        if addr == public_key:
                            tx.append(t)
            block = block.previous_block
        return tx