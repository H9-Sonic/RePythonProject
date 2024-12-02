# View - User Interface
import tkinter as tk
from os import path
from tkinter import filedialog, messagebox, Toplevel

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Data Acoustic Modeling")
        self.geometry('800x600')
        self.resizable(False, False)
        self.create_widgets()
        self.canvas = None

    def create_widgets(self):
        self.load_button = tk.Button(self, text="Open a File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.analyze_button = tk.Button(self, text="Analyze File/Convert to wav", command=self.analyze_reverb)
        self.analyze_button.grid(row=1, column=0, padx=10, pady=10)

        self.plot_waveform_button = tk.Button(self, text="Waveform Graph", command=self.plot_waveform)
        self.plot_waveform_button.grid(row=2, column=0, padx=10, pady=10)

        self.plot_spectrogram_button = tk.Button(self, text="Frequency Graph", command=self.plot_spectrogram)
        self.plot_spectrogram_button.grid(row=3, column=0, padx=10, pady=10)

        self.plot_rt60_button = tk.Button(self, text="Cycle RT60 Graphs", command=self.plot_rt60)
        self.plot_rt60_button.grid(row=4, column=0, padx=10, pady=10)

        self.plot_combined_rt60_button = tk.Button(self, text="Combine RT60 Graphs", command=self.plot_combined_rt60)
        self.plot_combined_rt60_button.grid(row=5, column=0, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.grid(row=6, column=0, padx=10, pady=10)

        self.file_label = tk.Label(self, text="File Name: None")
        self.file_label.grid(row=0, column=1, padx=10, pady=10)

        self.analysis_result = tk.Label(self, text="")
        self.analysis_result.grid(row=1, column=1, padx=10, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.load_file(file_path)
            self.file_label.config(text=f"File Name: {path.basename(file_path)}")

    def analyze_reverb(self):
        rt60_time, dom_frequency, file_length = self.controller.analyze_reverb()
        if rt60_time is not None and dom_frequency is not None and file_length is not None:
            self.analysis_result.config(text=f"Estimated RT60: {rt60_time:.2f}s\nDominant Frequency: {dom_frequency:.2f}Hz\nFile Length: {file_length:.2f}s")
        else:
            self.analysis_result.config(text="Error occurred in Analysis")


    def plot_waveform(self):
        new_window = Toplevel(self)
        new_window.title("Waveform Graph")
        new_window.geometry('800x600')

        fig = self.controller.plot_waveform()

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            print("Waveform displayed")
        else:
            messagebox.showerror("Error", "Waveform could not be plotted, no data available")


    def plot_spectrogram(self):
        new_window = Toplevel(self)
        new_window.title("Waveform Graph")
        new_window.geometry('800x600')

        fig = self.controller.plot_spectrogram()

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            print("Spectrogram displayed")
        else:
            messagebox.showerror("Error", "Waveform could not be plotted, no data available")


    def plot_rt60(self):
        new_window = Toplevel(self)
        new_window.title("RT60 Graph")
        new_window.geometry('800x600')

        fig = self.controller.plot_rt60()

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            print("RT60 Graph displayed")
        else:
            messagebox.showerror("Error", "RT60 could not be plotted, no data available")

    def plot_combined_rt60(self):
        new_window = Toplevel(self)
        new_window.title("Combined RT60 Graph")
        new_window.geometry('800x600')

        fig = self.controller.plot_combined_rt60()

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            print("RT60 Graph displayed")
        else:
            messagebox.showerror("Error", "Combined RT60 could not be plotted, no data available")

    def set_controller(self, controller):
        self.controller = controller