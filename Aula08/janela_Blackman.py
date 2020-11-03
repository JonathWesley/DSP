import numpy as np
from numpy import pi, sin, log10, zeros
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.signal import freqz


sample_rate = 8000
M = 2

# para calcular os valores
i = np.arange(0, M, 1/sample_rate)

# função sinc (low-pass filter)
w_i = 0.42 - 0.5 * np.cos(2*np.pi*i/M) - 0.08 * np.cos(4*np.pi*i/M)

###############
#   plot
subplot(2, 1, 1)
plt.plot(i, w_i, label="Blackman")
plt.legend()

[w, h] = freqz(w_i, worN=sample_rate, fs=1)

subplot(2, 1, 2)
plot(w, 20 * log10(abs(h)), 'b')
plt.xlabel("Freq")
plt.ylabel("Magnitude")

grid()
show()
