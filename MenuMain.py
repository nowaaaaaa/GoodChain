from Menu import *
from MenuSignUp import *
from MenuLogIn import *
from MenuExplore import *

class MenuMain(Menu):
    def __init__(self, goodChain):
        items = ["Sign Up", "Log In", "Explore the blockchain", "Exit"]
        functions = [self.sign_up, self.log_in, self.explore, self.exit]
        Menu.__init__(self, goodChain, "GoodChain Main Menu", items, functions)

    def sign_up(self):
        self.goodChain.set_menu(MenuSignUp(self.goodChain))

    def log_in(self):
        self.goodChain.set_menu(MenuLogIn(self.goodChain))

    def explore(self):
        self.goodChain.set_menu(MenuExplore(self.goodChain))

    def exit(self):
        self.goodChain.set_menu(None)

        