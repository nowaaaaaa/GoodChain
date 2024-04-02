from Backend.Database import Database
from Frontend.MainMenu import MainMenu

class GoodChain:
    def __init__(self):
        self.database = Database()
        self.menu = MainMenu()

    def run(self):
        self.menu.show()
        self.database.cursor.execute("SELECT * FROM users")
        for user in self.database.cursor:
            print(user)