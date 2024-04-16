from Menu import *
from Transaction import Transaction

class MenuTransaction(Menu):
    def __init__(self, goodChain, transaction = None, error = ""):
        if transaction == None:
            self.transaction = Transaction()
        else:
            self.transaction = transaction
        items = []
        functions = []
        for i in range(len(self.transaction.outputs)):
            items.append(f"{goodChain.database.get_username(self.transaction.outputs[i][0])} receives {self.transaction.outputs[i][1]} coins")
            functions.append(lambda : self.remove_output(i))
        title =  "Setting up a transaction, available balance: " + str(self.goodChain.check_available()) + " coins"
        if error != "":
            title += '\n' + error
        items.append("Confirm transaction")
        functions.append(self.confirm_transaction)
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions) 
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.setMenu(MenuUser(self.goodChain))
    
    def confirm_transaction(self):
        output = sum([o[1] for o in self.transaction.outputs])
        if self.goodChain.check_balance() < output:
            self.reload_menu("Insufficient balance")
            return
        self.transaction.set_input(self.goodChain.user.public_key, output)
        self.transaction.sign(self.goodChain.user.get_private_key())
        if not self.transaction.is_valid():
            self.reload_menu("Invalid signature or output")
            return
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Please confirm you want to make this transaction:\n" + self.goodChain.readable_transaction(self.transaction).show())):
            self.goodChain.add_to_pool(self.transaction)
            self.goodChain.add_message("Transaction was added to pool")
            from MenuUser import MenuUser
            self.goodChain.setMenu(MenuUser(self.goodChain))
        else:
            self.reload_menu()

    def remove_output(self, index):
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Are you sure you want to remove this output?").show()):
            self.transaction.outputs.remove[index]
        self.reload_menu()

    def reload_menu(self, error = ""):
        self.goodChain.setMenu(MenuTransaction(self.goodChain, self.transaction, error))
    