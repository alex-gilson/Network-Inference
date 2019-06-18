
import csv
import matplotlib.pyplot as plt
import sys
import numpy as np


networkFileName='/home/alex/Documents/Final-Year-Project/r/sim_times_2/network_10_nodes/network_stimulation_random_spikes_stimulation_time_1500_4/network_2.csv'
inferredNetworkFileName='/home/alex/Documents/Final-Year-Project/r/sim_times_2/network_10_nodes/network_stimulation_random_spikes_stimulation_time_1500_4/inferred_network_4.csv'

original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2]))

original_network = np.array(original_network)

inferred_network=[[],[],[]]
with open(inferredNetworkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            inferred_network[0].append(row[0])
            inferred_network[1].append(row[1])
            inferred_network[2].append(float(row[2]))


original_network[0] = np.add(original_network[0].astype(int),np.ones(len(original_network[0])))
original_network[1] = np.add(original_network[1].astype(int),np.ones(len(original_network[1])))
# original_network[0] = 
plt.figure()
plt.grid('--',linewidth=1, zorder=-1) 
plt.scatter(original_network[0],original_network[1], s=original_network[2].astype(float),c='b',label='Original Network', zorder=1)
plt.xlabel('source neuron index')
plt.ylabel('target neuron index')
plt.xticks([1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10])
plt.yticks([1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10])
# plt.xlim([1,11])
plt.title('Network of 10 nodes')
plt.show()           
