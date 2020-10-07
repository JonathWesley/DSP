import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.pyplot import axvline, axhline
from collections import defaultdict

def planoZ(z, p):
    ax = plt.subplot(2, 2, 1)

    circulo = patches.Circle((0, 0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.1)
    ax.add_patch(circulo)
    axvline(0, color='0.7')
    axhline(0, color='0.7')

    polos = plt.plot(p.real, p.imag, 'x', markersize=9, alpha=0.5)

    zeros = plt.plot(z.real, z.imag, 'o', markersize=9,
                     color='none', alpha=0.5,
                     markeredgecolor=polos[0].get_color(),
                     )

    r = 1.5 * np.amax(np.concatenate((abs(z), abs(p), [1])))
    plt.axis('scaled')
    plt.axis([-r, r, -r, r])

    plt.show()

N = [1, 0.8]
D = [1, 1, 0.41]

zeros = np.roots(N)
polos = np.roots(D)

print(zeros)
print(polos)

planoZ(zeros, polos)
