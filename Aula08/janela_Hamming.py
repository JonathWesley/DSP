import numpy as np
from numpy import pi, sin, log10, zeros
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.signal import freqz

sample_rate = 8000
M = 2

# para calcular os valores
i = np.arange(0, M, 1/sample_rate)

# w[i] = 0.54 - 0.46*cos(2pi / M)
# função hamming window
w_i = 0.54 - 0.46 * np.cos(2*np.pi*i/M)

###############
#   plot Magnitude
subplot(2, 1, 1)
plt.plot(i, w_i, label="Output")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# pega as componentes de frequencia
[w, h] = freqz(w_i, worN=sample_rate, fs=1)

# plot Frequencia
subplot(2, 1, 2)
plot(w, 20 * log10(abs(h)), 'b')
plt.xlabel("Freq")
plt.ylabel("Magnitude")

grid()
show()
