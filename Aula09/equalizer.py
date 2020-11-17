import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def kernelLowPass(M, h, Fc, K = 1):
    for i in range(M):
        if i-M/2 == 0:
            h[i] = 2 * np.pi * Fc * K
        else:
            h[i] = K * (np.sin(2*np.pi*Fc*(i - M / 2))/(i-M/2)) * (0.42-0.5*np.cos((2*np.pi*i)/M) + 0.08*np.cos((4*np.pi*i)/M))
    return h
        
Fs = 8000
FcPB = 600
FcPA = 3000
FcPF_PB = 3000
FcPF_PA = 600
Bw = 200

GB = 0.7
GA = 0.5
GF = 0.6

# Normalizando
Bw = Bw / Fs
FcPB = FcPB / Fs
FcPA = FcPA / Fs
FcPF_PB = FcPF_PB / Fs
FcPF_PA = FcPF_PA / Fs
M = 4 / Bw
M = int(M)

# FILTRO PB #
##########################################################################################
hPB = np.zeros(M)
hPB = kernelLowPass(M, hPB, FcPB)

soma = 0
for i in range(M):
    soma = soma + hPB[i]

for i in range(M):
    hPB[i] = hPB[i] / soma
    

# FILTRO PA #
##########################################################################################
hPA = np.zeros(M)
hPA = kernelLowPass(M, hPA, FcPA)

soma = 0
for i in range(M):
    soma = soma + hPA[i]

for i in range(M):
    hPA[i] = hPA[i] / soma
    
hPA = -hPA
hPA[int(M/2)] += 1

# FILTRO PF #
##########################################################################################
hPF_PB = np.zeros(M)
hPF_PB = kernelLowPass(M, hPF_PB, FcPF_PB)

soma = 0
for i in range(M):
    soma = soma + hPF_PB[i]

for i in range(M):
    hPF_PB[i] = hPF_PB[i] / soma
    
hPF_PA = np.zeros(M)
hPF_PA = kernelLowPass(M, hPF_PA, FcPF_PA)

soma = 0
for i in range(M):
    soma = soma + hPF_PA[i]

for i in range(M):
    hPF_PA[i] = hPF_PA[i] / soma
    
hPF_PA = -hPF_PA
hPF_PA[int(M/2)] += 1

hPF = np.convolve(hPF_PA, hPF_PB)

# EQUALIZER #
##########################################################################################
h = np.convolve(hPA, hPB)
h = np.convolve(h, hPF)

with open('coeficientesEqualizer.dat', 'w') as f:
    for x in hPF:
        f.write(str(x.astype(np.float16))+",\n")
        
read_path = "Sweep_3800.pcm"
with open(read_path, 'rb') as f:
    buf = f.read()
    data_i = np.frombuffer(buf, dtype='int16')
    data_len = len(data_i)

    data_o_pb = GB * np.convolve(hPB, data_i, 'same')
    data_o_pa = GA * np.convolve(hPA, data_i, 'same')
    data_o_pf = GF * np.convolve(hPF, data_i, 'same')

    data_o = data_o_pb + data_o_pf + data_o_pa
    data_o = data_o.astype(dtype='int16')

t = np.arange(0, data_len/Fs, 1 / Fs)

plt.figure("Gráficos",figsize=(15,12))

plt.subplot(511)
plt.title("Entrada")
plt.xlabel("Tempo")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(t, data_i[: len(t)])

plt.subplot(512)
plt.title("Saída")
plt.xlabel("Tempo")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(t, data_o[: len(t)])

[wPB, hPB] = freqz(hPB, worN=Fs, fs=1)
[wPA, hPA] = freqz(hPA, worN=Fs, fs=1)
[wPF, hPF] = freqz(hPF, worN=Fs, fs=1)

plt.subplot(513)
plt.title("Resposta em frequência")
plt.xlabel("Número de amostras")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(wPB, abs(hPB))

plt.subplot(514)
plt.title("Resposta em frequência")
plt.xlabel("Número de amostras")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(wPA, abs(hPA))

plt.subplot(515)
plt.title("Resposta em frequência")
plt.xlabel("Frequência")
plt.ylabel("Amplitude")
plt.grid(1)
plt.plot(wPF, abs(hPF))

plt.tight_layout()

file_name = "resultEqualizer.pcm"
with open(file_name, 'wb') as f:
    for d in data_o:
        f.write(d)














