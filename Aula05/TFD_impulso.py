import numpy as np
import matplotlib.pyplot as plt


w = np.arange(-1*np.pi, np.pi, np.pi/100)

X = 1 + 2 * np.cos(w)

M_X = np.abs(X)
F_X = np.angle(X)

plt.plot(M_X)
plt.plot(F_X)

plt.show()
