# -*- coding: utf-8 -*-
"""

@author: Andriy
"""

import numpy as np
import matplotlib.pyplot as plt


# Lendo arquivo como binario
try:
    with open ("alo.pcm", "rb") as file:
        fid = file.read()
        file.close()
except:
    print("Falha ao abrir arquivo")
    exit(0)

s = np.frombuffer(fid, dtype = "int16")
len_data = len(s)
itera = len(s)

ganho = .5

# Executa o processamento
final_data = np.ones_like(s)
for i in range(itera):
    final_data[i] = s[i] * ganho


plt.figure("Figura 1",figsize=(15,8))

# Plotando a saída
plt.subplot(211)
plt.title("Sinal de entrada")
plt.xlabel("Número de amostras")
plt.ylabel("Amplitude da saída")
plt.grid(1)
plt.plot(s)

plt.subplot(212)
plt.title("Sinal de saída")
plt.xlabel("Número de amostras")
plt.ylabel("Amplitude da saída")
plt.grid(1)
plt.plot(final_data,color='red')


plt.tight_layout()

# Salvando o arquivo de saída
with open("sinal_saida.pcm", "wb") as new_file:
    for data in final_data:
        new_file.write(data)
    new_file.close()

# Salvando os gráficos
plt.savefig("graficos_sinais.png", format="png")


plt.show()
