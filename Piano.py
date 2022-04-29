import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


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


# functions

# calculates the step function which defines the playing interval and uses it to generate a single note
def tone_generator(start_time, period, freq):
    u1 = u2 = np.zeros(np.shape(t))

    u1[t >= start_time] = 1
    u2[t >= start_time + period] = 1
    plt.subplot(2,1,1)
    plt.plot(t,u1)
    plt.subplot(2,1,2)
    plt.plot(t,u2)
    step = u1 - u2
    note = np.sin(2 * np.pi * t * freq) * step

    return note


# main
t = np.linspace(0, 3, 12 * 1024) # parameters are (start time, duration, samplerate * duration)
x = tone_generator(0, 3, c4)  # x will contain the notes, this is a placeholder

#plt.plot(t, x)
plt.show()
#sd.play(x, 3 * 1024)
