from Frontend.Menu import *

class MenuSignUp:
    def __init__(self, GoodChain):
        self.GoodChain = GoodChain
        self.menu = Menu("Sign up", ["Username: ", "Password: ", "Sign up"])
        self.menu.show()
        username = self.menu.items[0]
        password = self.menu.items[1]
        # self.GoodChain.sign_up(username, password)
    
