import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

n = np.arange(-20, 20, 1)
f = 400
Fs = 8000
Ts = 1/Fs

s = np.sin(2*np.pi*n*(f/Fs))

plt.stem(n,s)
plt.title('Sinusoidal (Fo=100Hz e Fs=8kHz)')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)

with open("senoidal.pcm", "wb") as new_file:
    for x in s:
        new_file.write(x)
new_file.close()