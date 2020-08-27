import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

n = np.arange(0, 30, 1)
A = 1
a = 2

s = A*a**n

plt.stem(n,s)
plt.title('Exponencial (a = 2)')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)