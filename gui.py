"""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

class GUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.low_label = tk.Button(self)
        self.low_label['text'] = "Low"
        self.low_label.grid(row=0, column=0, padx=5, pady=5)
        self.medium_label = tk.Button(self)
        self.medium_label['text'] = "Medium"
        self.medium_label.grid(row=0, column=1, padx=5, pady=5)
        self.high_label = tk.Button(self)
        self.high_label['text'] = "High"
        self.high_label.grid(row=0, column=2, padx=5, pady=5)

        self.quit = tk.Button(self, command=self.master.destroy)
        self.quit['text'] = "Quit"
        self.quit.grid(row=2, column=1, padx=5, pady=5)

    root.title('Frequency Viewer')
    root.geometry('500x300')
    root.resizable(False, False)

    title = tk.Label(root, text='Frequency Viewer', font=('Arial', 16))


    class GUI(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)


    low_label = tk.Button(root, text="Low")
    Med_label = tk.Button(root, text="Medium")
    High_label = tk.Button(root, text="High")



app = GUI(master=root)
app.mainloop()
"""