from Backend.Database import Database
from Frontend.MainMenu import MainMenu

class GoodChain:
    def __init__(self):
        self.database = Database()
        self.menu = MainMenu()

    def run(self):
        self.menu.show()
        self.database.cursor.execute("SELECT * FROM users")
        for data in self.database.verify_user('mike111', 'mike111'):
            print(data)