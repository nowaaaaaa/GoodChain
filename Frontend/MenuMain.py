from Frontend.Menu import *
from Frontend.MenuSignUp import *
from Frontend.MenuLogIn import *
class MenuMain(Menu):
    def __init__(self, goodChain):
        items = [("Sign up", lambda : goodChain.setMenu(MenuSignUp(goodChain))), ("Log in", lambda : goodChain.setMenu(MenuLogIn(goodChain)))]
        # self.menu = Menu("GoodChain Main Menu", items)
        Menu.__init__(self, "GoodChain Main Menu", items)
 