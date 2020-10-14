import numpy as np
from zplane import zplane

"""
        Z^2 + 1.5Z + 2
D(Z) =  --------------
             Z^2
"""

num = np.array([1, 1.5, 2])
den = np.array([1, 0, 0])

num_roots = np.roots(num)
den_roots = np.roots(den)

print(num_roots)
print(den_roots)

zplane(num, den)
