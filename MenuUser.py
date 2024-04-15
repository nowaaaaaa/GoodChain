from Menu import Menu
from Transaction import Transaction

class MenuUser(Menu):
    def __init__(self, goodChain):
        title = f"Welcome to GoodChain, {goodChain.user.username}.\n You have {goodChain.check_balance()} coins."
        items = ["Make a transaction", "Mine a block", "Log out"]
        functions = [self.make_transaction, self.log_out]
        Menu.__init__(self, goodChain, title, items, functions)

    def make_transaction(self):
        transaction = Transaction()
        transaction.set_input(self.goodChain.user.public_key, self.goodChain.check_balance())

    def log_out(self):
        from MenuMain import MenuMain
        self.goodChain.log_out()
        self.goodChain.setMenu(MenuMain(self.goodChain))

