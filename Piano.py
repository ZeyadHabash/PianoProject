from math import ceil

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

# Piano Frequencies
# 3rd Octave
c3 = 130.81
d3 = 146.83
e3 = 164.81
f3 = 174.61
g3 = 196
a3 = 220
b3 = 246.93

# 4th Octave
c4 = 261.63
d4 = 293.66
e4 = 329.63
f4 = 349.23
g4 = 392
a4 = 440
b4 = 493.88


# Functions

# Calculates the step function, using the given amplitude, which defines the playing interval and uses it to generate
# a note with the given frequencies
def tone_generator(start_time, period, freq1, freq2, amp):
    u1 = np.zeros(np.shape(t))
    u2 = np.zeros(np.shape(t))

    # Initialize u1 and u2 as unit step functions with given amplitude
    u1[t >= start_time] = amp
    u2[t >= start_time + period] = amp

    # Final step which determines the time of playing the tone calculated by subtracting 2 unit step functions
    step = u1 - u2

    # Tone calculated using [sin (2𝜋Ϝ𝑖𝑡) + sin (2𝜋𝑓𝑖𝑡) ] * step
    # where step is [𝑢(𝑡 − 𝑡𝑖) − 𝑢(𝑡 − 𝑡𝑖 − 𝑇𝑖)]
    note = (np.sin(2 * np.pi * t * freq1) + np.sin(2 * np.pi * t * freq2)) * step

    return note


# Generates a whole song by adding tones made using the tone_generator() function
def song_generator(t_start, t_period, frequencies1, frequencies2, amps):  # Parameters are arrays of (start time,
    # periods, left hand frequencies, right hand frequencies, amplitudes)
    pt = 0

    # For loop which adds all tones made by passing each element of the given arrays to the tone_generator() function
    for i in range(len(amps)):
        note = tone_generator(t_start[i], t_period[i], frequencies1[i], frequencies2[i], amps[i])
        pt = pt + note
    return pt


# Main
f1, f2 = np.random.randint(0, 512, 2)
t = np.linspace(0, 3, 12 * 1024)  # Parameters are (start time, duration, samplerate * duration)
amps = [1, 0.5, 0.5, 0.2, 1, 0.3, 0.9]
t_start = [0, 0.35, 0.85, 1.15, 2, 2.35, 2.9]
t_period = [0.25, 0.4, 0.25, 0.75, 0.25, 0.5, 0.1]
frequencies_1 = [0, 0, 0, 0, 0, 0, 0]
frequencies_2 = [c4, d4, e4, c4, e4, g4, a4]

song = song_generator(t_start, t_period, frequencies_1, frequencies_2, amps)

N = 3 * 1024
f = np.linspace(0, 512, int(N / 2))
# song before noise
song_f = fft(song)
song_f = 2 / N * np.abs(song_f[0:int(N / 2)])

n = tone_generator(0, 3, f1, f2, 1)
# song with noise
final_song = song + n
final_song_f = fft(final_song)
final_song_f = 2 / N * np.abs(final_song_f[0:int(N / 2)])

maxOG = np.amax(song_f)

freqList = []
for frqIndex in range(len(final_song_f)):
    if final_song_f[frqIndex] > ceil(maxOG):
        freqList.append(frqIndex)

fn1 = round(f[freqList[0]])
fn2 = round(f[freqList[1]])

filteringTone = tone_generator(0, 3, fn1, fn2, 1)

# song after filtering
song_filtered = final_song - filteringTone
song_filtered_f = fft(song_filtered)
song_filtered_f = 2 / N * np.abs(song_filtered_f[0:int(N / 2)])

sd.play(song_filtered, 3 * 1024)
plt.subplot(3, 2, 1)
plt.plot(t, song)
plt.subplot(3, 2, 2)
plt.plot(f, song_f)
plt.subplot(3, 2, 3)
plt.plot(t, final_song)
plt.subplot(3, 2, 4)
plt.plot(f, final_song_f)
plt.subplot(3, 2, 5)
plt.plot(t, song_filtered)
plt.subplot(3, 2, 6)
plt.plot(f, song_filtered_f)

plt.show()
sd.wait()
