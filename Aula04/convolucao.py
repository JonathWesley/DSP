# -*- coding: utf-8 -*-
"""

@author: Jonath
"""

import numpy as np
import matplotlib.pyplot as plt


plt.figure("Convoluções",figsize=(15,12))

h = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]

# Impulso
xUnitario = [1, 0, 0, 0, 0, 0]


plt.subplot(311)
plt.title("Impulso unitário")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid(1)
plt.stem(np.convolve(xUnitario, h))
plt.xticks(np.arange(-1, 12.1, 1))
plt.yticks(np.arange(0, 0.2, 0.05))

# Degrau unitário
xDegrau = [1, 1, 1, 1, 1, 1]

plt.subplot(312)
plt.title("Degrau unitário")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid(1)
plt.stem(np.convolve(xDegrau, h))
plt.xticks(np.arange(-1, 12.1, 1))
plt.yticks(np.arange(0, 1.1, 0.2))



plt.tight_layout()


# Salvando os gráficos
plt.savefig("graficos_sinais.png", format="png")

plt.show()

