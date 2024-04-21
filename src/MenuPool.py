from Menu import Menu
from MenuTransaction import MenuTransaction
from Transaction import is_float

class MenuPool(Menu):
    def __init__(self, goodChain, error = ""):
        title = "Viewing transaction pool" + error
        items = []
        functions = []
        transactions = goodChain.get_pool()
        self.goodChain = goodChain
        for tx in transactions:
            items.append(self.display_transaction(tx))
            functions.append(lambda tx=tx : self.view_transaction(tx))
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)
    
    def view_transaction(self, tx):
        if MenuViewTransaction(self.goodChain, tx).show():
            self.reload_menu("\nTransaction in pool edited")
        else:
            self.reload_menu()
    
    def reload_menu(self, error = ""):
        self.goodChain.set_menu(MenuPool(self.goodChain, error))

    def display_transaction(self, tx):
        return f"Transaction {tx.id} by {self.goodChain.database.get_username(tx.ingoing[0])}"
    
    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))

class MenuViewTransaction(Menu):
    def __init__(self, goodChain, transaction):
        title = f"Transaction {transaction.id}:\n{goodChain.readable_transaction(transaction)}"
        items = []
        functions = []
        self.transaction = transaction
        if goodChain.user != None and transaction.ingoing[0] == goodChain.user.public_key:
            items.append("Edit transaction")
            functions.append(lambda : self.edit_transaction())
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)
    
    def edit_transaction(self):
        replace, new_tx = MenuEditTransaction(self.goodChain, self.transaction).show()
        if replace:
            if new_tx == None:
                self.goodChain.remove_from_pool(self.transaction)
            else:
                self.goodChain.replace_in_pool(self.transaction, new_tx)
            return True    
        return False
    
    def back(self):
        return False

class MenuEditTransaction(Menu):
    def __init__(self, goodChain, old_transaction, transaction = None, error = ""):
        items = []
        functions = []
        if transaction == None:
            from Transaction import Transaction
            self.transaction = Transaction()
            self.transaction.set_input(old_transaction.ingoing[0], old_transaction.ingoing[1])
            for o in old_transaction.outputs:
                self.transaction.add_output(o[0], o[1])
            self.transaction.set_reward(old_transaction.get_reward())
            self.transaction.id = old_transaction.id
        else:
            self.transaction = transaction
        self.old_transaction = old_transaction
        self.available = goodChain.check_available(goodChain.user.public_key) + old_transaction.ingoing[1]
        for i in range(len(self.transaction.outputs)):
            if self.transaction.outputs[i][0] == None:
                continue
            items.append(f"{goodChain.database.get_username(self.transaction.outputs[i][0])} receives {self.transaction.outputs[i][1]} coins")
            functions.append(lambda i=i : self.remove_output(i))
        title =  "Editing up a transaction, available balance: " + str(self.available) + " coins"
        if error != "":
            title += '\n' + error
        items.append("Add output")
        functions.append(self.add_output)
        items.append("Set mining reward, currently: " + str(self.transaction.get_reward()) + " coins")
        functions.append(self.set_reward)
        items.append("Confirm transaction")
        functions.append(self.confirm_transaction)
        items.append("Remove transaction")
        functions.append(self.remove_transaction)
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions) 

    def add_output(self):
        raw_addr = input("Enter the address or username of the recipient: ")
        addr = None
        username = None
        if self.goodChain.user.username == raw_addr or self.goodChain.user.public_key == raw_addr:
            return self.reload_menu("Cannot send to yourself")
        if self.goodChain.database.get_username(raw_addr) == None:
            if self.goodChain.database.get_public_key(raw_addr) == None:
                return self.reload_menu("Invalid address or username")
            else:
                addr = self.goodChain.database.get_public_key(raw_addr)
                username = raw_addr
        else:
            addr = raw_addr
            username = self.goodChain.database.get_username(raw_addr)
        amount = input(f"Enter the amount to send to {username}: ")
        if not is_float(amount) or float(amount) <= 0 or self.goodChain.check_available(self.goodChain.user.public_key) < self.get_total_output() + float(amount):
            return self.reload_menu("Invalid amount entered")
        self.transaction.add_output(addr, float(amount))
        return self.reload_menu()

    def set_reward(self):
        amount = input(f"Enter mining reward amount: ")
        if not is_float(amount) or self.available < self.get_total_output() + float(amount) or float(amount) < 0.0:
            return self.reload_menu("Invalid amount entered")
        self.transaction.set_reward(float(amount))
        return self.reload_menu()

    def back(self):
        return False, None
    
    def confirm_transaction(self):
        if len(self.transaction.outputs) <= 0:
            return self.reload_menu("No outputs specified")
        output = sum([o[1] for o in self.transaction.outputs])
        if self.available < output:
            return self.reload_menu("Insufficient balance")
        self.transaction.set_input(self.goodChain.user.public_key, output)
        self.transaction.sign(self.goodChain.user.get_private_key())
        if not self.transaction.is_valid():
            return self.reload_menu("Invalid signature or output")
        return True, self.transaction
        
    def remove_output(self, index):
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Are you sure you want to remove this output?").show()):
            self.transaction.outputs.remove(self.transaction.outputs[index])
        return self.reload_menu()

    def reload_menu(self, error = ""):
        return MenuEditTransaction(self.goodChain, self.old_transaction, self.transaction, error).show()
    
    def get_total_output(self):
        return sum([o[1] for o in self.transaction.outputs])
    
    def remove_transaction(self):
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Are you sure you want to remove this transaction?").show()):
            return True, None
        return self.reload_menu()