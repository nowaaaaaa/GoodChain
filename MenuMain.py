from Menu import *
from MenuSignUp import *
from MenuLogIn import *


class MenuMain(Menu):
    def __init__(self, goodChain):
        items = ["Sign Up", "Log In", "Explore the blockchain", "Exit"]
        functions = [self.signUp, self.logIn, self.explore, self.exit]
        Menu.__init__(self, goodChain, "GoodChain Main Menu", items, functions)

    def signUp(self):
        self.goodChain.setMenu(MenuSignUp(self.goodChain))

    def logIn(self):
        self.goodChain.setMenu(MenuLogIn(self.goodChain))

    def explore(self):
        self.goodChain.setMenu(MenuMain(self.goodChain))

    def exit(self):
        self.goodChain.setMenu(None)

        