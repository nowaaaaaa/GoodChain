from Menu import Menu

class MenuUser(Menu):
    def __init__(self, goodChain):
        title = f"Welcome to GoodChain, {goodChain.user.username}.\n You have {goodChain.check_balance()} coins."
        Menu.__init__(self, goodChain, title, ["Log out"], [self.log_out])

    def log_out(self):
        from MenuMain import MenuMain
        self.goodChain.log_out()
        self.goodChain.setMenu(MenuMain(self.goodChain))

