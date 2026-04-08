import tkinter as tk
from logic import ATMLogic
from gui import ATMGUI


if __name__ == "__main__":
    prozor = tk.Tk()
    logic = ATMLogic()
    app = ATMGUI(prozor, logic)
    prozor.mainloop()