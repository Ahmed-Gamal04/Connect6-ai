import tkinter as tk
from gui import Connect6GUI

def main():
    root = tk.Tk()
    app = Connect6GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()