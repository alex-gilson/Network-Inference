import csv
import numpy as np
import sys


testIndicesFileName = str(sys.argv[1])
testFiringsFileName = str(sys.argv[2])
networkFileName = str(sys.argv[3])
N = int(sys.argv[4])
horizon = int(sys.argv[5])

test_firings = np.genfromtxt(testFiringsFileName, delimiter=",")
test_indices = np.genfromtxt(testIndicesFileName, delimiter=",").astype(int)
S = np.zeros((N,N))
rank = 3

original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2]))

for i,j,k in zip(original_network[0],original_network[1], original_network[2]):
    S[int(i),int(j)] = k;

n = 0
# S[j,i]
current_neuron = test_indices[0]
connected_neurons = np.where(S[current_neuron,:] > 0)[0]
weights = S[current_neuron,np.where(S[current_neuron,:] > 0)][0]
# Order the possibly spiking neurons by weights
possible_neurons = [connected_neurons[np.flip(np.argsort(weights))[i]] for i in range(len(weights))]
start = test_firings[n] 
end = start + horizon
# Find the location of all the nodes that fired in the window
index = np.array(np.where((test_firings >= start) & (test_firings < end)))[0]
indices_in_window = np.array([test_indices[i] for i in index])

import pdb; pdb.set_trace()
