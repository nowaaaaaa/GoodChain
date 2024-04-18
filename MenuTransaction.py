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
        title =  "Setting up a transaction, available balance: " + str(goodChain.check_available(goodChain.user.public_key)) + " coins"
        if error != "":
            title += '\n' + error
        items.append("Add output")
        functions.append(self.add_output)
        items.append("Set mining reward, currently: " + str(self.transaction.get_reward()) + " coins")
        functions.append(self.set_reward)
        items.append("Confirm transaction")
        functions.append(self.confirm_transaction)
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions) 
    
    def add_output(self):
        raw_addr = input("Enter the address or username of the recipient: ")
        addr = None
        username = None
        if self.goodChain.database.get_username(raw_addr) == None:
            if self.goodChain.database.get_public_key(raw_addr) == None:
                self.reload_menu("Invalid address or username")
                return
            else:
                addr = self.goodChain.database.get_public_key(raw_addr)
                username = raw_addr
        else:
            addr = raw_addr
            username = self.goodChain.database.get_username(raw_addr)
        amount = input(f"Enter the amount to send to {username}: ")
        if not amount.isdigit() or self.goodChain.check_available(self.goodChain.user.public_key) < self.get_total_output() + int(amount):
            self.reload_menu("Invalid amount entered")
            return
        self.transaction.add_output(addr, int(amount))
        self.reload_menu()

    def set_reward(self):
        amount = input(f"Enter mining reward amount: ")
        if not amount.isdigit() or self.goodChain.check_available(self.goodChain.user.public_key) < self.get_total_output() + int(amount):
            self.reload_menu("Invalid amount entered")
            return
        self.transaction.set_reward(int(amount))
        self.reload_menu()

    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))
    
    def confirm_transaction(self):
        if len(self.transaction.outputs) <= 0:
            self.reload_menu("No outputs specified")
            return
        output = sum([o[1] for o in self.transaction.outputs])
        if self.goodChain.check_available(self.goodChain.user.public_key) < output:
            self.reload_menu("Insufficient balance")
            return
        self.transaction.set_input(self.goodChain.user.public_key, output)
        self.transaction.sign(self.goodChain.user.get_private_key())
        if not self.transaction.is_valid():
            self.reload_menu("Invalid signature or output")
            return
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Please confirm you want to make this transaction:\n" + self.goodChain.readable_transaction(self.transaction)).show()):
            self.goodChain.add_to_pool(self.transaction)
            self.goodChain.post_message("Transaction was added to pool")
            from MenuUser import MenuUser
            self.goodChain.set_menu(MenuUser(self.goodChain))
        else:
            self.reload_menu()

    def remove_output(self, index):
        from MenuConfirm import MenuConfirm
        if (MenuConfirm("Are you sure you want to remove this output?").show()):
            self.transaction.outputs.remove[index]
        self.reload_menu()

    def reload_menu(self, error = ""):
        self.goodChain.set_menu(MenuTransaction(self.goodChain, self.transaction, error))
    
    def get_total_output(self):
        return sum([o[1] for o in self.transaction.outputs])
    