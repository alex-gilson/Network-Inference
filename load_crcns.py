
import scipy.io
import pdb
import numpy as np
import matplotlib.pyplot as plt


DATASET_LENGTH = 25
mean_spikes = np.zeros(DATASET_LENGTH)
text_file = open("spikes_shape_data.txt", "w")
sum_spikes = np.zeros(DATASET_LENGTH)
mean_spikes = np.zeros(DATASET_LENGTH)
std_spikes = np.zeros(DATASET_LENGTH)

for n in range(1,DATASET_LENGTH + 1):
    filename = 'CRCNS/data/DataSet' + str(n) + '.mat'
    data = scipy.io.loadmat(filename)['data']
    number_neurons = data['nNeurons'][0][0][0][0]
    avg_spikes = 0
    spikes = np.zeros(number_neurons)
    
    for i in range(0,number_neurons):
        spikes[i] = data['spikes'][0][0][i][0].shape[1]
        print(spikes[i])
    
    sum_spikes[n-1] = np.sum(spikes)
    mean_spikes[n-1] = np.mean(spikes)
    std_spikes[n-1] = np.std(spikes)

    text_file.write('Dataset: %i ' % n) 
    text_file.write('Number of neurons: %d ' % number_neurons)
    text_file.write('Sum: %d ' % sum_spikes[n-1])
    text_file.write('Mean: %d ' % mean_spikes[n-1])
    text_file.write('Std: %d ' % std_spikes[n-1])
    text_file.write('\n')

text_file.close()
plt.figure()
plt.hist(spikes,25)
plt.grid()
plt.xlabel('number of spikes')
plt.ylabel('number of occurrences')
plt.title('Histogram of the number of spikes for the mouse dataset')
plt.show()

