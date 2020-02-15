from SAPTableExtractor.mainGUI import mainGUI
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = mainGUI(master=root)
    app.mainloop()
    