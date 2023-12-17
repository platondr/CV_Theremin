import numpy as np
from pygame import mixer
from scipy.io.wavfile import write

# inputting the parameters
AUDIO_RATE = 44100
length = 0.2


def generate(freq, volume):
    # creating time values
    t = np.linspace(0, length, int(length * AUDIO_RATE), dtype=np.float32)
    # generating the wave
    y = np.sin(2 * np.pi * freq * t)
    # saving the wave to a .wav file
    write("sound.wav", AUDIO_RATE, y)
    # setting the necessary volume
    mixer.music.set_volume(volume)
    # playing the sound
    sound = mixer.Sound('sound.wav')
    sound.set_volume(volume)
    sound.play()
