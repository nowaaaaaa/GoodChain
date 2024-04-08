from Menu import Menu

class MenuUser(Menu):
    def __init__(self, GoodChain):
        Menu.__init__(self, GoodChain, "User Menu", ["Log out"], [self.log_out])

    def log_out(self):
        self.goodChain.log_out()
        self.goodChain.setMenu(MenuMain(self.goodChain))

