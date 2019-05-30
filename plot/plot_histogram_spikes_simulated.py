import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

seed=int(sys.argv[1])
N=int(sys.argv[2])
I_var=float(sys.argv[3])
simulation_duration=int(sys.argv[4])
stimulation_type = str(sys.argv[5])
NUMBER_NEURONS = N

networkFileName = 'spike_data/network_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + stimulation_type + '_' + str(seed) + '.csv'
firingsFileName = 'spike_data/firings_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + stimulation_type + '_' + str(seed) + '.csv'
indicesFileName = 'spike_data/indices_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + stimulation_type +  '_' + str(seed) + '.csv'

indices = []
firings = []

with open(indicesFileName, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        indices.append(row)

with open(firingsFileName, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        firings.append(row)

# Flatten the firing times from each of the neurons
firings = np.array([item for sublist in firings for item in sublist]).astype(float)

# Flatten the firing times from each of the neurons
indices = np.array([item for sublist in indices for item in sublist]).astype(float)

# Order the firings and indices chronologically
sort_idx = np.argsort(firings)
firings = np.array([firings[sort_idx[i]] for i in range(len(firings))])
indices = np.array([indices[sort_idx[i]] for i in range(len(indices))]).astype(int)

# The addition is to keep consistency of indices with the real dataset
indices = indices + 1

network = np.genfromtxt(networkFileName, delimiter=',')
# firings = np.genfromtxt(firingsFileName, delimiter=',')
# indices = np.genfromtxt(indicesFileName, delimiter=',')

num_spikes = firings.shape[0]
freq_spikes = (num_spikes)/simulation_duration
freq_spikes_neuron = (num_spikes)/(simulation_duration*N)
print('Number of neurons: ' + str(N) + ', Time: ' + str(simulation_duration) +  'ms , I_var: ' + str(I_var) + 'Stim type: ' + stimulation_type +  ', Seed: ' + str(seed))
print('Freq spikes %d.2 Hz ' % freq_spikes) 
print('Freq spikes/neuron Hz  %d.2 ' % freq_spikes_neuron) 
print('Number of spikes: ', num_spikes) 

bincount = np.bincount(firings.astype(int))

plt.figure()
plt.hist(bincount,25)
plt.xlabel('number of spikes')
plt.ylabel('number of occurrences')
plt.grid()
plt.title('Histogram of a simulated network of ' + str(NUMBER_NEURONS) + ' neurons')
plt.savefig('histogram_number_spikes_simulated_N_'+ str(N) + '_t_' + str(simulation_duration) +  '_I_var_' + str(I_var) + '_' + 'Stim type: ' + stimulation_type + '_'  + str(seed)+ '.png',dpi=300)



