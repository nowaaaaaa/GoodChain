from Backend.Database import Database
from Frontend.MainMenu import MainMenu
from Backend.User import User
from Frontend.MenuMain import MenuMain

class GoodChain:
    def __init__(self):
        self.database = Database()
        self.menu = MenuMain(self)

    def run(self):
        self.menu.show()
        # self.database.cursor.execute("SELECT * FROM users")
        # for data in self.database.verify_user('mike111', 'mike111'):
        #     print(data)
    
    def logIn(self, username, password):
        user = self.database.verify_user(username, password)
        self.user = User(user[0], user[1], user[2], user[3])
    
    def setMenu(self, menu):
        self.menu = menu