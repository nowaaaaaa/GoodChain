from Database import *
from User import User
from Menu import Menu
from MenuMain import MenuMain
from Pool import Pool
import pickle

class GoodChain:
    path = './Data/blockchain.dat'
    messages = []
    user = None

    def __init__(self):
        self.database = Database()
        self.last_block = None
        # self.make_test_blocks()
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
    
    # 300000, 5 tx = Min time: 14.040112495422363, Max time: 38.65707063674927, Average time: 25.442252230644225
    # 150000, 5 Min time: 9.904855966567993, Max time: 22.739466905593872, Average time: 13.560591292381286
    # 150000, 10 Min time: 18.764503002166748, Max time: 45.773133754730225, Average time: 27.044932866096495
    def test_mining(self):
        from Transaction import Transaction
        from Block import Block
        n = 10
        min_time = 10000
        max_time = -1
        times = []
        user1 = User(self.database.verify_user('mike111', 'mike111'))
        user2 = User(self.database.verify_user('rose222', 'rose222'))
        user3 = User(self.database.verify_user('alex333', 'alex333'))
        for i in range(n):
            transactions = []
            for j in range(10):
                tx = Transaction()
                tx.set_input(user1.public_key, i+1)
                tx.add_output(user2.public_key, i+1)
                tx.sign(user1.get_private_key())
                transactions.append(tx)
            times.append(Block(transactions, self.last_block).mine(2, user3.public_key))
            if times[i] < min_time:
                min_time = times[i]
            if times[i] > max_time:
                max_time = times[i]
        print(f"Min time: {min_time}, Max time: {max_time}, Average time: {sum(times)/n}")

    def run(self):
        # while self.menu:
        #     self.menu.show()
        self.test_mining()
    
    def log_in(self, user_list):
        self.user = User(user_list)
        pool = Pool()
        for tx in pool.invalid:
            if tx.ingoing[0] == self.user.public_key:
                self.add_message("Invalid transaction removed from pool")
                pool.remove_invalid(tx)
    
    def reward_sign_up(self):
        from Transaction import Transaction
        tx = Transaction()
        tx.set_input(None, 50)
        tx.add_output(self.user.public_key, 50)
        self.add_to_pool(tx)

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
    
    def check_balance(self, public_key, starting_block = None):
        from Transaction import Transaction
        if starting_block == None:
            if self.last_block == None:
                return 0
            starting_block = self.last_block
        amount = 0 if starting_block.previous_block == None else self.check_balance(public_key, starting_block.previous_block)
        if starting_block.is_validated():
            for tx in starting_block.data:
                amount += tx.get_net_gain(public_key)
        return amount  
    
    def check_available(self, public_key):
        return self.check_balance(public_key) - self.check_pool()

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
    
    def can_mine(self):
        if self.last_block != None and not self.last_block.is_validated():
            self.post_message("The last block has not yet been validated.")
            return False
        if len(Pool().transactions) >= 4:
            from datetime import datetime
            if self.last_block != None and (datetime.now() - self.last_block.mine_time).total_seconds() < 180:
                self.post_message("You must wait at least 3 minutes after the last block was mined.")
                return False
            return True
        self.post_message("There are not enough valid transactions in the pool to mine a block.")
        return False
    
    def get_mandatory_transactions(self):
        pool = Pool()
        tx, invalid = pool.get_mandatory()
        if invalid > 0:
            self.post_message(f"Removed {invalid} invalid transactions from the pool")
        return tx
    
    def get_optional_transactions(self):
        pool = Pool()
        tx, invalid = pool.get_optional()
        if invalid > 0:
            self.post_message(f"Removed {invalid} invalid transactions from the pool")
        return tx

    def mine_block(self, transactions):
        from Block import Block
        from Transaction import Transaction
        block = Block(transactions, self.last_block)
        reward_tx = Transaction()
        reward_amt = 50
        for tx in transactions:
            reward_amt += tx.get_reward()
        reward_tx.set_input(None, reward_amt)
        reward_tx.add_output(self.user.public_key, reward_amt)
        block.add_tx(reward_tx)
        if not block.is_valid():
            self.post_message("Tried to mine an invalid block.")
            return
        time = block.mine(2, self.user.public_key)
        self.add_block(block)
        self.save_block()
        self.load_block()
        for tx in transactions:
            self.remove_from_pool(tx)
        self.post_message(f"Block successfully mined in {time} seconds.")
    
    def remove_from_pool(self, tx):
        pool = Pool()
        try:
            pool.transactions.remove(tx)
        except:
            pass
        pool.save_pool()
    
    def validate_block(self, id):
        block = self.last_block
        while block != None and block.block_id != id:
            block = block.previous_block
        block.validate_block(self.user.get_private_key(), self.user.public_key)
        for s in self.last_block.sigs:
            print(s[1])
        self.save_block()
        self.load_block()
        for s in self.last_block.sigs:
            print(s[1])
        while block != None and block.block_id != id:
            block = block.previous_block
        return block