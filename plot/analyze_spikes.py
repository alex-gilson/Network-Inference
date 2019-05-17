import numpy as np

simulation_duration=int(60*1000)
I_var = 6 
number_neurons = 98
networkFileName = '../spike_data/network_' + str(int(number_neurons)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)/1000) + '.csv'
firingsFileName = '../spike_data/firings_' + str(int(number_neurons)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)/1000) + '.csv'
indicesFileName = '../spike_data/indices_' + str(int(number_neurons)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)/1000) + '.csv'

network = np.genfromtxt(networkFileName, delimiter=',')
firings = np.genfromtxt(firingsFileName, delimiter=',')
indices = np.genfromtxt(indicesFileName, delimiter=',')
import pdb; pdb.set_trace()


