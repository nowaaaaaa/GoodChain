from Menu import Menu
from Transaction import Transaction

class MenuUser(Menu):
    def __init__(self, goodChain):
        title = f"Welcome to GoodChain, {goodChain.user.username}.\n You have {goodChain.check_available(goodChain.user.public_key)} coins available and {goodChain.check_pool()} coins in the pool."
        for message in goodChain.get_messages():
            title += f"\n{message}"
        goodChain.messages = []
        items = ["Make a transaction", "Receive transactions", "Mine a block", "Log out"]
        functions = [self.make_transaction, self.receive_transactions, self.mine_block, self.log_out]
        Menu.__init__(self, goodChain, title, items, functions)

    def make_transaction(self):
        from MenuTransaction import MenuTransaction
        self.goodChain.set_menu(MenuTransaction(self.goodChain))
    
    def receive_transactions(self):
        from MenuReceive import MenuReceive
        self.goodChain.set_menu(MenuReceive(self.goodChain))

    def mine_block(self):
        self.goodChain.set_menu(MenuUser(self.goodChain))
    
    def log_out(self):
        from MenuMain import MenuMain
        self.goodChain.log_out()
        self.goodChain.set_menu(MenuMain(self.goodChain))

