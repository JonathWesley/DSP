import numpy as np
from numpy import pi, cos, sin, log10
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.signal import freqz


sample_rate = 8000

# frequencia de corte deve estar entre 0 e 0.5
fc = 800/sample_rate

# definindo o roll-off
# BW é a largura em samples da banda de transição
# Tem que estar em 0 e 0.5
BW = 4000/sample_rate
M = 4 / BW

K = 1

# -M/2 to M/2
i = np.arange(0.00000001, M, 1/sample_rate)

# 16-4
h_i = K * (sin(2*pi*fc*(i-M/2))/(i-M/2)) * (0.42 - 0.5*cos(2*pi*i/M) + 0.08*cos(4*pi*i/M))
h_i = h_i / np.sum(h_i)
print(h_i)

###############
#   plot
subplot(2, 1, 1)
plt.plot(i, h_i, label="Windowed")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")


[w, h] = freqz(h_i, worN=sample_rate, fs=1)

subplot(2, 1, 2)
# plot(w, 20 * log10(abs(h)), 'b')
plot(w, abs(h), 'b')
plt.xlabel("Freq")
plt.ylabel("Magnitude")

grid()
show()
