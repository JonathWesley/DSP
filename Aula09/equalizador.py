import numpy as np
from numpy import pi, cos, sin, log10
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, subplot, xlabel, ylabel, title, grid, axis, figure, show
from scipy.signal import freqz


def gera_coef(M, fc):
    # 0 to M
    i1 = np.arange(10 ** -9, M, 1.)

    # Eq diretamente 16-4
    h1 = (sin(2 * pi * fc * (i1 - M / 2)) / (i1 - M / 2)) * (
                0.42 - 0.5 * cos(2 * pi * i1 / M) + 0.08 * cos(4 * pi * i1 / M))

    # normalize
    h1 = h1 / np.sum(h1)

    return h1


sample_rate = 8000

# definindo a frequencia de corte
# tem que estar entre 0 e 0.5
fc_pb = 600/sample_rate
fc_pa = 3000/sample_rate

# definindo o roll-off
# BW é a largura em samples da banda de transição
# Tem que estar em 0 e 0.5
BW = 200/sample_rate
M = 4 / BW

# filtro PB
h_pb = gera_coef(M, fc_pb)

# filtro PF
h_pf2 = gera_coef(M, fc_pa)        # passa baixa

h_pf1 = gera_coef(M, fc_pb)        # passa alta
h_pf1 = -h_pf1
h_pf1[int(M/2)] += 1
h_pf = np.convolve(h_pf1, h_pf2)

# filtro PA
h_pa = gera_coef(M, fc_pa)
h_pa = -h_pa
h_pa[int(M/2)] += 1

# ganhos
g_pb = .5
g_pf = .7
g_pa = .1


read_path = "../swip.pcm"
with open(read_path, 'rb') as f:
    buf = f.read()
    data_i = np.frombuffer(buf, dtype='int16')
    data_len = len(data_i)

    # replica do arquivo lido para salvar o resultado
    data_pb = g_pb * np.convolve(h_pb, data_i, 'same')
    data_pf = g_pf * np.convolve(h_pf, data_i, 'same')
    data_pa = g_pa * np.convolve(h_pa, data_i, 'same')

    data_o = data_pb + data_pa + data_pf

    data_o = data_o.astype(dtype='int16')


# amostra de 100 ms
t = np.arange(0, data_len/sample_rate, 1 / sample_rate)

###############
#   plot
subplot(2, 1, 1)
plt.plot(t, data_i[: len(t)], "k-", label="Input")
plt.plot(t, data_o[: len(t)], label="Output")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")


print("calculating freqz")
[w1, h1] = freqz(h_pa, worN=sample_rate, fs=1)
[w2, h2] = freqz(h_pb, worN=sample_rate, fs=1)
[w3, h3] = freqz(h_pf, worN=sample_rate, fs=1)

print("printing freqz")
subplot(2, 1, 2)
# plot(w1, 20 * log10(abs(h1)), label="freqz1")
# plot(w2, 20 * log10(abs(h2)), label="freqz2")
plot(w1, abs(h1), label="PA")
plot(w2, abs(h2), label="PB")
plot(w3, abs(h3), label="PF")
plt.legend()
plt.xlabel("Freq")
plt.ylabel("Amplitude")

file_name = "../equalizador.pcm"
with open(file_name, 'wb') as f:
    for d in data_o:
        f.write(d)

grid()
show()


