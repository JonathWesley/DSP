import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with open ('alo.pcm', 'rb') as f:
        buffer = f.read ()
        data = np.frombuffer (buffer, dtype = 'int16')
        left = data [:: 2]
        right = data [1 :: 2]
    
    Fs = 8000 
    t1 = 1.0 * 10**-3 
    t2 = 1.5 * 10**-3
    n = [int(t1 * Fs), int(t2 * Fs), 0]
    
    a = [.5, .3, .2]
    delay = n[2]
    delayArray = np.zeros(len(data), dtype = "int16");
    
    result = np.copy(data)
    
    for i in range(len(a)):
        for j in range(len(data)):
            delayArray[j] = a[i] * data[j]
            
            np.concatenate([result, np.zeros(n[i], dtype = "int16")])
            
        result = np.concatenate([result, delayArray])
    
    plt.figure("Eco", figsize=(15,8))
    
    plt.subplot(211)
    plt.title("Entrada")
    plt.xlabel("Numero de amostras")
    plt.ylabel("Amplitude")
    plt.grid(1)
    plt.plot(data, color='green')
    
    plt.subplot(212)
    plt.title("Saída")
    plt.xlabel("Numero de amostras")
    plt.ylabel("Amplitude")
    plt.grid(1)
    plt.plot(result, color='red')
    
    plt.tight_layout()
    plt.show()
    
    with open("aloEco.pcm", "wb") as new_file:
        for x in result:
            new_file.write(x)
        new_file.close()