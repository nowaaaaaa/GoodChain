from Menu import Menu
from Transaction import Transaction

class MenuUser(Menu):
    def __init__(self, goodChain):
        title = f"Welcome to GoodChain, {goodChain.user.username}.\n You have {goodChain.check_available(goodChain.user.public_key)} coins available, {goodChain.check_unvalidated(goodChain.user.public_key)} coins in unvalidated blocks and {goodChain.check_pool()} outgoing and {goodChain.check_pool_incoming()} incoming coins in the pool.\n GoodChain currently has {goodChain.last_block.block_id+1  if goodChain.last_block != None else 0} {"block" if goodChain.last_block != None and goodChain.last_block.block_id == 0 else "blocks"} with {goodChain.count_tx()} total transactions."  + goodChain.get_notifications()
        for message in goodChain.get_messages():
            title += f"\n{message}"
        items = ["Make a transaction", "Mine a block", "Explore the blockchain", "View transaction pool", "View transaction history", "View your keys", "Log out", "Exit"]
        pending = 0
        for tx in goodChain.get_pool():
            if tx.ingoing[0] == goodChain.user.public_key:
                pending += 1
        if pending == 1:
            items[3] += " (You have 1 pending transaction)"
        elif pending > 1:
            items[3] += f" (You have {pending} pending transactions)"
        functions = [self.make_transaction, self.mine_block, self.explore_blockchain, self.view_transaction_pool, self.view_transaction_history, self.view_keys, self.log_out, self.exit]
        Menu.__init__(self, goodChain, title, items, functions)

    def make_transaction(self):
        from MenuTransaction import MenuTransaction
        self.goodChain.set_menu(MenuTransaction(self.goodChain))

    def mine_block(self):
        from MenuMine import MenuMine
        if self.goodChain.can_mine():
            self.goodChain.set_menu(MenuMine(self.goodChain))
        else:
            self.goodChain.set_menu(MenuUser(self.goodChain))

    def explore_blockchain(self):
        from MenuExplore import MenuExplore
        self.goodChain.set_menu(MenuExplore(self.goodChain))
    
    def view_transaction_pool(self):
        from MenuPool import MenuPool
        self.goodChain.set_menu(MenuPool(self.goodChain))

    def view_transaction_history(self):
        from MenuViewTransactions import MenuViewTransactions
        self.goodChain.set_menu(MenuViewTransactions(self.goodChain))
    
    def view_keys(self):
        from MenuViewKeys import MenuViewKeys
        self.goodChain.set_menu(MenuViewKeys(self.goodChain))

    def log_out(self):
        from MenuMain import MenuMain
        self.goodChain.log_out()
        self.goodChain.set_menu(MenuMain(self.goodChain))

    def exit(self):
        self.goodChain.set_menu(None)

