import numpy as np
import matplotlib.pyplot as plt
import sys

seed=int(sys.argv[1])
N=int(sys.argv[2])
I_var=float(sys.argv[3])
simulation_duration=int(sys.argv[4])
NUMBER_NEURONS = N

networkFileName = '../spike_data/network_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + str(seed) + '.csv'
firingsFileName = '../spike_data/firings_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + str(seed) + '.csv'
indicesFileName = '../spike_data/indices_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + str(seed) + '.csv'

network = np.genfromtxt(networkFileName, delimiter=',')
firings = np.genfromtxt(firingsFileName, delimiter=',')
indices = np.genfromtxt(indicesFileName, delimiter=',')

num_spikes = firings.shape[0]
freq_spikes = (num_spikes)/simulation_duration
freq_spikes_neuron = (num_spikes)/(simulation_duration*N)
print('Freq spikes %d.2 Hz ' % freq_spikes) 
print('Freq spikes/neuron Hz  %d.2 ' % freq_spikes_neuron) 

bincount = np.bincount(firings.astype(int))

plt.figure()
plt.hist(bincount,25)
plt.xlabel('number of spikes')
plt.ylabel('number of occurrences')
plt.grid()
plt.title('Histogram of a simulated network of ' + str(NUMBER_NEURONS) + ' neurons')
plt.savefig('histogram_number_spikes_simulated.png',dpi=300)



