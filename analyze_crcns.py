
import scipy.io
import pdb
import numpy as np
import matplotlib.pyplot as plt


DATASET_LENGTH = 25
mean_spikes = np.zeros(DATASET_LENGTH)
text_file = open("spikes_shape_data.txt", "w")
sum_spikes = np.zeros(DATASET_LENGTH)
mean_spikes = np.zeros(DATASET_LENGTH)
median_spikes = np.zeros(DATASET_LENGTH)
std_spikes = np.zeros(DATASET_LENGTH)

plt.figure()

for n in range(1,DATASET_LENGTH + 1):
    filename = 'CRCNS/data/DataSet' + str(n) + '.mat'
    data = scipy.io.loadmat(filename)['data']
    number_neurons = data['nNeurons'][0][0][0][0]
    simulation_duration = data['recordinglength'][0][0][0][0]
    avg_spikes = 0
    spikes = np.zeros(number_neurons)
    
    for i in range(0,number_neurons):
        spikes[i] = data['spikes'][0][0][i][0].shape[1]
        print(spikes[i])
    
    duration = data['recordinglength'][0][0][0][0]
    sum_spikes[n-1] = np.sum(spikes)
    mean_spikes[n-1] = np.mean(spikes)
    median_spikes[n-1] = np.median(spikes)
    std_spikes[n-1] = np.std(spikes)
    freq_spikes = (1000*sum_spikes[n-1])/simulation_duration
    freq_spikes_neuron = (1000*sum_spikes[n-1])/(simulation_duration*number_neurons)
    
    text_file.write('Dataset: %i\n' % n) 
    text_file.write('Duration: %i' % duration)
    text_file.write('# neurons: %d ' % number_neurons)
    text_file.write('Sum: %d ' % sum_spikes[n-1])
    text_file.write('Mean: %d.2 ' % mean_spikes[n-1])
    text_file.write('Median: %d.2 ' % median_spikes[n-1])
    text_file.write('Std: %d.2 ' % std_spikes[n-1])
    text_file.write('Freq spikes %d.2 Hz ' % freq_spikes)
    text_file.write('Freq spikes/neuron: %d.2 Hz ' % freq_spikes_neuron)
    text_file.write('\n')

    
    if n > 4 and n < 9:
        plt.subplot(2,2,n-4)
        plt.hist(spikes,25)
        plt.tight_layout()
        plt.grid()
        plt.xlabel('number of spikes')
        plt.ylabel('number of occurrences')
        plt.title(str(number_neurons) + ' neurons')

text_file.close()
plt.savefig('dataset_spike_shape.pdf', dpi=300)
