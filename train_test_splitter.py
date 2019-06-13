import csv
import numpy as np
import sys


TRAIN_TEST_SPLIT = float(sys.argv[1])/100
indicesFileName = str(sys.argv[2])
firingsFileName = str(sys.argv[3])
trainIndicesFileName = str(sys.argv[4])
testIndicesFileName = str(sys.argv[5])
trainFiringsFileName = str(sys.argv[6])
testFiringsFileName = str(sys.argv[7])

# indicesFileName = "/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/indices_1.csv"
# firingsFileName = "/home/alex/Documents/Final-Year-Project/r/network_10_nodes/network_stimulation_random_spikes_stimulation_time_100_4/firings_1.csv"

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


spikes = []

# Flatten the firing times from each of the neurons
firings = np.array([item for sublist in firings for item in sublist]).astype(float)

# Flatten the firing times from each of the neurons
indices = np.array([item for sublist in indices for item in sublist]).astype(float)

# Order the firings and indices chronologically
sort_idx = np.argsort(firings)
firings = np.array([firings[sort_idx[i]] for i in range(len(firings))])
indices = np.array([indices[sort_idx[i]] for i in range(len(indices))]).astype(int)

# Do a train test split of the firing data
cutoff = int(len(firings)*TRAIN_TEST_SPLIT)
train_firings = firings[np.where(firings <= firings[cutoff])]
test_firings = firings[np.where(firings > firings[cutoff])]
train_indices = indices[np.where(firings <= firings[cutoff])]
test_indices = indices[np.where(firings > firings[cutoff])]

np.savetxt(trainFiringsFileName, train_firings, delimiter=",")
np.savetxt(testFiringsFileName, test_firings, delimiter=",")
np.savetxt(trainIndicesFileName, train_indices, delimiter=",")
np.savetxt(testIndicesFileName, test_indices, delimiter=",")



