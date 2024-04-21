from Menu import *

class MenuReceive(Menu):
    def __init__(self, goodChain, error = ""):
        title = "Select a transaction to confirm receiving it"
        if error != "":
            title += "\n" + error
        items = []
        functions = []
        for tx in goodChain.get_unconfirmed_transactions():
            items.append(goodChain.readable_transaction(tx))
            functions.append(lambda : self.confirm_transaction(tx))
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)

    def confirm_transaction(self, tx):
        tx.sign(self.goodChain.user.get_private_key())
        self.goodChain.save_block()
        self.reload_menu("Transaction received")
    
    def reload_menu(self, error = ""):
        self.goodChain.set_menu(MenuReceive(self.goodChain, error))
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))