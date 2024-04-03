from Frontend.Menu import *

class MenuLogIn:
    def __init__(self, GoodChain):
        self.GoodChain = GoodChain
        self.menu = Menu("Log in", ["Username: ", "Password: ", "Log in"])
        self.menu.show()
        username = self.menu.items[0]
        password = self.menu.items[1]
        self.GoodChain.log_in(username, password)
    
    def inputUserCredentials():
        username = input("Username: ")
        password = input("Password: ")
        return username, password