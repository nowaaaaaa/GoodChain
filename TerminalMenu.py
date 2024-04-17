import keyboard
from os import system, name
from time import sleep
from colorama import Fore, Back, Style

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
                    print(Back.WHITE + self.menu_cursor + ' ' + item.replace("\n", "\n  ") + Style.RESET_ALL)
                else:
                    print(' ' + item.replace("\n", "\n "))
            sleep(0.2)
            while True:
                key = keyboard.read_key(suppress=True)
                if key == 'up':
                    self.selected_index = (self.selected_index - 1) % len(self.items)
                    break
                elif key == 'down':
                    self.selected_index = (self.selected_index + 1) % len(self.items)
                    break
                elif key == 'enter':
                    return self.selected_index
                else:
                    continue
    
    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')