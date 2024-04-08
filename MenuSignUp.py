from Menu import *
from MenuMain import *
from MenuUser import MenuUser
from InputValidation import *

class MenuSignUp(Menu):
    def __init__(self, GoodChain, username = "", password = "", error = ""):
        self.username = username
        self.password = password
        items = ["Username: " + self.username, "Password: " + len(self.password) * '*', "Sign up", "Back"]
        functions = [self.set_username, self.set_password, self.sign_up, self.back]
        Menu.__init__(self, GoodChain, "Sign up" + error, items, functions)

    def set_username(self):
        unfiltered_username = input("Enter your username: ")
        if validate_username(unfiltered_username):
            self.username = unfiltered_username
            self.reload_menu()
        else:
            self.reload_menu("\nPlease enter a valid username")
    
    def set_password(self):
        unfiltered_password = input("Enter your password: ")
        if validate_password(unfiltered_password):
            self.password = unfiltered_password
            self.reload_menu()
        else:
            self.reload_menu("\nPlease enter a valid password")
        
    def sign_up(self):
        if (self.username == "" or self.password == ""):
            self.reload_menu("\nPlease enter a valid username and password")
            return
        self.goodChain.database.add_user(self.username, self.password)
        self.goodChain.logIn(self.goodChain.database.verify_user(self.username, self.password))
        self.goodChain.setMenu(MenuUser(self.goodChain))
    
    def back(self):
        self.goodChain.setMenu(MenuMain(self.goodChain))

    def reload_menu(self, error = ""):
        self.goodChain.setMenu(MenuSignUp(self.goodChain, self.username, self.password, error))