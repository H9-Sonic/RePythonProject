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
        print(f"File loaded and converted to mono: {file_path}")
        messagebox.showinfo("File Loaded", f"Loaded file: {file_path}\nConverted to mono if multi-channel.")

    def analyze_reverb(self):
        RT60 = self.model.analyze_reverb()
        dom_frequency = self.model.dom_freq()
        file_length = self.model.file_length()
        return RT60, dom_frequency, file_length

    #def dom_freq(self):
    #    return self.model.dom_freq()

    def plot_waveform(self):
        fig = self.model.plot_waveform()
        return fig

    def plot_spectrogram(self):
        fig = self.model.plot_spectrogram()
        return fig

    def plot_rt60(self):
        fig = self.model.plot_rt60_graph(self.current_rt60_band)
        if fig:
            print("RT60 graph plotted successfully")
        else:
            print("RT60 graph plot failed")
        # Cycle through the RT60 bands for the next button press
        current_index = self.rt60_bands.index(self.current_rt60_band)
        self.current_rt60_band = self.rt60_bands[(current_index + 1) % len(self.rt60_bands)]
        return fig

    def plot_combined_rt60(self):
        fig = self.model.plot_combined_rt60_graph()
        return fig