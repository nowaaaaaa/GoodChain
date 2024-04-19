from Menu import *
from colorama import Fore, Back, Style

class MenuMine(Menu):
    def __init__(self, goodChain, transactions = [], error = ""):
        self.goodChain = goodChain
        if transactions == []:
            transactions = goodChain.get_mandatory_transactions()
            if len(transactions) < 4:
                self.back()
                return
        self.transactions = transactions
        title = f"Select transactions to include in the block\n Current reward: {self.get_total_reward()} coins{error}" 
        items = []
        functions = []
        for tx in goodChain.get_optional_transactions():
            if tx in self.transactions:
                items.append(Fore.GREEN + self.display_transaction(tx) + Style.RESET_ALL)
            else:
                items.append(self.display_transaction(tx))
            functions.append(lambda tx=tx : self.toggle_transaction(tx))
        items.append("Mine block")
        functions.append(self.mine_block)
        items.append("Back")
        functions.append(self.back)
        # for tx in self.transactions:
        #     if tx in self.transactions:
        #         items.append(Fore.GREEN + self.display_transaction(tx) + Style.RESET_ALL)
        #     else:
        #         items.append(self.display_transaction(tx))            
        #     functions.append(lambda tx=tx : self.toggle_transaction(tx))
        Menu.__init__(self, goodChain, title, items, functions)

    def toggle_transaction(self, tx):
        if tx in self.transactions:
            self.transactions.remove(tx)
        else:
            if len(self.transactions) >= 9:
                self.reload_menu("\nCannot add more than 10 transactions to a block")
                return
            self.transactions.append(tx)
        self.reload_menu()
        
    def mine_block(self):
        from MenuConfirm import MenuConfirm
        confirm_title = "Are you sure you want to mine this block?"
        for tx in self.transactions:
            confirm_title += f"\n{self.display_transaction(tx)}"
        if not MenuConfirm(confirm_title).show():
            self.reload_menu()
            return
        self.goodChain.mine_block(self.transactions)
        self.back()
    
    def get_total_reward(self):
        total = 50
        for tx in self.transactions:
            total += tx.get_reward()
        return total
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))

    def display_transaction(self, tx):
        return f"{tx.ingoing[1]} from {self.goodChain.database.get_username(tx.ingoing[0])} to {self.goodChain.database.get_username(tx.outputs[0][0])}, reward: {tx.get_reward()}"
    
    def reload_menu(self, error = ""):
        self.goodChain.set_menu(MenuMine(self.goodChain, self.transactions, error))