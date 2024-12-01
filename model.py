# model.py - Handles data and computation
from os import path
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import scipy.signal as signal

class Model:
    def __init__(self):
        self.audio = None
        self.sampling_rate = None

    def load_audio(self):
        # Load the audio using librosa
        self.audio, self.sampling_rate = librosa.load(self.file_path, sr=None, mono=False)

    def convert_to_mono(self):
        if self.audio.ndim > 1:  # If the audio has more than one channel
            self.audio = librosa.to_mono(self.audio)

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

    def plot_waveform(self):
        if self.audio is not None:
            plt.figure()
            librosa.display.waveshow(self.audio, sr=self.sampling_rate)
            plt.title('Waveform')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.show()

    def plot_spectrogram(self):
        if self.audio is not None:
            # Generate the spectrogram
            S = librosa.stft(self.audio)
            S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
            plt.figure()
            librosa.display.specshow(S_db, sr=self.sampling_rate, x_axis='time', y_axis='hz')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Spectrogram')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.show()

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
            times = np.linspace(0, 9.0, len(rt60_values))

            colors = {"low": 'orange', "mid": 'purple', "high": 'blue'}
            plt.figure()
            plt.plot(times, rt60_values, color=colors[frequency_band], linewidth=2)
            plt.title(f'{frequency_band.capitalize()} RT60 Graph')
            plt.xlabel('Time (s)')
            plt.ylabel('Power (dB)')
            #plt.xlim(0.0, 9.0)
            #plt.ylim(-40.0, 40.0)
            plt.grid(True)
            plt.show()

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

            plt.figure()
            plt.plot(times, rt60_low, color='orange', label='Low Frequency')
            plt.plot(times, rt60_mid, color='purple', label='Mid Frequency')
            plt.plot(times, rt60_high, color='blue', label='High Frequency')
            plt.title('Combined RT60 Graph')
            plt.xlabel('Time (s)')
            plt.ylabel('Power (dB)')
            #plt.xlim(0.0, 9.0)
            #plt.ylim(-40.0, 40.0)
            plt.legend()
            plt.grid(True)
            plt.show()