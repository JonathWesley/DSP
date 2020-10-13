# -*- coding: utf-8 -*-
"""

@author: Jonath
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, log10, exp

plt.figure("Figura 1",figsize=(15,8))

#A
w = np.arange(0, pi, pi/1000)
num_m = 3 * (1*exp(-1j*w) - 1.2)
den_m = (exp(-1j*w) - 0.5) * (exp(-1j*w) - 0.9)

plt.subplot(311)
plt.title("A")
plt.grid(1)
plt.plot(w, 20 * log10(abs(num_m/den_m)))
plt.xticks(np.arange(0, 3.1, 0.5))
plt.yticks(np.arange(0, 25.1, 5))


#B
num_m = exp(-1j*w)
den_m = (exp(-1j*w) - 0.9) * (exp(-1j*w) - 1.2)

plt.subplot(312)
plt.title("B")
plt.grid(1)
plt.plot(w, 20 * log10(abs(num_m/den_m)))
plt.xticks(np.arange(0, 3.1, 0.5))
plt.yticks(np.arange(-10, 35.1, 10))


#C
num_m = (exp(-1j*w) + 0.9)
den_m = exp(-2j*w) + exp(-1j*w) + 0.41

plt.subplot(313)
plt.title("C")
plt.grid(1)
plt.plot(w, 20 * log10(abs(num_m/den_m)))
plt.xticks(np.arange(0, 3.1, 0.5))
plt.yticks(np.arange(-15, 10.1, 5))


plt.tight_layout()


# Salvando os gráficos
plt.savefig("graficos.png", format="png")

plt.show()
