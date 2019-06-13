import csv
import numpy as np
import sys


testIndicesFileName = str(sys.argv[1])
testFiringsFileName = str(sys.argv[2])
networkFileName = str(sys.argv[3])
N = int(sys.argv[4])

test_firings = np.genfromtxt(testFiringsFileName, delimiter=",")
test_indices = np.genfromtxt(testIndicesFileName, delimiter=",").astype(int)
S = np.zeros((N,N))

original_network=[[],[],[]]
with open(networkFileName, 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
            original_network[0].append(row[0])
            original_network[1].append(row[1])
            original_network[2].append(float(row[2]))

for i,j,k in zip(original_network[0],original_network[1], original_network[2]):
    S[int(i),int(j)] = k;

current_neuron = test_indices[0]
import pdb; pdb.set_trace()
