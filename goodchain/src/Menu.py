# from simple_term_menu import TerminalMenu
from TerminalMenu import *
from Chain import *

class Menu:
    def __init__(self, goodChain, title, items, functions):
        self.goodChain = goodChain
        self.title = title
        self.items = items
        self.functions = functions
        self.terminal_menu = TerminalMenu(items, title, menu_cursor='>', menu_cursor_style=('fg_red', 'bold'), menu_highlight_style=('bg_blue', 'fg_yellow'))
        
    def show(self):
        selected_index = self.terminal_menu.show()
        return self.functions[selected_index]()
        

