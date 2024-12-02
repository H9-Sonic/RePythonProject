from os import path
from pydub import AudioSegment
from pydub.playback import play
import wave
import numpy as np
import matplotlib.pyplot as plt

from controller import Controller
from model import Model
from view import View



model = Model()
view = View()
controller = Controller(model, view)
view.mainloop()

# Display the waveform of the exported mono wav file
# display_waveform(wav_file)
