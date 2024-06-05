from Menu import *

class MenuViewKeys(Menu):
    def __init__(self, goodChain):
        title = f"Your public key:\n{goodChain.user.public_key}\nYour private key:\n{goodChain.user.get_private_key().private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )}"
        items = ["Back"]
        functions = [self.back]
        Menu.__init__(self, goodChain, title, items, functions)

    def back(self):
        from MenuUser import MenuUser
        self.goodChain.set_menu(MenuUser(self.goodChain))