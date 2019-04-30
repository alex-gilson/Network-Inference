
import scipy.io
import pdb
import numpy as np
import matplotlib.pyplot as plt

NUM_NEURONS = 98
data = scipy.io.loadmat('CRCNS/data/DataSet4.mat')['data']
avg_spikes = 0
spikes = np.zeros(NUM_NEURONS)
for i in range(0,NUM_NEURONS):
    
    spikes[i] = data['spikes'][0][0][i][0].shape[1]
    print(spikes[i])

mean_spikes = np.mean(spikes)
std_spikes = np.std(spikes)
plt.figure()
plt.hist(spikes,25)
plt.grid()
plt.xlabel('Number of spikes')
plt.ylabel('Number of occurrences')
plt.title('Histogram of the number of spikes')
plt.show()
pdb.set_trace()
