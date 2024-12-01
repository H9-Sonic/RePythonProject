from os import path
from pydub import AudioSegment
from pydub.playback import play

m4a_file = "clap2.m4a"
wav_file = "clap2.wav"


sound = AudioSegment.from_file(m4a_file, format='m4a')
sound.export(wav_file, format="wav")

original_audio = AudioSegment.from_wav(wav_file)
channel_count = original_audio.channels
print(channel_count)
monoSound_wav = original_audio.set_channels(1)
monoSound_wav.export(wav_file, format="wav")
monoSound_audio = AudioSegment.from_wav(wav_file)
channel_count = monoSound_audio.channels
print(channel_count)