from Database import *
from User import User
from Menu import Menu
from MenuMain import MenuMain

class GoodChain:
    def __init__(self):
        self.database = Database()
        self.menu = MenuMain(self)

    def run(self):
        print("Welcome to GoodChain!")
        while self.menu:
            self.menu.show()
        # self.database.cursor.execute("SELECT * FROM users")
        # for data in self.database.verify_user('mike111', 'mike111'):
        #     print(data)
    
    def logIn(self, user):
        self.user = User(user[0], user[1], user[2], user[3])
    
    def log_out(self):
        self.user = None

    def setMenu(self, menu):
        self.menu = menu
    
    def check_balance(self):
        return 0