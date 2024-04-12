from Menu import Menu
from Transaction import Transaction

class MenuUser(Menu):
    def __init__(self, goodChain):
        title = f"Welcome to GoodChain, {goodChain.user.username}.\n You have {goodChain.check_balance()} coins."
        Menu.__init__(self, goodChain, title, ["Log out"], [self.log_out])

    def make_transaction(self):
        transaction = Transaction()
        user_in = self.goodChain.user.calculate_balance()

    def log_out(self):
        from MenuMain import MenuMain
        self.goodChain.log_out()
        self.goodChain.setMenu(MenuMain(self.goodChain))

