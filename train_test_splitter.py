import csv
import scipy.io
import numpy as np
import sys


TRAIN_TEST_SPLIT = float(sys.argv[1])/100
indicesFileName = str(sys.argv[2])
firingsFileName = str(sys.argv[3])
trainIndicesFileName = str(sys.argv[4])
testIndicesFileName = str(sys.argv[5])
trainFiringsFileName = str(sys.argv[6])
testFiringsFileName = str(sys.argv[7])
dataset=int(sys.argv[8])


indices = []
firings = []

if dataset != 0:

    spikes = []

    # Load the data
    filename = 'CRCNS/data/DataSet' + str(dataset) + '.mat'
    data = scipy.io.loadmat(filename)['data']
    NUMBER_NEURONS = data['nNeurons'][0][0][0][0]
    N = NUMBER_NEURONS
    simulation_duration = data['recordinglength'][0][0][0][0]

    # This is needed to create a firings and indices file
    for i in range(0,NUMBER_NEURONS):
        spikes.append(data['spikes'][0][0][i][0][0])

        # Flatten the firing times from each of the neurons
        firings = [item for sublist in spikes for item in sublist]

        # Create the indices where each row is a different index
        indices = [[i+1]*len(spikes[i]) for i in range(len(spikes))]

        # Flatten the indices from each of the spikes
        indices = [item for sublist in indices for item in sublist]

        # Order the firings and indices chronologically
        sort_idx = np.argsort(firings)
        firings = [firings[sort_idx[i]] for i in range(len(firings))]
        indices = [indices[sort_idx[i]] for i in range(len(indices))]

# It isn't a real dataset, it's simulated
if dataset == 0:

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
train_firings = firings[:cutoff]
test_firings = firings[cutoff:]
train_indices = indices[:cutoff]
test_indices = indices[cutoff:]

np.savetxt(trainFiringsFileName, train_firings, delimiter=",")
np.savetxt(testFiringsFileName, test_firings, delimiter=",")
np.savetxt(trainIndicesFileName, train_indices, delimiter=",")
np.savetxt(testIndicesFileName, test_indices, delimiter=",")



