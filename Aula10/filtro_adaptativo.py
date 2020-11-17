import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

Fs = 8000
N = 160

wn = np.zeros(N, dtype=np.float64)

mu = 0.0000000001

# Sistema desconhecido
with open('coeficientesPB.dat', 'r') as f:
    buf = f.read().replace("\n", "").split(",")
    buf.remove('')
    coef = np.asarray(buf, dtype=np.float16)

# vetor de entrada, x[n]
with open('wn.pcm', 'rb') as f:
    buf = f.read()
    buf = np.frombuffer(buf, dtype='int16')
    xn = buf[0:N]
    
# sinal desejado
dn = coef.T * xn

# iterações
itera = 40000
for i in range(itera):
    # filtragem
    yn = wn.T * xn
    
    # estimacao do erro
    en = dn - yn
    # normaliza
    en = en / abs(sum(en))

    # adaptacao do vetor de coeficientes
    wn = wn + 2 * mu * en * xn


# salva coeficientes
with open('coeficientesFA.dat', 'w') as f:
    for d in wn:
        f.write(str(d.astype(np.float16))+",\n")


t = np.arange(0, N / 8000, 1 / 8000)


plt.figure("Gráficos",figsize=(15,12))

plt.subplot(511)
plt.title("Erro")
plt.xlabel("N")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(en)

[w1, h1] = freqz(coef, worN=8000, fs=1)
[w2, h2] = freqz(wn, worN=8000, fs=1)

plt.subplot(512)
plt.title("Coeficientes")
plt.xlabel("N")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(coef)

plt.subplot(513)
plt.title("Coeficientes atualizado")
plt.xlabel("N")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(wn)

plt.subplot(514)
plt.title("Saída desejada")
plt.xlabel("N")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(dn)

plt.subplot(515)
plt.title("Saída do filtro")
plt.xlabel("N")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(yn)

with open('resultFA.pcm', 'wb') as f:
    yn = np.convolve(wn, buf, mode="same")
    for d in yn:
        f.write(d.astype(np.float16))

plt.tight_layout()