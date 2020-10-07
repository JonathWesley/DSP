import numpy as np
import matplotlib.pyplot as plt


a = 0.5

w = np.arange(-1*np.pi, np.pi, np.pi/100)

D = 1 - a * np.exp(-1j*w)
X = 1 / D

M_X = np.abs(X)
F_X = np.angle(X)

plt.plot(M_X)
plt.plot(F_X)

plt.show()
