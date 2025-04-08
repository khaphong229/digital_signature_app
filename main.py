import tkinter as tk
from gui.app import DigitalSignatureApp

def main():
    root = tk.Tk()
    app = DigitalSignatureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
