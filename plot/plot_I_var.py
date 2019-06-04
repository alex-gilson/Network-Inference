
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib

seed=1
N=98
simulation_duration=100000
stimulation_type = 'random_spike'
NUMBER_NEURONS = N

spikes = np.zeros(21)
I_vars = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10] 
i = 0

for i, I_var in enumerate(I_vars):

    indicesFileName = 'spike_data/spike_data_random_spike/indices_' + str(int(N)) + '_' + str(int(I_var*10)) + '_' + str(int(simulation_duration)) + '_' + stimulation_type +  '_' + str(seed) + '.csv'

    indices = []

    with open(indicesFileName, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            indices.append(row)

    # Flatten the firing times from each of the neurons
    indices = np.array([item for sublist in indices for item in sublist]).astype(float)
    spikes[i] = len(indices)


matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
    
plt.figure()
plot1 = plt.plot(I_vars, spikes, label='simulated network')
plot2 = plt.vlines(4.018, 0, 636878,'r', linestyle="dashed", label=None)
plot3 = plt.hlines(636878, 0, 4.018,'r', linestyle="dashed", label=None)
plot4 = plt.plot(4.018, 636878, color='r',marker='.', zorder=2, label='mouse dataset',markersize=17)
plt.xlabel(r'$\textbf{\alpha $')
plt.ylabel('number of spikes')
plt.title('Number of spikes as a function of parameter I')
plt.legend()
plt.grid()
plt.xlim(0,None)
plt.ylim(0,None)
plt.savefig('I_var_plot.pdf',dpi=300)
plt.show()


