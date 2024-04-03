from simple_term_menu import TerminalMenu

class Menu:
# implement a modular class to create menus you can navigate through using arrow keys without using consolemenu library
    def __init__(self, items, functions):
        self.title = title
        self.items = items
        self.functions = functions
        self.selected = 0
        self.show()
        
    def show(self):
        while True:
            print("\033c")
            print(self.title)
            for i, item in enumerate(self.items):
                if i == self.selected:
                    print(f"> {item}")
                else:
                    print(f"  {item}")
            key = read_key()
            if key == u'\u2191':
                self.selected = (self.selected - 1) % len(self.items)
            elif key == u'\u2193':
                self.selected = (self.selected + 1) % len(self.items)
            elif key == "\r":
                return self.selected
        

