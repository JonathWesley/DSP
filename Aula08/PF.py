# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 20:53:59 2020

@author: jonath
"""

import numpy as np
import matplotlib.pyplot as plt
from PB import *
from PA import *

if __name__ == '__main__':
    #Criando variáveis
    media_buf = np.zeros(2)
    saida = 0
    
    #
    FcB = 6000
    FcA = 1000
    Fs = 8000
    
    #Calculando Omega
    wcA = 2*np.pi*FcA     #6280
    wcB = 2*np.pi*FcB
    
    # F'
    F1 = 2 * Fs     #16000
    
    # coeficientes
    aB = wcB/(F1+wcB)
    bB = (wcB-F1)/(F1+wcB)
    aA = wcA/(F1+wcA)
    bA = (wcA-F1)/(F1+wcA)
    
    read_path = "Sweep10_3600.pcm"
    with open(read_path, 'rb') as f:
        buf = f.read()
        data_i = np.frombuffer(buf, dtype='int16')
        data_len = len(data_i)
    
    data_o = np.convolve(PB(data_i, data_len, saida, media_buf, aB, bB), PA(data_i, data_len, saida, media_buf, aA, bA))
    #data_o = PB(data_i, data_len, saida, media_buf, aB, bB) * PA(data_i, data_len, saida, media_buf, aA, bA)
    
    print("Valor de aA: " + str(aA))
    print("Valor de bA: " + str(bA))
    print("Valor de aB: " + str(aB))
    print("Valor de bB: " + str(bB))
    
    
    
    plt.figure("Gráficos",figsize=(25,12))
    
    plt.subplot(211)
    plt.title("Entrada")
    plt.xlabel("Frequência")
    plt.ylabel("Amplitude")
    plt.grid(1)
    plt.plot(data_i)
    
    
    plt.subplot(212)
    plt.title("Saida")
    plt.ylabel("Amplitude")
    plt.xlabel("Frequência")
    plt.grid(1)
    plt.plot(data_o)
    plt.xticks(np.arange(0, 40001, 1000))
    
    plt.tight_layout()
    
    
    
    file_name = "Result.pcm"
    with open(file_name, 'wb') as f:
        for d in data_o:
            f.write(d)
        
    plt.show()
    
    # Sim, eu sei que isso aqui nao ta certo