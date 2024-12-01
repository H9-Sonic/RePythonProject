from os import path
from pydub import AudioSegment
from pydub.playback import play
import wave
import numpy as np
import matplotlib.pyplot as plt

from controller import Controller
from model import Model
from view import View

"""
# Convert m4a to wav and set mono
m4a_file = "clap2.m4a"
wav_file = "clap2.wav"

sound = AudioSegment.from_file(m4a_file, format='m4a')
sound.export(wav_file, format="wav")

original_audio = AudioSegment.from_wav(wav_file)
channel_count = original_audio.channels
print(f"Original channel count: {channel_count}")

# Convert to mono
monoSound_wav = original_audio.set_channels(1)
monoSound_wav.export(wav_file, format="wav")
monoSound_audio = AudioSegment.from_wav(wav_file)
channel_count = monoSound_audio.channels
print(f"Channel count after conversion to mono: {channel_count}")


# Function to display the waveform
"""
"""

def display_waveform(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        # Get parameters
        n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_file.getparams()
        print(
            f"Channels: {n_channels}, Sample Width: {sampwidth}, Frame Rate: {framerate}, Frames: {n_frames}, Compression: {comptype}")

        # Read frames and convert to numpy array
        frames = wav_file.readframes(n_frames)
        signal = np.frombuffer(frames, dtype=np.int16)

        # Create a time axis in seconds
        time_axis = np.linspace(0, n_frames / framerate, num=n_frames)

        # Plot the waveform
        plt.figure(figsize=(12, 6))
        plt.plot(time_axis, signal, label="Waveform", color="blue")
        plt.title("Waveform of the Audio")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.legend()
        plt.show()

"""

model = Model()
view = View()
controller = Controller(model, view)
view.mainloop()

# Display the waveform of the exported mono wav file
# display_waveform(wav_file)
