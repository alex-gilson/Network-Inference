import scipy.io
import numpy as np

# Load the data
n = 4
filename = 'CRCNS/data/DataSet' + str(n) + '.mat'
data = scipy.io.loadmat(filename)['data']
number_neurons = data['nNeurons'][0][0][0][0]
simulation_duration = data['recordinglength'][0][0][0][0]
# spikes = np.zeros(number_neurons)

# Count the number of spikes in the whole dataset
# for i in range(0,number_neurons):
indices = data['spikes'][0][0][:][0]
sorted_diff = np.sort(np.diff(indices[0][0]))[::-1]
print(sorted_diff)

import pdb; pdb.set_trace()
