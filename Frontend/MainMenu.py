from consolemenu import *
from consolemenu.items import *

class MainMenu:
    def __init__(self):
        self.menu = ConsoleMenu("GoodChain", "Main Menu")
        selMen = SelectionMenu(["Sign up", "Log in"])
        self.menu.append_item(SubmenuItem("Sign up or log in", selMen, self.menu))
        self.menu.append_item(FunctionItem("Explore the blockchain", print, ["Exploring the blockchain"]))
        # self.menu.append_item(SubmenuItem("Sign up or log in", FunctionItem("Sign up", input, ["Username:"]), FunctionItem("Log in", selMen, self.menu)))

    def show(self):
        self.menu.show()