from tkinter import *
from tkinter import ttk
from random import *
#import random 

class App(Tk):
    def __init__(self):
        super().__init__()
        mainWindow = ttk.Frame(self, padding=0)
        mainWindow.grid()
        self.selected=[]
        self.own_field_buttons=[]
        
        self.opponent_ships=[]
        self.opponent_field_buttons=[]
        self.attacked=[]

        
        ttk.Label(mainWindow, text="You").grid(row=0, column=0)
        self.own_field = self.create_field(mainWindow)
        self.own_field.grid(row=1, column=0)
        
        self.start_btn = ttk.Button(mainWindow, text="Start Game", command=lambda s=self, m=mainWindow: s.start_game(m))
        self.start_btn.grid(row=2, column=0)
        self.mainloop()
    
    def start_game(self, mw):
        ttk.Label(mw, text="Opponent").grid(row=0, column=1)
        self.opponent_ships = self.get_rand_ship_set()
        print(len(self.opponent_ships))
        attack_field=self.create_field(mw, attack=True)
        attack_field.grid(row=1, column=1, sticky="e")
        self.convert_own_field(mw)

    def convert_own_field(self, mw):
        self.own_field.grid_forget()
        fixed_field = self.create_field(mw, fixed=True)
        fixed_field.grid(row=1, column=0)
        self.start_btn.grid_forget()

    def create_field(self, parent, attack=False, fixed=False):
        field = ttk.Frame(parent)
        width = ttk.Label(text="A").winfo_height()
        width *= 2
        for row in range(11):
            for column in range(11):
                if (row == 0 and column == 0):
                    ttk.Label(field, text="#", width=width).grid(row=row, column=column)
                elif (row == 0):
                    ttk.Label(field, text=str(column), width=width).grid(row=row, column=column)
                elif (column == 0):
                    ttk.Label(field, text=chr(64+row), width=width).grid(row=row, column=column)
                else:
                    if not fixed:
                        btn = ttk.Button(field, command=lambda r=row, c=column, a=attack: self.clicked(r, c, a), width=width)
                        btn.grid(row=row, column=column)
                        if not attack:
                            self.own_field_buttons.append(btn)
                        else:
                            self.opponent_field_buttons.append(btn)
                    elif (row, column) in self.selected:
                        ttk.Button(field, text="#", width=width).grid(row=row, column=column)
                    else:
                        ttk.Button(field, text=" ", width=width).grid(row=row, column=column)
        return field

    def clicked(self, row, column, attack):
        if attack:
            if not (row, column) in self.attacked:
                if self.hit(row, column):
                    self.opponent_field_buttons[column+((row-1)*10)-1].config(text="X")
                else:
                    self.opponent_field_buttons[column+((row-1)*10)-1].config(text="0")
                print(f"attack {row} / {column}")
            else:
                pass
        else:
            if not (row, column) in self.selected:
                self.selected.append((row, column))
                self.own_field_buttons[column+((row-1)*10)-1].config(text="#")
                print(f"selected {row} / {column}")
            else:
                self.selected.remove((row, column))
                self.own_field_buttons[column+((row-1)*10)-1].config(text="")
                print(f"UNselected {row} / {column}")
        
        # opponents strike code
    
    def hit(self, row, column):
        self.attacked.append((row, column))
        return (row, column) in self.opponent_ships      
    
    def get_rand_ship_set(self):
        ship_sizes=[2, 3, 3, 4, 5]
        ship_set=[]
        for i, len in enumerate(ship_sizes):
            new_ship = self.get_rand_ship(len, ship_set)
            for coordinate in new_ship:
                ship_set.append(coordinate)
        return ship_set
    
    def get_rand_ship(self, len, ship_set):
        valid = False
        while not valid:
            ship=[]
            valid = True
            direction = randint(0,2)
            row_pos = randint(1, 12-len)
            column_pos = randint(1, 12-len)
            for _ in range(len):
                if (row_pos, column_pos) in ship_set or (row_pos-1, column_pos) in ship_set:
                    valid = False
                    break
                ship.append((row_pos, column_pos))
                if direction: row_pos+=1 
                else: column_pos+=1
        return ship

app = App()