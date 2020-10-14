# -*- coding: utf-8 -*-
"""

@author: Jonath
"""

import numpy as np
import matplotlib.pyplot as plt

sample_rate = 8000
media_buf = np.zeros(2)
saida = 0

Fc = 200
Fs = sample_rate

# calcula FC
wc = 2*np.pi*Fc

# F'
F1 = 2 * Fs

# coeficientes
a = wc/(F1+wc)
b = (wc-F1)/(F1+wc)

read_path = "Sweep10_3600.pcm"
with open(read_path, 'rb') as f:
    buf = f.read()
    data_i = np.frombuffer(buf, dtype='int16')
    data_len = len(data_i)

    data_o = np.zeros_like(data_i)

    for i in range(data_len):
        media_buf[0] = data_i[i]

        m = a*media_buf[0] + a*media_buf[1] - b*saida
        saida = m     # y-1
        data_o[i] = m
        media_buf[1:2] = media_buf[0:1]

# amostra de 100 ms
t = np.arange(0, data_len/sample_rate, 1 / sample_rate)


plt.figure("Gráficos",figsize=(15,12))

plt.subplot(211)
plt.title("Entrada")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid(1)
plt.plot(t, data_i[: len(t)])
plt.xticks(np.arange(0, 5.1, 1))
plt.yticks(np.arange(-15000, 15000.1, 5000))


plt.subplot(212)
plt.title("Saida")
plt.xlabel("n")
plt.ylabel("x[n]")
plt.grid(1)
plt.plot(t, data_o[: len(t)])
plt.xticks(np.arange(0, 5.1, 1))
plt.yticks(np.arange(-15000, 15000.1, 5000))


file_name = "Sweep10_3600_result.pcm"
with open(file_name, 'wb') as f:
    for d in data_o:
        f.write(d)