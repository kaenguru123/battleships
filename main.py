from tkinter import *
from tkinter import ttk

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
                self.attacked.append((row, column))
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
    
    def hit(self, row, column):
        if not len(self.opponent_ships) == 0:
            return (row, column) in self.opponent_ships      
        return False


app = App()