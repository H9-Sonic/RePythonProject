# model.py - Handles data and computation
from os import path
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import scipy.signal as signal
from matplotlib.figure import Figure
from pydub import AudioSegment
from scipy.signal import welch
from scipy.io import wavfile



class Model:
    def __init__(self):
        self.audio = None
        self.sampling_rate = None

    def convert_audio(self):
        #convert audio from .m4a to .wav
        m4a_file = "clap2.m4a"
        wav_file = "clap2.wav"

        #converts if there is a file present
        sound = AudioSegment.from_file(m4a_file, format='m4a')
        sound.export(wav_file, format="wav")
        print("Audio converted to .wav")
        return wav_file


    def load_audio(self):
        # Load the audio using librosa
        try:
            self.audio, self.sampling_rate = librosa.load(self.file_path, sr=None, mono=False)
        except Exception as e:
            print(f"Error loading audio; {e}")

    def convert_to_mono(self):
        if self.audio.ndim > 1:  # If the audio has more than one channel
            self.audio = librosa.to_mono(self.audio)
            print(f"Audio converted to mono")
        else:
            print("Audio is already mono")

    def analyze_reverb(self):
        # Calculate RT60 using the Schroeder integration method
        if self.audio is not None:
            impulse_response = np.correlate(self.audio, self.audio, mode='full')
            impulse_response = impulse_response[impulse_response.size // 2:]
            energy = np.cumsum(impulse_response[::-1] ** 2)[::-1]
            energy_db = 10 * np.log10(energy / np.max(energy))
            times = np.arange(energy_db.size) / self.sampling_rate
            # Find the RT60 time by looking for a drop of 60 dB
            rt60_idx = np.where(energy_db <= -60)[0]
            rt60_time = times[rt60_idx[0]] if rt60_idx.size > 0 else None
            return rt60_time
        return None

    def dom_freq(self):
        sample, data = wavfile.read("clap2.wav")
        frequencies, power = welch(data, sample, nperseg=4096)
        dominant_freq = frequencies[np.argmax(power)]
        #print(f'Dominant frequency: {round(dominant_freq)}Hz')
        return dominant_freq

    def file_length(self):
        #gives length of audio file in seconds
        audio = AudioSegment.from_wav(self.convert_audio())
        file_length = len(audio) / 1000

        #print(f'The audio is {file_length} seconds long')
        return file_length

    def plot_waveform(self):
        if self.audio is not None:
            librosa.display.waveshow(self.audio, sr=self.sampling_rate)

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            librosa.display.waveshow(self.audio, sr=self.sampling_rate, ax=ax)
            ax.set_title('Waveform')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            return fig

    def plot_spectrogram(self):
        if self.audio is not None:
            # Generate the spectrogram
            S = librosa.stft(self.audio)
            S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            librosa.display.specshow(S_db, sr=self.sampling_rate, x_axis='time', y_axis='hz', ax=ax)
            ax.set_title('Spectrogram')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            return fig

    def plot_rt60_graph(self, frequency_band):
        if self.audio is not None and frequency_band in ["low", "mid", "high"]:
            # Generate RT60 data based on actual audio data
            S = librosa.stft(self.audio)
            S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
            freqs, times, Sxx = signal.spectrogram(self.audio, self.sampling_rate)

            # Adjust frequency bands to capture different characteristics
            if frequency_band == "low":
                freq_mask = (freqs >= 60) & (freqs <= 200)
            elif frequency_band == "mid":
                freq_mask = (freqs > 250) & (freqs <= 1500)
            else:  # "high"
                freq_mask = (freqs > 4000)

            Sxx_filtered = Sxx[freq_mask, :]
            rt60_values = np.mean(Sxx_filtered, axis=0)
            times = np.linspace(0, len(rt60_values)/self.sampling_rate, num=len(rt60_values))

            colors = {"low": 'orange', "mid": 'purple', "high": 'blue'}
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(times, rt60_values, color=colors[frequency_band], linewidth=2)
            ax.set_title(f'{frequency_band.capitalize()} RT60 graph')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power (dB)')
            ax.grid(True)
            return fig
        else:
            print("Audio not loaded")
            return None


    def plot_combined_rt60_graph(self):
        if self.audio is not None:
            # Generate RT60 data for low, mid, and high frequencies based on actual audio data
            S = librosa.stft(self.audio)
            S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
            freqs, times, Sxx = signal.spectrogram(self.audio, self.sampling_rate)

            # Low frequencies (60-200 Hz)
            low_mask = (freqs >= 60) & (freqs <= 200)
            Sxx_low = Sxx[low_mask, :]
            rt60_low = np.mean(Sxx_low, axis=0)

            # Mid frequencies (250-1500 Hz)
            mid_mask = (freqs > 250) & (freqs <= 1500)
            Sxx_mid = Sxx[mid_mask, :]
            rt60_mid = np.mean(Sxx_mid, axis=0)

            # High frequencies (> 4000 Hz)
            high_mask = (freqs > 4000)
            Sxx_high = Sxx[high_mask, :]
            rt60_high = np.mean(Sxx_high, axis=0)

            times = np.linspace(0, 9.0, len(rt60_low))

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(times, rt60_low, color='orange', label='Low Frequency')
            ax.plot(times, rt60_mid, color='blue', label='Mid Frequency')
            ax.plot(times, rt60_high, color='purple', label='High Frequency')
            ax.set_title(f'Combined RT60 graph')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power (dB)')
            ax.grid(True)
            return fig