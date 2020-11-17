import numpy as np
from numpy import log10
import matplotlib.pyplot as plt
from scipy.signal import freqz

M = 500
Fc = 0.015
K = 1

# criar o vetor q vai armazenar os valores
h_i = np.zeros(M)

#240 ' 'Calculate the low-pass filter kernel via Eq. 16-4
#250 FOR I% = 0 TO 100
#260 IF (I%-M%/2) = 0 THEN H[I%] = 2*PI*FC
#270 IF (I%-M%/2) <> 0 THEN H[I%] = SIN(2*PI*FC * (I%-M%/2)) / (I%-M%/2)
#280 H[I%] = H[I%] * (0.54 - 0.46*COS(2*PI*I%/M%) )

# função windowed sinc
for i in range(M):
    if i-M/2 == 0:
        h_i[i] = 2 * np.pi * Fc * K
    else:
        h_i[i] = K * (np.sin(2*np.pi*Fc*(i - M / 2))/(i-M/2)) * (0.42-0.5*np.cos((2*np.pi*i)/M) + 0.08*np.cos((4*np.pi*i)/M))

# plot magnitude
plt.figure("Gráficos",figsize=(15,15))  
plt.subplot(2,1,1)
plt.title("Filtro kernel")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(h_i)

[w, h] = freqz(h_i, worN=8000, fs=1)
plt.subplot(2,1,2)
plt.title("Filtro kernel")
plt.xlabel("Amplitude")
plt.ylabel("Frequencia")
plt.grid(1)
plt.plot(w, abs(h))

plt.show()
