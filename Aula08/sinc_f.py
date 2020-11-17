import numpy as np
import matplotlib.pyplot as plt


sample_rate = 8000
fc = 100

i = np.arange(-0.1, 0.1, 1/sample_rate)

#         sin(2*pi*fc*i)
# h[i] = ----------------
#              i*pi

# função sinc (low-pass filter)
h = np.sin(2*np.pi*fc*i)/(i*np.pi)

###############
#   plot
plt.figure("Gráficos",figsize=(15,15))
plt.grid(1)
plt.plot(h)

