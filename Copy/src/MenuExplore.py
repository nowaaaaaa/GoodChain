from Menu import *

class MenuExplore(Menu):
    def __init__(self, goodChain, block = None):
        if block == None:
            block = goodChain.last_block
        self.block = block
        items = []
        functions = []
        if block == None:
            title = "Blockchain is empty"
        else:
            title = f"Block {block.block_id}, mined by {goodChain.database.get_username(block.miner)} on {block.mine_time}, validations: {len(block.sigs)}"
            next_block = block.next_block != None
            previous_block = block.previous_block != None
            if next_block:
                items.append("Next block")
                functions.append(self.next_block)
            if previous_block:
                items.append("Previous block")
                functions.append(self.previous_block)
            items.append("View transactions")
            functions.append(self.view_transactions)
            if goodChain.user != None and goodChain.user.public_key != block.miner and not block.validated_by(goodChain.user.public_key):
                items.append("Validate block")
                functions.append(self.validate_block)
        items.append("Back")
        functions.append(self.back)
        Menu.__init__(self, goodChain, title, items, functions)
    
    def next_block(self):
        self.goodChain.set_menu(MenuExplore(self.goodChain, self.block.next_block))
    
    def previous_block(self):
        self.goodChain.set_menu(MenuExplore(self.goodChain, self.block.previous_block))
    
    def view_transactions(self):
        self.goodChain.set_menu(MenuViewTransactions(self.goodChain, self.block))
    
    def validate_block(self):
        from MenuConfirm import MenuConfirm
        if MenuConfirm("Are you sure you want to validate this block?").show():
            result = self.goodChain.validate_block(self.block.block_id)
            if result:
                self.goodChain.set_menu(MenuExplore(self.goodChain, result))
            else:
                from MenuUser import MenuUser
                self.goodChain.set_menu(MenuUser(self.goodChain))
        else:
            self.goodChain.set_menu(MenuExplore(self.goodChain, self.block))
    
    def back(self):
        if self.goodChain.user == None:
            from MenuMain import MenuMain
            self.goodChain.set_menu(MenuMain(self.goodChain))
        else:
            from MenuUser import MenuUser
            self.goodChain.set_menu(MenuUser(self.goodChain))

class MenuViewTransactions(Menu):
    def __init__(self, goodChain, block):
        title = f"Transactions in block {block.block_id}:"
        items = []
        functions = []
        for tx in block.data:
            if tx.is_valid():
                title += "\nValid transaction "
            else:
                title += "\nInvalid transaction "
            title += f"{tx.id}\n{goodChain.readable_transaction(tx)}"
        items.append("Back")
        functions.append(self.back)
        self.block = block
        Menu.__init__(self, goodChain, title, items, functions)

    def back(self):
        self.goodChain.set_menu(MenuExplore(self.goodChain, self.block))