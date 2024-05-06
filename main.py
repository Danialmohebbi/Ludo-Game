import logic
import interface
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
root = Tk()
root.title('converter')
root.geometry('250x200')
root.resizable(False, False)

players_num = StringVar()

def entries():
    '''
    gets an Int between 2 and 4 regarding the number of players in the game
    '''
    try:
        f = int(players_num.get())
    except ValueError:
        messagebox.showerror(message='Invalid input')
        players_num.set('')
        return
    if 2 <= f <= 4:
        root.destroy()
            
        interface.Window(logic.Ludo(f))
    else:
        messagebox.showerror(message='This a 2-4 players game')
        players_num.set('')
        return
ttk.Label(root, text='Please Enter the following: ').grid(row= 0, column=1)
ttk.Label(root, text='Players:').grid(row=1, column=0)
ttk.Entry(root, textvariable=players_num).grid(row=1, column=1)
ttk.Button(root, text='Enter', command=entries, width=10).grid(row=2, column=1)

for w in root.winfo_children():
    w.grid_configure(padx=4, pady=4)

root.mainloop()

                 
