# Controller - Manages the app logic
from tkinter import messagebox


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.current_rt60_band = "low"
        self.rt60_bands = ["low", "mid", "high"]

    def load_file(self, file_path):
        self.model.file_path = file_path
        self.model.load_audio()
        self.model.convert_to_mono()
        messagebox.showinfo("File Loaded", f"Loaded file: {file_path}\nConverted to mono if multi-channel.")

    def analyze_reverb(self):
        return self.model.analyze_reverb()

    def plot_waveform(self):
        self.model.plot_waveform()

    def plot_spectrogram(self):
        self.model.plot_spectrogram()

    def plot_rt60(self):
        self.model.plot_rt60_graph(self.current_rt60_band)
        # Cycle through the RT60 bands for the next button press
        current_index = self.rt60_bands.index(self.current_rt60_band)
        self.current_rt60_band = self.rt60_bands[(current_index + 1) % len(self.rt60_bands)]

    def plot_combined_rt60(self):
        self.model.plot_combined_rt60_graph()