from os import system, name
from time import sleep
from colorama import Fore, Back, Style
import KeyboardInput

class TerminalMenu:

    def __init__(self, items, title, menu_cursor, menu_cursor_style, menu_highlight_style):
        self.title = title
        self.items = items
        self.selected_index = 0
        self.menu_cursor = menu_cursor
        self.menu_cursor_style = menu_cursor_style
        self.menu_highlight_style = menu_highlight_style
    

    def show(self):
        while True:
            self.clear()
            print(self.title)
            for i, item in enumerate(self.items):
                if i == self.selected_index:
                    print(Back.WHITE + Fore.BLACK + self.menu_cursor + ' ' + item.replace("\n", "\n  ") + Style.RESET_ALL)
                else:
                    print(' ' + item.replace("\n", "\n "))
            kb = KeyboardInput.KBHit()
            key = None
            # sleep(0.2)
            while key == None:
                key = kb.getch()
                if key == b'\xe0':
                    key = kb.getch()
                    if key == b'H':
                        self.selected_index = (self.selected_index - 1) % len(self.items)
                        key = None
                        break
                    elif key == b'P':
                        key = None
                        self.selected_index = (self.selected_index + 1) % len(self.items)
                        break
                    else:
                        key = None
                        continue
                if key == b'\r':
                    key = None
                    return self.selected_index
                else:
                    key = None
                    continue
    
    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')