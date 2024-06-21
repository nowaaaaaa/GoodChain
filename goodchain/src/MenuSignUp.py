from Menu import *
from MenuUser import MenuUser
from InputValidation import *

class MenuSignUp(Menu):
    def __init__(self, goodChain, username = "", password = "", error = ""):
        self.username = username
        self.password = password
        items = ["Username: " + self.username, "Password: " + len(self.password) * '*', "Sign up", "Back"]
        functions = [self.set_username, self.set_password, self.sign_up, self.back]
        Menu.__init__(self, goodChain, "Sign up" + error, items, functions)

    def set_username(self):
        unfiltered_username = input("Enter your username: ")
        if validate_username(unfiltered_username):
            if self.goodChain.database.user_exists(unfiltered_username):
                self.reload_menu("\nUsername already exists")
                return
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
        self.goodChain.sign_up(self.username, self.password)
        self.goodChain.set_menu(MenuUser(self.goodChain))
    
    def back(self):
        from MenuMain import MenuMain
        self.goodChain.set_menu(MenuMain(self.goodChain))

    def reload_menu(self, error = ""):
        self.goodChain.set_menu(MenuSignUp(self.goodChain, self.username, self.password, error))