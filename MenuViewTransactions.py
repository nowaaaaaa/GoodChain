from Menu import *

class MenuViewTransactions(Menu):
    def __init__(self, goodChain):
        title = "Personal transaction History"
        items = []
        functions = []
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)

    def view_transaction(self, tx):
        Menu(self.goodChain, self.goodChain.readable_transaction(tx), ["Back"], [lambda : 0]).show()
        self.reload_menu()
    
    def reload_menu(self):
        self.goodChain.set_menu(MenuViewTransactions(self.goodChain))
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))
    
