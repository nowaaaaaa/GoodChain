from simple_term_menu import TerminalMenu

class Menu:
# implement a modular class to create menus you can navigate through using arrow keys without using consolemenu library
    def __init__(self, items, functions):
        self.title = title
        self.items = items
        self.functions = functions
        self.terminal_menu = TerminalMenu(items, title, menu_cursor='>', menu_cursor_style=('fg_red', 'bold'), menu_highlight_style=('bg_blue', 'fg_yellow'))
        
    def show(self):
        selected_index = self.terminal_menu.show()
        self.functions[selected_index]()
        

