from Database import *
from User import User
from Menu import Menu
from MenuMain import MenuMain
from Pool import Pool
import pickle

class GoodChain:
    path = '../data/blockchain.dat'
    messages = []
    notifications = []
    user = None

    def __init__(self):
        self.database = Database()
        if self.database.tampered:
            self.notifications.append("Detected database tampering, users removed.")
        self.last_block = None
        self.load_block()
        self.menu = MenuMain(self)

    def run(self):
        while self.menu:
            self.menu.show()

    def log_in(self, user_list):
        self.user = User(user_list)
        if not self.last_block.is_validated():
            self.validate_block(self.last_block.block_id)
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
            return
        for tx in pool.invalid:
            if tx.ingoing[0] == self.user.public_key:
                self.add_message("Invalid transaction removed from pool")
                pool.remove_invalid(tx)
    
    def reward_sign_up(self):
        from Transaction import Transaction
        tx = Transaction()
        tx.set_input(None, 50.0)
        tx.add_output(self.user.public_key, 50.0)
        self.add_to_pool(tx)

    def log_out(self):
        self.user = None
        self.messages = []

    def set_menu(self, menu):
        self.menu = menu
    
    def load_block(self):
        try:
            self.last_block = pickle.load(open(self.path, 'rb'))
            self.remove_invalid_blocks()
            self.save_block()
        except:
            from os.path import exists
            if exists(self.path):
                self.notifications.append("Detected blockchain tampering, all blocks removed.")
                self.remove_invalid_blocks()
                self.save_block()
            return
    
    def save_block(self):
        self.remove_invalid_blocks()
        pickle.dump(self.last_block, open(self.path, 'wb'))
    
    def check_balance(self, public_key, starting_block = None):
        if starting_block == None:
            if self.last_block == None:
                return 0.0
            starting_block = self.last_block
        amount = 0.0 if starting_block.previous_block == None else self.check_balance(public_key, starting_block.previous_block)
        if starting_block.is_validated():
            for tx in starting_block.data:
                amount += tx.get_net_gain(public_key)
        return amount  
    
    def check_unvalidated(self, public_key, starting_block = None):
        if starting_block == None:
            if self.last_block == None:
                return 0.0
            starting_block = self.last_block
        amount = 0.0 if starting_block.previous_block == None else self.check_unvalidated(public_key, starting_block.previous_block)
        if not starting_block.is_validated():
            for tx in starting_block.data:
                amount += tx.get_net_gain(public_key)
        return amount
    
    def check_available(self, public_key):
        return self.check_balance(public_key) - self.check_pool()

    def check_pool(self):
        public_key = self.user.public_key
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        return sum([tx.ingoing[1] for tx in pool.transactions if tx.ingoing[0] == public_key])
    
    def check_pool_incoming(self):
        public_key = self.user.public_key
        amount = 0.0
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        for tx in pool.transactions:
            for addr, amt in tx.outputs:
                if addr == public_key:
                    amount += amt
        return amount
    
    def add_block(self, block):
        if block.previous_block != self.last_block:
            return
        if self.last_block != None:
            self.last_block.next_block = block
        self.last_block = block
    
    def add_to_pool(self, tx):
        from NetTransaction import TransactionClient
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        pool.add_tx(tx)
        pool.save_pool()
        TransactionClient().send_transaction(tx)
    
    def readable_transaction(self, tx):
        result = ""
        for addr, amt in tx.outputs:
            if addr == None:
                continue
            result += f"{amt} to {self.database.get_username(addr)}\n"
        result += f"{tx.ingoing[1]} from {self.database.get_username(tx.ingoing[0])}, reward: {tx.get_reward()}"
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
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        if len(pool.transactions) >= 4:
            from datetime import datetime
            if self.last_block != None and (datetime.now() - self.last_block.mine_time).total_seconds() < 180:
                self.post_message("You must wait at least 3 minutes after the last block was mined.")
                return False
            return True
        self.post_message("There are not enough valid transactions in the pool to mine a block.")
        return False
    
    def get_mandatory_transactions(self):
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        tx, invalid = pool.get_mandatory()
        if invalid > 0:
            self.post_message(f"Removed {invalid} invalid transactions from the pool")
        return tx
    
    def get_optional_transactions(self):
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
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
        if time < 10 or time > 20:
            self.post_message(f"Block mined in {time} seconds, which is not in the accepted range.")
            return
        self.add_block(block)
        self.save_block()
        self.load_block()
        for tx in transactions:
            self.remove_from_pool(tx)
        self.post_message(f"Block successfully mined in {time} seconds.")
    
    def remove_from_pool(self, tx):
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        try:
            pool.transactions.remove(tx)
        except:
            pass
        pool.save_pool()
    
    def replace_in_pool(self, old, new):
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
            return
        if not new.is_valid():
            return
        i = pool.transactions.index(old)
        pool.transactions[i] = new
        pool.save_pool()

    def validate_block(self, id):
        block = self.last_block
        while block != None and block.block_id != id:
            block = block.previous_block
        balance_correct = True
        for tx in block.data:
            if tx.ingoing[0] != None and block.get_user_input(tx.ingoing[0]) > self.check_balance(tx.ingoing[0], block):
                balance_correct = False
                break
        validation_result = block.validate_block(self.user.get_private_key(), self.user.public_key)
        self.save_block()
        if not balance_correct or validation_result == 0:
            self.post_message(f"Could not validate invalid block {block.block_id}.")
            block.sign_inv(self.user.get_private_key(), self.user.public_key)
            self.save_block()
        elif validation_result == 1:
            self.post_message(f"Could not validate block {block.block_id}, already validated by you")
            return None
        elif validation_result == 2:
            return block
        if len(block.inv_sigs) >= 3:
            self.remove_invalidated_block(block.id)
            self.post_message(f"Block {block.block_id} invalidated by 3 users, removed it from blockchain.")
            return None
        self.save_block()
        return block

    def get_last_valid(self):
        block = self.last_block
        while block != None and not block.tamper_check():
            block = block.previous_block
        return block.block_id if block != None else -1
    
    def remove_invalid_blocks(self):
        block = self.last_block
        last_valid = self.get_last_valid()
        if block == None or last_valid == self.last_block.block_id:
            return
        if last_valid == -1:
            self.last_block = None
            self.notifications.append("Detected tampering with the blockchain, all blocks removed.")
            return
        while block.block_id > last_valid and block != None:
            block = block.previous_block
        if block == None:
            self.last_block = None
            self.notifications.append("Detected tampering with the blockchain, all blocks removed.")
            return
        self.last_block = block
        self.last_block.next_block = None
        self.notifications.append(f"Detected tampering with the blockchain, removed blocks after block {last_valid}.")

    def get_pool(self):
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        return pool.transactions
    
    def get_transactions(self, public_key):
        block = self.last_block
        tx = []
        while block != None:
            for t in block.data:
                if t.ingoing[0] == public_key:
                    tx.append(t)
                else:
                    for addr, amt in t.outputs:
                        if addr == public_key:
                            tx.append(t)
                            break
            block = block.previous_block
        return tx
    
    def remove_invalidated_block(self, id):
        block = self.last_block
        while block != None and block.block_id != id:
            block = block.previous_block
        if block == None:
            return
        pool = Pool()
        if pool.tampered:
            self.notifications.append("Detected pool tampering, all transactions removed from pool.")
        tx = block.data.copy()
        for t in pool.transactions:
            if t.is_valid():
                tx.append(t)
            else:
                pool.invalid.append(t)
        pool.transactions = tx
        pool.save_pool()
        self.last_block = block.previous_block
        self.last_block.next_block = None
        self.save_block()
        self.load_block()
        self.post_message(f"Invalid block {id} removed from blockchain")
    
    def count_tx(self):
        block = self.last_block
        count = 0
        while block != None:
            count += len(block.data)
            block = block.previous_block
        return count

    def get_notifications(self):
        res = ""
        for n in self.notifications:
            res += "\n" + n
        self.notifications = []
        return res