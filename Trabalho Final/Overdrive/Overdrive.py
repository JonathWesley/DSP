import numpy as np

# Normalizando o vetor de entrada
def normalize(sample, maxValue):
    sampleOut = []

    for i in range(len(sample)):
        if sample[i] != 0:
            sampleOut.append(sample[i] / maxValue)
        else:
            sampleOut.append(0)

    return sampleOut

def overdrive(sample):
    sampleOut = sample
    threshold = 1/3

    for i in range(len(sample)):
        if (0 < sampleOut[i] <= threshold) or ((-1 * threshold) <= sampleOut[i] < 0):
            sampleOut[i] = 2 * sampleOut[i]
            
        if sampleOut[i] >= threshold:
            sampleOut[i] = (3 - (2 - (3 * sampleOut[i])) ** 2) / 3

        if sampleOut[i] <= (-1 * threshold):
            sampleOut[i] = (-1 * (3 - (2 - (3 * (-1 * sampleOut[i]))) ** 2)) / 3

        if sampleOut[i] >= (2 * threshold):
            sampleOut[i] = 1

        if sampleOut[i] <= (-2 * threshold):
            sampleOut[i] = -1

    return sampleOut

# Lê o arquive colocando ele em um mapa de memoria
data = np.memmap("Guitar_test.pcm", dtype='h', mode='r')

# Define o valor máximo
maxValue = 31809

# Normaliza a entrada (-1,  1)
data = normalize(data, maxValue)

data = overdrive(data)

for i in range(len(data)):
    data[i] = data[i] * maxValue

outAudio = np.memmap("Overdrive_Python.pcm", dtype='int16', mode='w+', shape=(1, len(data)))
outAudio[:] = data[:]
del outAudio

