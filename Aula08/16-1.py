import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

TAM = 4999
M = 100
Fc = 0.14

# input signal
x = np.zeros(TAM)
# output signal
y = np.zeros(TAM)
# filter kernel
h = np.zeros(M)

# tem que fazer alguma coisa aqui pra carregar o vetor X
read_path = "Sweep10_3600.pcm"
with open(read_path, 'rb') as f:
    buf = f.read()
    x = np.frombuffer(buf, dtype='int16')

for i in range(M):
    if i-M/2 == 0:
        h[i] = 2 * np.pi * Fc
    else:
        h[i] = np.sin(2 * np.pi * Fc * (i - M / 2)) / (i - M / 2)
    h[i] = h[i] * (0.54 - 0.46 * np.cos(2 * np.pi * (i / M)))

soma = 0
for i in range(M):
    soma = soma + h[i]
    
for i in range(M):
    h[i] = h[i] / soma
    
for j in range(M, TAM, 1):
    y[j] = 0
    for i in range(M):
        y[j] = y[j] + x[j-i] * h[i]
        

plt.figure("Gráficos",figsize=(15,15))  
plt.subplot(2,1,1)
plt.title("Filtro kernel")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(y)

[w, h] = freqz(y, worN=8000, fs=1)
plt.subplot(2,1,2)
plt.title("Filtro kernel")
plt.xlabel("Amplitude")
plt.ylabel("Frequencia")
plt.grid(1)
plt.plot(w, abs(h))

plt.show()