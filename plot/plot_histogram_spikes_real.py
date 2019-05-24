
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

n = 4   # Dataset number
# Load the data
filename = '../CRCNS/data/DataSet' + str(n) + '.mat'
data = scipy.io.loadmat(filename)['data']
NUMBER_NEURONS = data['nNeurons'][0][0][0][0]
N = NUMBER_NEURONS
simulation_duration = data['recordinglength'][0][0][0][0]
diffusion_type = 'rayleigh'

horizon = 20

spikes = []

# This is needed to create a firings and indices file
for i in range(0,NUMBER_NEURONS):
    spikes.append(data['spikes'][0][0][i][0][0])

# Flatten the firing times from each of the neurons
firings = [item for sublist in spikes for item in sublist]

# Create the indices where each row is a different index
indices = [[i+1]*len(spikes[i]) for i in range(len(spikes))]

# Flatten the indices from each of the spikes
indices = [item for sublist in indices for item in sublist]

# Order the firings and indices chronologically
sort_idx = np.argsort(firings)
firings = [firings[sort_idx[i]] for i in range(len(firings))]
indices = [indices[sort_idx[i]] for i in range(len(indices))]

num_spikes = len(firings)
freq_spikes = (1000*num_spikes)/simulation_duration
freq_spikes_neuron = (num_spikes)/(simulation_duration*N)
print('Freq spikes %d.2 Hz ' % freq_spikes) 
print('Freq spikes/neuron Hz  %d.2 ' % freq_spikes_neuron) 

# bincount = [len(np.where(np.array(indices)==i)[0]) for i in range(1,99)]
bincount = np.bincount(np.array(indices).astype(int))

plt.figure()
plt.hist(bincount)
plt.xlabel('number of spikes')
plt.ylabel('number of occurrences')
plt.title('Histogram of a dataset of ' + str(NUMBER_NEURONS) + ' neurons')
plt.grid()
plt.savefig('histogram_number_spikes_dataset.pdf',dpi=300)
plt.savefig('histogram_number_spikes_dataset.png',dpi=300)
