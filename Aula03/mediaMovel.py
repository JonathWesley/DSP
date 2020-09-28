import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

def moving_average(a, n) : 
    result = np.cumsum(a, dtype=float)
    result[n:] = result[n:] - result[:-n] 
    return result[n - 1:]

if __name__ == "__main__":
    with open ('wn.pcm', 'rb') as f:
        buffer = f.read ()
        data = np.frombuffer (buffer, dtype = 'int16')
        left = data [:: 2]
        right = data [1 :: 2]
        
    keys = [4, 8, 16, 32, 64, 128, 256, 512, 1024]  
    
    size = int(input("Digite o tamanho (exponencial de 2): "))
    
    result = moving_average(data, size)
    plt.figure(figsize=[15, 10])
    plt.grid(True)
    plt.plot(result, label='Media Movel')
    plt.legend(loc = 2)
    
    
    with open("mediaMovel_wn.pcm", "wb") as new_file:
        for x in result:
            new_file.write(x)
    new_file.close()