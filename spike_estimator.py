import csv
import numpy as np
import sys
import scipy.io


testIndicesFileName = str(sys.argv[1])
testFiringsFileName = str(sys.argv[2])
networkFileName = str(sys.argv[3])
N = int(sys.argv[4])
horizon = int(sys.argv[5])
dataset = int(sys.argv[6])

if dataset != 0:
    filename = 'CRCNS/data/DataSet' + str(dataset) + '.mat'
    N = scipy.io.loadmat(filename)['data']['nNeurons'][0][0][0][0]

test_firings = np.genfromtxt(testFiringsFileName, delimiter=",")
test_indices = np.genfromtxt(testIndicesFileName, delimiter=",").astype(int)
if dataset != 0:
    test_indices = test_indices - 1
S = np.zeros((N,N))
rank = 3

original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            row = np.array(row).astype(float)
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2]))

for i,j,k in zip(original_network[0],original_network[1], original_network[2]):
    S[int(i),int(j)] = k;

n = 0
accuracies = []
num_firings = []
Ks = []
# S[j,i]
# Iterate through the simulation spikes
print(len(test_firings))
while n < len(test_firings):

    start = test_firings[n] 
    end = start + horizon

    # Find the location of all the nodes that fired in the window
    index = np.array(np.where((test_firings >= start) & (test_firings < end)))[0]
    indices_in_window = np.array([test_indices[i] for i in index])[1:]
    num_firings.append(indices_in_window.size)
    
    # Find the neuron that originates the cascade
    current_neuron = test_indices[n]

    # Find the connected neurons to the original one and the weights of their connections
    connected_neurons = [i for i in np.where(S[current_neuron,:] > 0)[0]]
    weights = [i for i in S[current_neuron,np.where(S[current_neuron,:] > 0)][0]]

    # Order the possibly spiking neurons by weight
    possible_neurons = [connected_neurons[np.flip(np.argsort(weights))[i]] for i in range(len(weights))]


    while len(set(possible_neurons)) < indices_in_window.size:
        connected_neurons_2 = []
        weights_2 = []
        size_set = len(set(possible_neurons))
        for neuron in possible_neurons:
            if np.where(S[neuron,:] > 0)[0].size > 0:
               connected_neurons_2 = connected_neurons_2 + [i for i in np.where(S[neuron,:] > 0)[0]]
               weights_2 = weights_2 + [i for i in S[neuron,np.where(S[neuron,:] > 0)][0]]
                
        connected_neurons = connected_neurons + connected_neurons_2
        weights = weights + weights_2
        # # Order the possibly spiking neurons by weight
        possible_neurons = [connected_neurons[np.flip(np.argsort(weights))[i]] for i in range(len(weights))]

        # No new neurons were added
        if size_set == len(set(possible_neurons)):
            break
   
    idxs = []
    for i in range(len(possible_neurons)):
        if np.sum(np.array(possible_neurons) == possible_neurons[i]) > 1:
            count = 0
            for j in range(len(possible_neurons)):
                if count == 0 and possible_neurons[j] == possible_neurons[i]:
                    count = 1
                elif count != 0 and possible_neurons[j] == possible_neurons[i]:
                    idxs.append(j)
    possible_neurons_2 = []
    for i in range(len(possible_neurons)):
       if np.sum(np.array(idxs) == i) > 0:
            continue
       else:
            possible_neurons_2.append(possible_neurons[i])
        
    possible_neurons = possible_neurons_2
    Ks.append(indices_in_window.size)

    if num_firings[-1] > 0:
        accuracy = np.sum(np.array([np.sum(possible_neurons == i) for i in indices_in_window]))*indices_in_window.size**-1        
        accuracies.append(accuracy)

    n = index[-1] + 1

print('Accuracy is : ', np.mean(np.array(accuracies)))
print('Average K is: ', np.mean(np.array(Ks))+1)
#0.8343457427306646 networkFileName
# 0.10438514907359596 inferredNetworkFileName
# 0.07691112545496863 Real dataset 4
