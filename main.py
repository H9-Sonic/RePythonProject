from os import path
from pydub import AudioSegment
from pydub.playback import play

#origional file is .m4a converting to .wav
m4a_file = "clap2.m4a"
wav_file = "clap2.wav"

#convert audio to .wav
sound = AudioSegment.from_file(m4a_file, format='m4a')
sound.export(wav_file, format="wav")

#find channel count of audio before turning to mono
original_audio = AudioSegment.from_wav(wav_file)
channel_count = original_audio.channels
print(f'The original channel count is: {channel_count}')

#turn file to mono sound
monoSound_wav = original_audio.set_channels(1)
monoSound_wav.export(wav_file, format="wav")
monoSound_audio = AudioSegment.from_wav(wav_file)
channel_count = monoSound_audio.channels
print(f'The current channel count is: {channel_count}')

#get length of audio file in seconds
file_length = len(monoSound_audio)/1000
print(f'The audio is {file_length} seconds long')
