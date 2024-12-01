# View - User Interface
import tkinter as tk
from os import path
from tkinter import filedialog, messagebox

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Data Acoustic Modeling")
        self.geometry('600x400')
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self, text="Open a File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.analyze_button = tk.Button(self, text="Analyze Reverb", command=self.analyze_reverb)
        self.analyze_button.grid(row=1, column=0, padx=10, pady=10)

        self.plot_waveform_button = tk.Button(self, text="Waveform Graph", command=self.plot_waveform)
        self.plot_waveform_button.grid(row=2, column=0, padx=10, pady=10)

        self.plot_spectrogram_button = tk.Button(self, text="Intensity Graph", command=self.plot_spectrogram)
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
        rt60_time = self.controller.analyze_reverb()
        if rt60_time is not None:
            self.analysis_result.config(text=f"Estimated RT60: {rt60_time:.2f}s")
        else:
            self.analysis_result.config(text="RT60 could not be estimated.")

    def plot_waveform(self):
        self.controller.plot_waveform()

    def plot_spectrogram(self):
        self.controller.plot_spectrogram()

    def plot_rt60(self):
        self.controller.plot_rt60()

    def plot_combined_rt60(self):
        self.controller.plot_combined_rt60()

    def set_controller(self, controller):
        self.controller = controller
