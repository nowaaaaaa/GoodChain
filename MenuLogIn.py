from Menu import *
from MenuMain import *
from MenuUser import MenuUser
from InputValidation import *

class MenuLogIn(Menu):
    def __init__(self, GoodChain, username = "", password = "", error = ""):
        self.username = username
        self.password = password
        items = ["Username: " + self.username, "Password: " + len(self.password) * '*', "Log in", "Back"]
        functions = [self.set_username, self.set_password, self.log_in, self.back]
        Menu.__init__(self, GoodChain, "Log in" + error, items, functions)

    def set_username(self):
        unfiltered_username = input("Enter your username: ")
        if len(unfiltered_username) > 3 and len(unfiltered_username) < 20:
            self.username = unfiltered_username
            self.reload_menu()
        else:
            self.reload_menu("\nInvalid username")
    
    def set_password(self):
        unfiltered_password = input("Enter your password: ")
        if len(unfiltered_password) > 5 and len(unfiltered_password) <= 20:
            self.password = unfiltered_password
            self.reload_menu()
        else:
            self.reload_menu("\nInvalid password")
        
    def log_in(self):
        user = self.goodChain.database.verify_user(self.username, self.password)
        if user == []:
            self.reload_menu("\nIncorrect username or password")
        else:
            self.goodChain.logIn(user)
            self.goodChain.setMenu(MenuUser(self.goodChain))
    
    def back(self):
        self.goodChain.setMenu(MenuMain(self.goodChain))

    def reload_menu(self, error = ""):
        self.goodChain.setMenu(MenuLogIn(self.goodChain, self.username, self.password, error))


