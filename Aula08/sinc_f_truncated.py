import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *


sample_rate = 8000
fc = 400
M = 0.02

# para calcular os valores
i = np.arange(-M/2, M/2, 1/sample_rate)

# função sinc (low-pass filter)
h_i = np.sin(2*np.pi*fc*i)/(i*np.pi)

# para deslocar
i = np.arange(0, M, 1/sample_rate)

###############
#   plot
subplot(1, 1, 1)
plt.plot(i, h_i, label="Output")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
grid()
show()

