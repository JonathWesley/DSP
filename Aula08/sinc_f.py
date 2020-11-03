import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, subplot, xlabel, ylabel, title, grid, axis, figure, show


sample_rate = 8000
fc = 100

i = np.arange(-0.1, 0.1, 1/sample_rate)

# função sinc (low-pass filter)
h_i = np.sin(2*np.pi*fc*i)/(i*np.pi)

###############
#   plot
subplot(1, 1, 1)
plt.plot(i, h_i, label="Sinc")
grid()
show()

