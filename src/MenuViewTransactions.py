from Menu import *

class MenuViewTransactions(Menu):
    def __init__(self, goodChain):
        title = "Personal transaction History"
        items = []
        functions = []
        for tx in goodChain.get_transactions(goodChain.user.public_key):
            items.append(f"Transaction {tx.id} for {tx.ingoing[1]} coins" + (f" from {goodChain.database.get_username(tx.ingoing[0])}" if tx.ingoing[0] != goodChain.user.public_key else "") + (" (unconfirmed)" if not tx.is_valid() else ""))
            functions.append(lambda tx=tx: self.view_transaction(tx))
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)

    def view_transaction(self, tx):
        Menu(self.goodChain, f"Transaction {tx.id} with {len(tx.sigs)} signatures:\n{self.goodChain.readable_transaction(tx)}", ["Back"], [lambda : 0]).show()
        self.reload_menu()
    
    def reload_menu(self):
        self.goodChain.set_menu(MenuViewTransactions(self.goodChain))
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))
    
