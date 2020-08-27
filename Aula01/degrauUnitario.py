import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

n = np.arange(-10, 20)
l = np.size(n)
s = np.zeros(l)
ind = np.where(n>=0)
s[ind] = 1

plt.stem(n,s)
plt.title('Degrau Unitario')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
