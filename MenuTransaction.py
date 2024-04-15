from Menu import *
from Transaction import Transaction

class MenuTransaction(Menu):
    def __init__(self, goodChain, transaction = None, error = ""):
        if transaction == None:
            self.transaction = Transaction()
            self.transaction.set_input(goodChain.user.public_key, goodChain.check_balance())
        else:
            self.transaction = transaction
        items = []
        functions = []
        for i in range(len(self.transaction.outputs)):
            items.append(f"{self.goodChain.database.get_username(self.transaction.outputs[i][0])} receives {self.transaction.outputs[i][1]} coins")
            functions.append(lambda : self.remove_output(i))
        title =  "Setting up a transaction"
        if error != "":
            title += '\n' + error
        Menu.__init__(self, goodChain, title, items, functions) 
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.setMenu(MenuUser(self.goodChain))
    
    def remove_output(self, index):
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Are you sure you want to remove this output?").show()):
            self.transaction.outputs.remove[index]
        self.reload_menu()

    def reload_menu(self):
        self.goodChain.setMenu(MenuTransaction(self.goodChain, self.transaction))
    