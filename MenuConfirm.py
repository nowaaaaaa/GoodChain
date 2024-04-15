from Menu import *

class MenuConfirm(Menu):
    def __init__(self, title):
        items = ["Confirm", "Cancel"]
        functions = [lambda : True, lambda : False]
        Menu.__init__(self, None, title, items, functions)